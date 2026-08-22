"""Vejrdata fra Open-Meteo.

Prognosen hentes for punkter **langs den rute, der faktisk sejles** — ikke for
rutens midtpunkt og ikke for luftlinjen. En tur fra Limfjorden til Bornholm har
ikke samme vind i begge ender, og en tur nord om Sjælland har ikke det vejr, der
står over luftlinjen tværs over øen.

Punkterne fordeles jævnt efter sejlet afstand, og hver sejltime bruger det
punkt, båden er nærmest. Det koster ét kald uanset hvor mange punkter der er,
fordi Open-Meteo tager en liste af positioner.

Bølgernes retning hentes med. Det er dét, der afgør om turen bliver en modsø,
der hamrer, eller en medsø, der skubber — og for en motorbåd betyder det mere
for både fart og komfort end vinden gør.

Svar caches på serveren, så mange samtidige brugere deler de samme kald.
"""
from __future__ import annotations

import asyncio
import time
from datetime import datetime

import httpx

from .config import TIMEZONE, settings
from .sailing import Route

FORECAST_URL = 'https://api.open-meteo.com/v1/forecast'
MARINE_URL = 'https://marine-api.open-meteo.com/v1/marine'

# Så langt vil tjenesterne give os tal. Vinden rækker til fjorten døgn, men
# bølgerne stopper ved ti, og en sejlplan uden søen er en halv plan. Ti er
# altså loftet — ikke fordi vi ikke kan spørge om mere, men fordi svaret er
# tomt derefter.
FORECAST_DAYS = 10

# Strømmen kommer i kilometer i timen. Vi regner i knob som alt andet.
KMH_TO_KN = 0.539957
MAX_POINTS = 12              # Open-Meteo tillader flere, men vi holder os høflige
SPACING_NM = 18.0            # ét prognosepunkt for hver ~18 sømil rute
CACHE_TTL_SECONDS = 30 * 60  # prognoserne opdateres langtfra hvert minut

Series = list[list[dict]]    # én tidsserie pr. punkt, i rækkefølge langs ruten

_cache: dict[str, tuple[float, Series]] = {}
_lock = asyncio.Lock()


class WeatherError(RuntimeError):
    """Vejrdata kunne ikke hentes."""


def sample_points(route: Route) -> list[tuple[float, float]]:
    """Punkter jævnt fordelt langs ruten, ét pr. ~18 sømil.

    Punkterne lægges midt i hvert afsnit, ikke i enderne — det er dér, vejret er
    repræsentativt for den strækning, punktet skal dække.
    """
    total = route.total_nm
    if total <= 0:
        wp = route.waypoints[0]
        return [(wp.lat, wp.lon)]
    count = max(1, min(MAX_POINTS, round(total / SPACING_NM) or 1))
    return [route.at(total * (i + 0.5) / count)[:2] for i in range(count)]


def series_at(weather: Series, along_nm: float, total_nm: float) -> list[dict]:
    """Den tidsserie, der hører til positionen `along_nm` inde i ruten."""
    if not weather:
        return []
    if total_nm <= 0:
        return weather[0]
    index = int(along_nm / total_nm * len(weather))
    return weather[max(0, min(len(weather) - 1, index))]


def _cache_key(points: list[tuple[float, float]]) -> str:
    # Afrund til ~1 km, så små justeringer af et waypoint stadig rammer cachen.
    return '|'.join(f'{lat:.2f},{lon:.2f}' for lat, lon in points)


async def _get_json(client: httpx.AsyncClient, url: str, params: dict) -> list[dict]:
    """Kald Open-Meteo og normalisér svaret til altid at være en liste."""
    r = await client.get(url, params=params, timeout=20)
    r.raise_for_status()
    data = r.json()
    return data if isinstance(data, list) else [data]


async def fetch_weather(route: Route) -> Series:
    """Hent time-for-time vind og bølger for punkterne langs ruten.

    Returnerer én liste pr. punkt:
    [{'time', 'wind_kn', 'wind_dir', 'gust_kn', 'wave_m', 'wave_dir', 'wave_s'}, …]
    """
    if len(route.waypoints) < 2:
        return []

    points = sample_points(route)
    key = _cache_key(points)

    async with _lock:
        hit = _cache.get(key)
        if hit and time.time() - hit[0] < CACHE_TTL_SECONDS:
            return hit[1]

    common = {
        'latitude': ','.join(f'{lat:.4f}' for lat, _ in points),
        'longitude': ','.join(f'{lon:.4f}' for _, lon in points),
        'forecast_days': FORECAST_DAYS,
        'timezone': TIMEZONE,
    }

    async with httpx.AsyncClient(headers={'User-Agent': settings.user_agent}) as client:
        try:
            wind_task = _get_json(client, FORECAST_URL, {
                **common,
                'hourly': 'windspeed_10m,winddirection_10m,windgusts_10m',
                'wind_speed_unit': 'kn',
            })
            # Strømmen hentes sammen med bølgerne. I Storebælt og Øresund
            # løber der jævnligt to-tre knob, og det er halvdelen af en
            # sejlbåds fart — en ankomsttid uden strøm er forkert præcis dér,
            # hvor det betyder mest.
            wave_task = _get_json(client, MARINE_URL, {
                **common,
                'hourly': ('wave_height,wave_direction,wave_period,'
                           'ocean_current_velocity,ocean_current_direction'),
            })
            wind_res, wave_res = await asyncio.gather(wind_task, wave_task,
                                                      return_exceptions=True)
        except httpx.HTTPError as exc:
            raise WeatherError(f'Kunne ikke hente vejrdata: {exc}') from exc

    if isinstance(wind_res, BaseException):
        raise WeatherError('Vejrtjenesten svarer ikke. Prøv igen om lidt.') from wind_res

    # Bølgedata findes ikke overalt (fx snævre fjorde og indre farvande). Det er
    # ikke en fejl – vi regner bare videre med bølgehøjde 0 og siger det tydeligt.
    waves = None if isinstance(wave_res, BaseException) else wave_res

    series: Series = []
    for i, block in enumerate(wind_res):
        hourly = block.get('hourly') or {}
        times = hourly.get('time') or []
        wave_block = (waves[i].get('hourly') or {}) if waves and i < len(waves) else {}
        heights = wave_block.get('wave_height') or []
        directions = wave_block.get('wave_direction') or []
        periods = wave_block.get('wave_period') or []
        cur_v = wave_block.get('ocean_current_velocity') or []
        cur_d = wave_block.get('ocean_current_direction') or []

        rows = []
        for j, iso in enumerate(times):
            wind_dir = _num(hourly.get('winddirection_10m'), j)
            rows.append({
                'time': datetime.fromisoformat(iso),
                'wind_kn': _num(hourly.get('windspeed_10m'), j),
                'wind_dir': wind_dir,
                'gust_kn': _num(hourly.get('windgusts_10m'), j),
                'wave_m': _num(heights, j),
                # Uden bølgeprognose bruger vi vindretningen. Søen står sjældent
                # langt fra vinden i indre farvande, og det er bedre end intet.
                'wave_dir': _num(directions, j) or wind_dir,
                'wave_s': _num(periods, j),
                # Open-Meteo giver strømmen i km/t og opgiver retningen som
                # dén, strømmen løber *mod* — samme regning som for vind ville
                # vende den forkert.
                'cur_kn': _num(cur_v, j) * KMH_TO_KN,
                'cur_dir': _num(cur_d, j),
            })
        series.append(rows)

    if not series or not series[0]:
        raise WeatherError('Vejrtjenesten returnerede ingen data for ruten.')

    async with _lock:
        _cache[key] = (time.time(), series)
        _prune_cache()

    return series


def has_wave_data(weather: Series) -> bool:
    """Falsk hvis marineprognosen manglede – så kan UI'et sige det ærligt."""
    return any(row['wave_m'] for rows in weather for row in rows)


def _num(values, index: int) -> float:
    try:
        v = values[index]
    except (TypeError, IndexError):
        return 0.0
    return float(v) if v is not None else 0.0


def _prune_cache(max_entries: int = 200) -> None:
    if len(_cache) <= max_entries:
        return
    for key in sorted(_cache, key=lambda k: _cache[k][0])[:len(_cache) - max_entries]:
        _cache.pop(key, None)
