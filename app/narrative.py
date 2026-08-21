"""Skriver sejlplanen ud i klar tekst.

Alt herinde er regnet ud af prognosen — ingen AI involveret. Det er den plan,
man kan tage med ombord, også når der ikke er nøgle på serveren eller net på
telefonen.

Sejlbåd og motorbåd fortælles ikke ens. For en sejlbåd handler turen om vinden:
hvilken sejlføring, hvilken halse, hvornår der skal rebes. For en motorbåd
handler den om søen: hvor meget farten falder, hvor hårdt det banker, og hvor
mange liter der går i det. Teksten følger båden.
"""
from __future__ import annotations

import math
from collections import Counter
from dataclasses import dataclass

from . import harbours
from .boats import PLANING, Boat
from .dates import clock, day, day_time, duration, full, spell
from .sailing import (CALM, GO, HEAD, STOP, WARN, Limits, Plan, Route,
                      beaufort, compass, haversine, point_of_sail, tack)


def num(value: float, decimals: int = 1) -> str:
    """Dansk talformat — komma som decimaltegn."""
    return f'{value:.{decimals}f}'.replace('.', ',')


def plural(n: int, one: str, many: str) -> str:
    return f'{n} {one if n == 1 else many}'


# ── Vendepunkter ──────────────────────────────────────────────────────────────
# Ord man ikke siger, når man peger på et sted på søkortet. "Ud for Køge" er
# hvad en skipper siger; "ud for Køge Marina" er hvad en database siger.
_HARBOUR_WORDS = ('lystbådehavn', 'bådehavn', 'marina', 'sejlklub', 'havn',
                  'baadelaug', 'bådelaug', 'hamn', 'hafen', 'sportshafen')

TURN_NAME_NM = 12.0   # længere væk end det siger stedet ikke noget


def short_name(name: str) -> str:
    """Havnens navn skåret ned til det, stedet hedder."""
    out = name
    for word in _HARBOUR_WORDS:
        low = out.lower()
        if low.endswith(' ' + word):
            out = out[:-(len(word) + 1)]
    return out.strip(' -–,') or name


def place_name(lat: float, lon: float) -> str:
    """Det nærmeste sted, en skipper ville pege på."""
    near = harbours.nearest(lat, lon, 1)
    if near and haversine(lat, lon, near[0].lat, near[0].lon) <= TURN_NAME_NM:
        return f'ud for {short_name(near[0].name)}'
    return 'vendepunktet'


# ── Stræk for stræk ───────────────────────────────────────────────────────────
@dataclass
class StretchBrief:
    """Ét stræk med én kurs — dét man styrer efter, indtil man skal vende."""
    number: int
    frm: str
    to: str
    course: int
    distance_nm: float
    hours: float
    wind_min: float
    wind_max: float
    wind_from: str
    wave_max: float
    sea: str
    sail: str
    tack: str
    speed_min: float
    speed_max: float
    # Hvor stor en del af strækket der går for motor, som en andel mellem 0 og 1.
    # Det stod før som et antal timer, talt op blandt de sejltimer der faldt
    # inden for strækket — og så kunne der stå "3 af timerne for motor" på et
    # stræk, der varede to. Andelen kan ikke komme i modstrid med varigheden.
    motor_share: float
    status: str
    starts: str
    ends: str
    is_motor: bool

    @property
    def headline(self) -> str:
        # Er begge ender det samme sted, siger pilen ingenting. Så lad være.
        head = self.frm if self.frm == self.to else f'{self.frm} → {self.to}'
        return f'{self.number}. {head[0].upper()}{head[1:]}'

    @property
    def heading(self) -> str:
        return f'kurs {self.course}° {compass(self.course)}'

    @property
    def sentence(self) -> str:
        # Kursen står som mærkat på kortet, så den gentages ikke her.
        parts = [f'{num(self.distance_nm)} sømil, {spell(self.hours)} undervejs.']

        if round(self.wind_min) == round(self.wind_max):
            parts.append(f'Vinden står {num(self.wind_max, 0)} knob fra {self.wind_from}.')
        else:
            parts.append(f'Vinden står {num(self.wind_min, 0)}–{num(self.wind_max, 0)} '
                         f'knob fra {self.wind_from}.')

        if self.is_motor:
            if self.speed_min < self.speed_max - 0.5:
                parts.append(f'Farten svinger mellem {num(self.speed_min)} og '
                             f'{num(self.speed_max)} knob.')
            else:
                parts.append(f'Der holdes {num(self.speed_max)} knob.')
        elif self.motor_share > 0.6:
            # Står motoren på det meste af strækket, er sejlføringen ikke det,
            # der beskriver turen. Så er det motorsejlads.
            parts.append('Der er for lidt vind til at sejle strækket — '
                         'motoren må trække det meste af vejen.')
        elif self.sail == 'i vindøjet':
            parts.append('Kursen ligger så tæt på vinden, at strækket skal krydses.')
        else:
            parts.append(f'Det sejles for {self.sail} på {self.tack}.')

        if self.wave_max >= 0.1:
            where = f' i {self.sea}' if self.sea != CALM else ''
            parts.append(f'Bølger op til {num(self.wave_max)} meter{where}.')
        if not self.is_motor and 0 < self.motor_share <= 0.6:
            parts.append(f'{spell(self.hours * self.motor_share)} af det for motor.')
        return ' '.join(parts)


def _trace(plan: Plan) -> list[tuple[float, object]]:
    """(sømil, klokkeslæt) hen ad ruten — sporet båden lagde."""
    rows = [(s.along_nm, s.time) for s in plan.segments]
    rows.append((plan.total_nm, plan.arrival))
    return rows


def _passed(trace: list, along: float):
    """Hvornår båden passerede et punkt. Springes der en nat over, tages kanten."""
    if along <= trace[0][0]:
        return trace[0][1]
    for (a1, t1), (a2, t2) in zip(trace, trace[1:]):
        if a1 <= along <= a2:
            span, gap = a2 - a1, (t2 - t1).total_seconds() / 3600
            if span <= 0 or gap > 2:      # her ligger en overnatning
                return t1 if along - a1 < a2 - along else t2
            return t1 + (t2 - t1) * ((along - a1) / span)
    return trace[-1][1]


def _sailing_hours(trace: list, start: float, end: float) -> float:
    """Timer med fart i mellem to punkter — havnetimer tæller ikke med."""
    total = 0.0
    for (a1, t1), (a2, t2) in zip(trace, trace[1:]):
        lo, hi = max(a1, start), min(a2, end)
        if hi <= lo:
            continue
        gap = (t2 - t1).total_seconds() / 3600
        span = a2 - a1
        if gap > 2 or span <= 0:
            continue
        total += gap * (hi - lo) / span
    return total


def stretch_briefs(route: Route, plan: Plan, boat: Boat) -> list[StretchBrief]:
    """Turen delt op dér, hvor kursen skifter — ikke dér, hvor man satte et kryds.

    Sætter man Køge og Præstø ind, er det ét ben, men det sejles mod sydøst, så
    mod syd og til sidst mod vest. Planen skal gælde for de stræk, man faktisk
    styrer, så det er dem, der beskrives.
    """
    stretches = route.stretches()
    if not stretches or not plan.segments:
        return []

    trace = _trace(plan)
    briefs = []
    for st in stretches:
        rows = [s for s in plan.segments
                if st.start_nm - 0.01 <= s.along_nm < st.end_nm - 0.01]
        if not rows:
            # Et kort stræk kan ligge helt inde i én sejltime. Så låner vi den
            # time, båden var i, da den passerede — tallene gælder stadig.
            rows = [min(plan.segments, key=lambda s: abs(s.along_nm - st.middle_nm))]

        first = route.waypoints[st.leg]
        last = route.waypoints[st.leg + 1] if st.leg + 1 < len(route.waypoints) else first
        at_start = route.at(st.start_nm)
        at_end = route.at(st.end_nm)

        starts_leg = st.number == 1 or stretches[st.number - 2].leg != st.leg
        ends_leg = (st.number == len(stretches)
                    or stretches[st.number].leg != st.leg)

        winds = [s.wind_kn for s in rows]
        speeds = [s.speed_kn for s in rows]
        seas = Counter(s.sea for s in rows if s.sea != CALM)
        twa = sum(s.twa for s in rows) / len(rows)

        briefs.append(StretchBrief(
            number=st.number,
            frm=first.name if starts_leg else place_name(at_start[0], at_start[1]),
            to=last.name if ends_leg else place_name(at_end[0], at_end[1]),
            course=round(st.course),
            distance_nm=st.distance_nm,
            hours=max(_sailing_hours(trace, st.start_nm, st.end_nm), 1 / 60),
            wind_min=min(winds), wind_max=max(winds),
            wind_from=Counter(compass(s.wind_dir) for s in rows).most_common(1)[0][0],
            wave_max=max(s.wave_m for s in rows),
            sea=seas.most_common(1)[0][0] if seas else CALM,
            sail=point_of_sail(twa),
            tack=Counter(tack(s.course, s.wind_dir) for s in rows).most_common(1)[0][0],
            speed_min=min(speeds), speed_max=max(speeds),
            motor_share=sum(1 for s in rows if s.motoring) / len(rows),
            status=(STOP if any(s.status == STOP for s in rows)
                    else WARN if any(s.status == WARN for s in rows) else GO),
            starts=day_time(_passed(trace, st.start_nm)),
            ends=day_time(_passed(trace, st.end_nm)),
            is_motor=boat.is_motor,
        ))
    return briefs


# ── Hvordan turen føles ───────────────────────────────────────────────────────
# ── Hvad turen ser ud til at blive, før vejret er hentet ──────────────────────
# Ruten kender vi med det samme; vejret tager tid at hente. I mellemtiden kan vi
# godt sige noget nyttigt: hvor langt, hvor længe ved almindelig vind, og om det
# overhovedet kan nås inden for ét sejldøgn. Det er dét, der gør at man ved hvad
# man beder om, før man trykker og venter.
TYPICAL_TWA = 90      # halvvind – hverken det bedste eller det værste
TYPICAL_TWS = 10      # jævn vind


def estimate(boat: Boat, route: Route, limits: Limits) -> tuple[str, int]:
    """Overslag over turen. Returnerer (tekst, antal sejldøgn det kræver)."""
    from .sailing import polar_speed

    speed = (boat.cruise_kn if boat.is_motor
             else polar_speed(boat, TYPICAL_TWA, TYPICAL_TWS))
    speed = max(1.0, speed)
    hours = route.total_nm / speed
    days = max(1, math.ceil(hours / limits.day_hours))

    where = 'ved marchfart' if boat.is_motor else 'i jævn vind'
    text = f'{num(route.total_nm)} sømil · ca. {spell(hours)} {where}'
    return text, days


def days_note(days: int, limits: Limits) -> str:
    """Én linje om hvad antallet af sejldøgn betyder for turen."""
    if days <= 1:
        return f'Kan nås inden for ét sejldøgn ({limits.day_start:02d}–{limits.day_end:02d}).'
    nights = plural(days - 1, 'overnatning', 'overnatninger')
    return (f'Kræver {days} sejldøgn — altså {nights} undervejs, '
            f'medmindre du slår mørkesejlads til.')


# ── Hvordan turen føles ───────────────────────────────────────────────────────
def ride(boat: Boat, plan: Plan) -> str:
    """Én sætning om, hvordan turen kommer til at føles ombord."""
    rows = plan.segments
    if not rows:
        return ''

    head = sum(1 for s in rows if s.sea == HEAD)
    calm = sum(1 for s in rows if s.sea == CALM)
    worst_felt = max(s.felt_m for s in rows)
    lost = _speed_loss(boat, plan)

    if not boat.is_motor:
        if calm > len(rows) * 0.7:
            return 'Der er næsten ingen sø. Det bliver en behagelig tur.'
        if head > len(rows) * 0.5 and worst_felt > 1.0:
            return ('Søen kommer ind forfra det meste af vejen. Båden stamper, '
                    'og der bliver vådt på fordækket — hold godt fast under skiftene.')
        if worst_felt > 1.2:
            return ('Der er sø nok til at man mærker den. Sørg for at alt er '
                    'surret, og at kabyssen kan bruges med én hånd.')
        return 'Søen er til at leve med, og turen bør være behagelig.'

    # Motorbåd: farten er det, søen tager fra dig.
    speed = f'Marchfarten er {num(boat.cruise_kn, 0)} knob'
    if lost >= 3:
        speed += (f', men søen tager omkring {num(lost, 0)} knob af den — '
                  f'du kommer frem med {num(plan.avg_speed_kn)} i snit')
    else:
        speed += f', og den kan holdes stort set hele vejen ({num(plan.avg_speed_kn)} i snit)'

    if calm > len(rows) * 0.7:
        feel = 'Vandet er så småt, at turen bliver stille og hurtig.'
    elif head > len(rows) * 0.4 and worst_felt > 0.8:
        feel = ('Søen står ind forfra. Det banker i skroget, og det bliver en '
                'tur, hvor man tager farten af og sætter den på igen.'
                if boat.hull == PLANING else
                'Søen står ind forfra. Der er stampen i det, men båden bliver ved.')
    elif worst_felt > 0.8:
        feel = 'Søen kommer skråt ind. Regn med rulning — sørg for at alt står fast.'
    else:
        feel = 'Der er lidt sø, men ikke nok til at det bliver ubehageligt.'

    fuel = (f' Der går omkring {num(plan.fuel_l, 0)} liter brændstof på turen.'
            if plan.fuel_l >= 5 else '')
    return f'{speed}. {feel}{fuel}'


def _speed_loss(boat: Boat, plan: Plan) -> float:
    if not boat.is_motor or not plan.segments:
        return 0.0
    return max(0.0, boat.cruise_kn - plan.avg_speed_kn)


# ── Overblik ──────────────────────────────────────────────────────────────────
def overview(boat: Boat, route: Route, plan: Plan) -> list[str]:
    """To-tre afsnit der fortæller, hvad turen går ud på."""
    names = ' → '.join(w.name for w in route.waypoints)
    legs = len(route.waypoints) - 1

    opening = (f'Ruten {names} er på {num(plan.total_nm)} sømil fordelt på '
               f'{plural(legs, "ben", "ben")}. Med {boat.name} tager den beregnet '
               f'{duration(plan.hours)} med fart i. Du kaster los {full(plan.depart)} '
               f'og er fremme {full(plan.arrival)}')
    if plan.stops:
        nights = plural(plan.nights, 'overnatning', 'overnatninger')
        stops = ', '.join(s.name for s in plan.stops)
        opening += f' — med {nights} undervejs i {stops}.'
    else:
        opening += ' i én stræk.'

    paragraphs = [opening]

    rows = plan.segments
    winds = [s.wind_kn for s in rows]
    first_dir, last_dir = compass(rows[0].wind_dir), compass(rows[-1].wind_dir)

    wind_text = (f'Vinden ligger mellem {num(min(winds), 0)} og {num(max(winds), 0)} knob '
                 f'({beaufort(max(winds))} på det kraftigste)')
    wind_text += (f' og drejer fra {first_dir} til {last_dir} undervejs.'
                  if first_dir != last_dir else f' fra {first_dir} hele vejen.')

    if boat.is_motor:
        middle = wind_text
    else:
        sails = Counter(point_of_sail(s.twa) for s in rows)
        dominant = sails.most_common(1)[0][0]
        middle = wind_text + (
            ' Store dele af turen ligger i vindøjet og skal krydses.'
            if dominant == 'i vindøjet' else f' Det meste sejles for {dominant}.')

    if plan.worst_wave_m >= 0.1:
        middle += f' Bølgerne når op på {num(plan.worst_wave_m)} meter.'
    else:
        middle += ' Der er ingen nævneværdig søgang i prognosen.'

    paragraphs.append(middle)

    feel = ride(boat, plan)
    if feel:
        paragraphs.append(feel)

    practical = []
    if plan.motor_hours and not boat.is_motor:
        practical.append(f'{plan.motor_hours} af timerne er så vindsvage, '
                         f'at motoren må hjælpe')
    if plan.night_hours:
        practical.append(f'{plan.night_hours} timer ligger uden for dit sejldøgn')
    gusts = max(s.gust_kn for s in rows)
    if gusts > plan.worst_wind_kn + 5:
        practical.append(f'vindstødene går op til {num(gusts, 0)} knob, '
                         f'altså noget over middelvinden')
    if practical:
        text = ', '.join(practical)
        paragraphs.append(text[0].upper() + text[1:] + '.')

    return paragraphs


# ── Dag for dag ───────────────────────────────────────────────────────────────
def day_lines(plan: Plan) -> list[str]:
    """Turen sat op som de sejldøgn, den falder i."""
    out = []
    for i, d in enumerate(plan.days, start=1):
        out.append(f'Dag {i} · {day(d.date, short=False)}: {d.frm} → {d.to}, '
                   f'{num(d.nm)} sømil, {clock(d.depart)}–{clock(d.arrive)} '
                   f'({duration(d.hours)} med fart i).')
    return out


# ── Advarsler ─────────────────────────────────────────────────────────────────
def warnings(plan: Plan, limits: Limits, boat: Boat) -> list[str]:
    """Det skipperen skal tage stilling til, før der kastes los."""
    out = []

    if plan.incomplete:
        out.append('Turen når ikke frem inden for den vejrudsigt, vi har. '
                   'Del den op, eller planlæg den sidste del senere.')

    for stop in plan.stops:
        if stop.late:
            out.append(
                f'Du er først fortøjet i {stop.name} kl. {clock(stop.arrive)} — '
                f'efter dit sejldøgn, der slutter {limits.day_end}:00. Der var '
                f'ingen havn tættere på, du kunne nå. Overvej at afgå tidligere, '
                f'eller at lægge et stop ind før.')

    if plan.stops and not any(s.late for s in plan.stops):
        first = plan.stops[0]
        out.append(
            f'Turen kan ikke sejles inden for ét sejldøgn. Planen lægger '
            f'{plural(plan.nights, "overnatning", "overnatninger")} ind — '
            f'første gang i {first.name} kl. {clock(first.arrive)}. '
            f'Vil du hele vejen i én stræk, skal du slå mørkesejlads til.')

    early = [s for s in plan.stops
             if (s.arrive.replace(hour=limits.day_end, minute=0)
                 - s.arrive).total_seconds() > 3 * 3600]
    if early:
        first = early[0]
        out.append(
            f'Du ligger fortøjet i {first.name} allerede kl. {clock(first.arrive)}, '
            f'og der er timer tilbage af dagen. Det er med vilje: næste stræk er '
            f'for langt til at nås inden kl. {limits.day_end:02d}:00, og der er '
            f'ingen havn imellem. Sejler du videre nu, ender du i mørke.')

    if plan.red_hours:
        worst = [s for s in plan.segments if s.status == STOP]
        out.append(
            f'{plan.red_hours} timer ligger over dine grænser — fra '
            f'{day_time(worst[0].time)}. Der er op til {num(max(s.wind_kn for s in worst), 0)} '
            f'knob og {num(max(s.wave_m for s in worst))} meter bølger. '
            f'Overvej at udskyde eller søge havn undervejs.')
    elif plan.yellow_hours:
        out.append(
            f'{plan.yellow_hours} timer nærmer sig dine grænser '
            f'({num(limits.max_wind, 0)} knob og {num(limits.max_wave)} meter). '
            f'{"Sæt farten ned i tide" if boat.is_motor else "Reb i god tid"}, '
            f'og hold øje med om prognosen flytter sig.')

    if plan.night_hours:
        night = [s for s in plan.segments if s.night]
        out.append(
            f'{plan.night_hours} timer sejles uden for sejldøgnet, første gang '
            f'omkring {clock(night[0].time)}. Sørg for lanterner, vagtplan og at '
            f'besætningen er udhvilet.')

    gusts = max((s.gust_kn for s in plan.segments), default=0)
    if gusts >= limits.max_wind:
        out.append(f'Vindstødene når {num(gusts, 0)} knob. Middelvinden holder sig '
                   f'lavere, men {"farten" if boat.is_motor else "rebningen"} skal '
                   f'passe til stødene, ikke til middelværdien.')

    if boat.is_motor and plan.fuel_l:
        out.append(f'Regn med omkring {num(plan.fuel_l, 0)} liter brændstof. '
                   f'Læg en fjerdedel oveni til reserve og til at ligge og vente.')

    longest = max((d.hours for d in plan.days), default=0)
    if longest >= 14:
        out.append(f'Den længste dag er på {duration(longest)} i træk. Aftal '
                   f'hvem der styrer hvornår, og hvor I kan afbryde undervejs.')

    if not out:
        out.append('Prognosen holder sig inden for dine grænser hele vejen, og du '
                   'er i havn inden sejldøgnet er omme. Det ser ud til at blive en god tur.')
    return out


# ── Hele planen ───────────────────────────────────────────────────────────────
def as_text(boat: Boat, route: Route, plan: Plan, limits: Limits) -> str:
    """Hele planen som ren tekst — til udklipsholderen eller en mail til gasten."""
    lines = [
        f'SEJLPLAN — {" → ".join(w.name for w in route.waypoints)}',
        '=' * 60,
        '',
        f'Båd:      {boat.name} ({boat.kind}, {num(boat.length_m)} m)',
        f'Afgang:   {full(plan.depart)}',
        f'Ankomst:  {full(plan.arrival)}',
        f'Distance: {num(plan.total_nm)} sømil',
        f'Varighed: {duration(plan.hours)} med fart i · '
        f'snitfart {num(plan.avg_speed_kn)} knob',
    ]
    if boat.is_motor:
        lines.append(f'Brændstof: ca. {num(plan.fuel_l, 0)} liter')
    if plan.stops:
        lines.append(f'Ophold:   {", ".join(s.name for s in plan.stops)}')

    lines += ['', 'OVERBLIK', '-' * 60]
    lines += overview(boat, route, plan)

    if len(plan.days) > 1:
        lines += ['', 'DAG FOR DAG', '-' * 60]
        lines += day_lines(plan)

    lines += ['', 'VÆR OPMÆRKSOM PÅ', '-' * 60]
    lines += [f'- {w}' for w in warnings(plan, limits, boat)]

    lines += ['', 'STRÆK FOR STRÆK', '-' * 60]
    for brief in stretch_briefs(route, plan, boat):
        lines += [f'{brief.headline}  ({brief.starts} → {brief.ends})',
                  f'  {brief.sentence}', '']

    lines += ['TIME FOR TIME', '-' * 60,
              'Tid            Vind        Bølger  Fart   Sejlføring']
    for s in plan.segments:
        mode = 'motor' if s.motoring else point_of_sail(s.twa)
        lines.append(
            f'{day_time(s.time):<14} {num(s.wind_kn, 0):>2} kn {compass(s.wind_dir):<4} '
            f'{num(s.wave_m):>5} m {num(s.speed_kn):>5} kn  {mode}')

    lines += ['', 'Prognoser er prognoser. Planen erstatter ikke søkort, '
                  'farvandsudsigt eller almindelig sømandskab.']
    return '\n'.join(lines)
