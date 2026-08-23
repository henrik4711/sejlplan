"""Udkiggen: den, der kigger på vagterne, mens ingen er logget på.

Kører i serveren som en baggrundsopgave. Med jævne mellemrum tages hver vagt
frem, ruten regnes igennem med brugerens egen båd og egne grænser, og hvis der
er et vindue, sendes beskeden.

Tre ting, der er værd at vide om måden:

Vi regner **kun** på de dage, brugeren har bedt om. Ligger vinduet ude i
fremtiden, og prognosen ikke er nået dertil endnu, sker der ingenting — så
venter vi til i morgen. Det er hele pointen: han skal ikke sidde og trykke
opdater i fjorten dage.

Vi skriver **én gang**. Kommer beskeden, er vagten brugt. Ellers ville en model,
der flytter sig en halv knob, blive til fem mails, og så holder folk op med at
læse dem.

Og vi skriver **kun, når det holder**: turen skal kunne sejles inden for
grænserne hele vejen, og man skal kunne komme hjem igen — er man blæst inde i
tre døgn på destinationen, er det ikke en gevinst.
"""
from __future__ import annotations

import asyncio
from datetime import date, datetime

from . import mailer, share, watch, weatherbound
from .boats import BOATS, DEFAULT_BOAT, custom_boat
from .config import settings
from .dates import full
from .mishap import report
from .sailing import GO, Limits, Route, Waypoint, WARN, find_windows
from .searoute import plan_route
from .weather import fetch_weather, series_at

# Hvor tit der kigges. Prognosen opdateres nogle få gange i døgnet, så oftere
# end det er spildt — og vi henter vejr for hver eneste vagt.
INTERVAL_S = 3 * 3600

# Vent lidt efter opstart. Serveren skal have lov at komme på benene og svare
# på det første besøg, før den går i gang med at regne ruter.
WARMUP_S = 90

# Ligger vinduet mere end så mange døgn ude, er der ingen grund til at regne:
# prognosen rækker der ikke endnu.
from .state import MAX_FORECAST_DAYS  # noqa: E402


def _boat_of(spec: dict):
    """Brugerens båd, som den var da vagten blev lagt."""
    if spec.get('custom'):
        return custom_boat(spec['custom'])
    return BOATS.get(spec.get('boat_id') or '') or BOATS[DEFAULT_BOAT]


def _limits_of(w: watch.Watch) -> Limits:
    lim = dict(w.limits or {})
    return Limits(
        max_wind=float(lim.get('max_wind', 20)),
        max_wave=float(lim.get('max_wave', 1.5)),
        date_from=w.date_from, date_to=w.date_to,
        day_start=int(lim.get('day_start', 7)),
        day_end=int(lim.get('day_end', 20)),
        night_ok=bool(lim.get('night_ok', False)),
        use_motor=bool(lim.get('use_motor', True)))


def in_reach(w: watch.Watch) -> bool:
    """Er prognosen overhovedet nået frem til brugerens vindue?"""
    start, end = w.window
    today = date.today()
    if end < today:
        return False
    horizon = today.toordinal() + MAX_FORECAST_DAYS - 1
    return start.toordinal() <= horizon


def good_enough(plan, quality: str) -> bool:
    """Er det et vindue, der er værd at skrive om?"""
    if plan.incomplete or plan.arrived_late or plan.red_hours:
        return False
    if quality == 'god':
        return plan.verdict == GO and not plan.yellow_hours
    return plan.verdict in (GO, WARN)


async def check(w: watch.Watch) -> dict | None:
    """Regn vagtens tur igennem. Giv det bedste vindue tilbage, hvis der er et."""
    if not in_reach(w):
        return None

    try:
        points = [Waypoint(float(d['lat']), float(d['lon']),
                           str(d.get('name') or 'Punkt'),
                           str(d.get('detail') or ''))
                  for d in w.waypoints]
    except (KeyError, TypeError, ValueError):
        return None
    if len(points) < 2:
        return None

    legs = plan_route([(p.lat, p.lon) for p in points])
    route = Route(points, [list(x.points) for x in legs],
                  [x.exact for x in legs])

    wx = await fetch_weather(route)
    boat = _boat_of(w.boat)
    limits = _limits_of(w)

    from . import harbours
    plans = find_windows(boat, route, wx, limits, harbours.stopovers(route))
    for plan in plans:
        if not good_enough(plan, w.quality):
            continue
        # Kan man ikke komme hjem igen, er det ikke en gevinst.
        home = weatherbound.look_ahead(
            plan, series_at(wx, route.total_nm, route.total_nm),
            limits, points[-1].name)
        if home is not None and home.matters:
            continue
        return {'plan': plan, 'route': route, 'boat': boat}
    return None


# ── Beskeden ──────────────────────────────────────────────────────────────────
def _link(path: str) -> str:
    return f'{settings.site_url}{path}'


async def tell(w: watch.Watch, hit: dict) -> bool:
    """Skriv til brugeren, at vejret er der."""
    plan, route = hit['plan'], hit['route']
    code = share.encode_route(route.waypoints, w.boat.get('boat_id') or '')
    open_url = _link(f'/?rute={code}')
    stop_url = _link(f'/vagt/stop/{w.id}')

    hello = f'Hej {w.name}' if w.name else 'Hej'
    stops = (f'\nUndervejs ligger du i {", ".join(s.name for s in plan.stops)}.'
             if plan.stops else '')

    text = f"""{hello}

Nu er der vejr til {w.title}.

Afgang     {full(plan.depart)}
Ankomst    {full(plan.arrival)}
Distance   {_da(plan.total_nm, 0)} sømil
Under vejs {_da(plan.under_way_h, 0)} timer, snit {_da(plan.avg_speed_kn)} knob
Vind       op til {_da(plan.worst_wind_kn, 0)} knob
Bølger     op til {_da(plan.worst_wave_m)} meter{stops}

Åbn turen i Sejlplan, så kan du se hele planen — dag for dag, stræk for stræk
og time for time:
{open_url}

Prognosen kan nå at flytte sig. Se den efter igen dagen før, du kaster los.

Vagten er hermed brugt. Vil du holde øje med en ny tur, så læg en ny vagt.
Vil du stoppe den her med det samme: {stop_url}

God tur.
Sejlplan
"""
    return await mailer.send(
        w.email, f'Nu er der vejr til {w.title}', text)


def _da(value: float, decimals: int = 1) -> str:
    """Dansk talformat — kun på tallene.

    Første udgave af den her mail lavede komma om til punktum i hele teksten
    bagefter. Det gjorde også adresserne om, så linket i mailen pegede
    ingensteder. Tallene formateres, hvor de skrives.
    """
    return f'{value:.{decimals}f}'.replace('.', ',')


async def confirm_mail(w: watch.Watch) -> bool:
    """Bed brugeren bekræfte sin adresse. Uden det skriver vi ikke igen."""
    yes_url = _link(f'/vagt/ja/{w.id}')
    stop_url = _link(f'/vagt/stop/{w.id}')
    hello = f'Hej {w.name}' if w.name else 'Hej'
    start, end = w.window

    text = f"""{hello}

Du har bedt Sejlplan holde øje med vejret til {w.title}
mellem {start.strftime('%d.%m.%Y')} og {end.strftime('%d.%m.%Y')}.

Bekræft, at adressen er din, så går vagten i gang:
{yes_url}

Vi skriver én gang — når der er et vindue, du kan sejle i. Ikke oftere.

Var det ikke dig, skal du ingenting gøre. Så bliver vagten aldrig aktiv, og
den ryger af sig selv. Vil du være sikker: {stop_url}

Sejlplan
"""
    return await mailer.send(
        w.email, f'Bekræft vejrvagt: {w.title}', text)


# ── Selve udkiggen ────────────────────────────────────────────────────────────
async def sweep_once() -> int:
    """Kig alle vagter igennem én gang. Giv antallet af sendte beskeder."""
    sent = 0
    for w in watch.pending():
        try:
            hit = await check(w)
        except Exception as exc:      # noqa: BLE001
            report(exc, f'vejrvagt {w.id}')
            continue
        if not hit:
            continue
        if await tell(w, hit):
            watch.mark_notified(w.id)
            sent += 1
    watch.sweep()
    return sent


async def run() -> None:
    """Baggrundsopgaven. Kører så længe serveren gør."""
    await asyncio.sleep(WARMUP_S)
    while True:
        try:
            sent = await sweep_once()
            if sent:
                print(f'[vejrvagt] {datetime.now():%H:%M} — {sent} besked(er)')
        except Exception as exc:      # noqa: BLE001
            report(exc, 'vejrvagten')
        await asyncio.sleep(INTERVAL_S)


def start() -> None:
    """Sæt udkiggen i gang, hvis der er noget at kigge med."""
    if not settings.watch_available:
        return
    asyncio.create_task(run())
