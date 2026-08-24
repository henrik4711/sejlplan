"""Stedsøgning: havneregisteret først, Open-Meteos geokoder som backup.

Registeret i `harbours.py` dækker godt 3.000 lystbådehavne og svarer uden at
røre nettet. Finder man ikke det man leder efter dér — en ø, en by, en fjord —
spørger vi Open-Meteo, samme leverandør som vejrdataene: ingen nøgle og ingen
rate limit at danse om.

Man kan også taste en position direkte. Både `55.69, 12.60` og `55°41,4'N
12°36,0'Ø` bliver forstået, for det er de to måder, positioner står skrevet i
en logbog.
"""
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass

import httpx

from .i18n import t
from . import harbours
from .config import settings

GEOCODE_URL = 'https://geocoding-api.open-meteo.com/v1/search'

_cache: dict[str, list['Place']] = {}

# Open-Meteos stedkoder vi gider vise. Resten (lufthavne, heliporte, bjergtoppe)
# er støj, når man planlægger en sejlads.
_ISLAND_CODES = {'ISL', 'ISLS', 'ISLET'}
_PLACE_PREFIX = 'PPL'

HAVN, ISLAND, TOWN, SPOT = 'havn', 'ø', 'by', 'position'

# Hvor langt en by må ligge fra en havn, før det ikke længere er den havn,
# brugeren mente. Fem sømil dækker en havneby og dens forstæder.
SNAP_NM = 5.0

# Rammer man kortet inden for den her afstand af en havn, er det havnen man
# pegede på. Længere væk er det et punkt i vandet.
HIT_NM = 0.8

# Og så langt væk kan en havn stadig bruges til at sige hvor man er.
NEAR_NM = 12.0

# Søger man efter en by, mener man den havn, gæstesejlere faktisk ligger i —
# ikke rådhuspladsen og ikke den nærmeste jollebro. De store byer har ikke en
# havn, der hedder det samme som byen, så dem peger vi selv på.
# Peger på positionen frem for navnet: der er tre "Ballen Havn" i registeret,
# men kun én af dem ligger på Samsø.
DESTINATIONS = {
    # Byer, hvor gæstehavnen hedder noget andet end byen
    'København': (55.71622, 12.58939),      # Svanemøllehavnen
    'Kbh': (55.71622, 12.58939),
    'Copenhagen': (55.71622, 12.58939),
    'Aalborg': (57.05777, 9.90212),         # Vestre Bådehavn
    'Odense': (55.41580, 10.37557),
    'Roskilde': (55.65113, 12.07747),
    'Kolding': (55.49514, 9.49988),
    'Malmö': (55.61779, 12.98839),          # Dockan Marina
    'Kiel': (54.33877, 10.15788),           # Sporthafen Düsternbrook
    'Oslo': (59.90754, 10.72471),           # Aker Brygge
    # Øer, hvor havnen hedder noget andet end øen
    'Læsø': (57.29585, 10.92378),           # Vesterø Havn
    'Samsø': (55.81607, 10.64011),          # Ballen Havn
    'Ærø': (54.89360, 10.40984),            # Ærøskøbing
    'Bornholm': (55.10454, 14.69282),       # Rønne, Nørrekås
    'Møn': (54.95341, 12.46482),            # Klintholm Havn
    'Langeland': (54.94138, 10.71073),      # Rudkøbing
}


@dataclass(frozen=True)
class Place:
    name: str
    detail: str
    lat: float
    lon: float
    kind: str = HAVN

    @property
    def icon(self) -> str:
        return {HAVN: 'anchor', ISLAND: 'landscape',
                TOWN: 'location_city'}.get(self.kind, 'my_location')


def _fold(s: str) -> str:
    """Sammenlign uden hensyn til store bogstaver og æøå/accenter."""
    s = s.lower().replace('æ', 'ae').replace('ø', 'oe').replace('å', 'aa')
    return ''.join(c for c in unicodedata.normalize('NFD', s) if not unicodedata.combining(c))


def from_harbour(h: harbours.Harbour) -> Place:
    detail = h.detail
    if h.berths:
        pladser = t('{n} pladser', n=h.berths)
        detail = f'{detail} · {pladser}' if detail else pladser
    return Place(h.name, detail or t('Lystbådehavn'), h.lat, h.lon, HAVN)


# ── Positioner ───────────────────────────────────────────────────────────────
_DEG = re.compile(r"""(?P<deg>\d{1,3})\s*[°º]\s*
                      (?:(?P<min>\d{1,2}(?:[.,]\d+)?)\s*['′]?\s*)?
                      (?:(?P<sec>\d{1,2}(?:[.,]\d+)?)\s*["″]?\s*)?
                      (?P<hemi>[NSEWØVnsewøv])""", re.VERBOSE)


def parse_coordinates(query: str) -> Place | None:
    """Genkend en indtastet position, i decimalgrader eller grader og minutter."""
    found = _DEG.findall(query)
    if len(found) == 2:
        values = {}
        for deg, minutes, seconds, hemi in found:
            value = float(deg) + _f(minutes) / 60 + _f(seconds) / 3600
            hemi = hemi.upper()
            if hemi in 'SW':
                value = -value
            values['lat' if hemi in 'NS' else 'lon'] = value
        if 'lat' in values and 'lon' in values:
            return _spot(values['lat'], values['lon'])

    parts = query.replace(';', ',').replace('/', ',').split(',')
    if len(parts) != 2:
        parts = query.split()
    if len(parts) != 2:
        return None
    try:
        lat = float(parts[0].strip().replace(',', '.'))
        lon = float(parts[1].strip().replace(',', '.'))
    except ValueError:
        return None
    return _spot(lat, lon)


def _f(value: str) -> float:
    return float(value.replace(',', '.')) if value else 0.0


def _spot(lat: float, lon: float) -> Place | None:
    if not (-90 <= lat <= 90 and -180 <= lon <= 180):
        return None
    return Place(f'{lat:.4f}°N {lon:.4f}°{t("Ø")}'.replace('.', ','),
                 'Indtastet position', lat, lon, SPOT)


# ── Søgning ──────────────────────────────────────────────────────────────────
async def search_remote(query: str, limit: int = 6) -> list[Place]:
    """Slå op hos Open-Meteos geokoder. Svar caches for resten af serverens levetid."""
    key = _fold(query)
    if key in _cache:
        return _cache[key][:limit]

    try:
        async with httpx.AsyncClient(headers={'User-Agent': settings.user_agent}) as client:
            r = await client.get(GEOCODE_URL, params={
                'name': query, 'count': 10, 'language': 'da', 'format': 'json',
            }, timeout=15)
            r.raise_for_status()
            raw = (r.json() or {}).get('results') or []
    except (httpx.HTTPError, ValueError):
        return []

    places: list[Place] = []
    for item in raw:
        code = (item.get('feature_code') or '').upper()
        if code in _ISLAND_CODES:
            kind = ISLAND
        elif code.startswith(_PLACE_PREFIX):
            kind = TOWN
        else:
            continue  # ikke et sted man sejler til

        region = ' · '.join(x for x in (item.get('admin1'), item.get('country')) if x)
        places.append(Place(
            name=item.get('name') or query,
            detail=region or t('Ukendt område'),
            lat=float(item['latitude']), lon=float(item['longitude']),
            kind=kind,
        ))

    _cache[key] = places
    return places[:limit]


def at_point(lat: float, lon: float) -> Place:
    """Hvad er dét her sted, brugeren har sat på kortet?

    Rammer man en havn, er det havnen — også når man har trukket en markør
    derhen. Rammer man vandet, får punktet navn efter det nærmeste sted, så
    planen kan sige "ud for Stevns" i stedet for at hedde noget, der passede
    et helt andet sted på kortet.
    """
    near = harbours.nearest(lat, lon, 1)
    if near:
        h = near[0]
        distance = _nm(lat, lon, h.lat, h.lon)
        if distance <= HIT_NM:
            return from_harbour(h)
        if distance <= NEAR_NM:
            return Place(t('Ud for {sted}', sted=short_name(h.name)),
                         h.detail, lat, lon, SPOT)
    return _spot(lat, lon) or Place(f'{lat:.3f}°N {lon:.3f}°{t("Ø")}',
                                    t('Position'), lat, lon, SPOT)


# Ord man ikke siger, når man peger på et sted på søkortet: "ud for Køge" er
# hvad en skipper siger, "ud for Køge Marina" er hvad en database siger.
_HARBOUR_WORDS = ('lystbådehavn', 'bådehavn', 'marina', 'sejlklub', 'havn',
                  'baadelaug', 'bådelaug', 'hamn', 'hafen', 'sportshafen')


def short_name(name: str) -> str:
    """Havnens navn skåret ned til det, stedet hedder."""
    out = name
    for word in _HARBOUR_WORDS:
        if out.lower().endswith(' ' + word):
            out = out[:-(len(word) + 1)]
    return out.strip(' -–,') or name


def snap_to_harbour(place: Place) -> Place:
    """Byt en by eller ø ud med havnen dér, hvis der ligger en tæt nok på.

    En geokoder peger på rådhuset. Man sejler ikke til et rådhus. Ligger der
    en havn inden for et par sømil, er det den, brugeren mente — og byens navn
    følger med som forklaring, så man kan se hvad man fik.
    """
    if place.kind not in (TOWN, ISLAND):
        return place
    near = harbours.nearest(place.lat, place.lon, 1)
    if not near:
        return place

    h = near[0]
    if _nm(place.lat, place.lon, h.lat, h.lon) > SNAP_NM:
        return place
    if _fold(h.name) == _fold(place.name):
        return from_harbour(h)
    return Place(h.name, t('{detalje} · ved {sted}', detalje=h.detail,
                           sted=place.name), h.lat, h.lon, HAVN)


def _nm(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    from .sailing import haversine
    return haversine(lat1, lon1, lat2, lon2)


def _alias(query: str) -> list[Place]:
    """De store byers og øers rigtige gæstehavn, hvis søgeordet er en af dem."""
    spot = _DESTINATIONS.get(_fold(query))
    if not spot:
        return []
    near = harbours.nearest(spot[0], spot[1], 1)
    return [from_harbour(near[0])] if near else []


_DESTINATIONS = {_fold(name): spot for name, spot in DESTINATIONS.items()}


async def search(query: str, limit: int = 8) -> list[Place]:
    """Samlet søgning: position → havneregister → geokoder."""
    query = query.strip()
    if not query:
        return []

    coord = parse_coordinates(query)
    if coord:
        return [coord]

    found = _alias(query)
    seen = {(round(p.lat, 3), round(p.lon, 3)) for p in found}
    for h in harbours.search(query, limit):
        key = (round(h.lat, 3), round(h.lon, 3))
        if key not in seen:
            seen.add(key)
            found.append(from_harbour(h))

    if len(found) >= 4:
        return found[:limit]

    for p in await search_remote(query, limit):
        p = snap_to_harbour(p)
        key = (round(p.lat, 3), round(p.lon, 3))
        if key not in seen:
            seen.add(key)
            found.append(p)
    return found[:limit]
