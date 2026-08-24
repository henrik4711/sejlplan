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
from datetime import date
from dataclasses import dataclass

from . import harbours
from .boats import PLANING, Boat
from .i18n import plural, t, t_in_sentence
from .dates import clock, day, day_time, duration, full, spell
from .sailing import (CALM, GO, HEAD, STOP, WARN, Limits, Plan, Route,
                      beaufort, compass, haversine, point_of_sail, tack)


def num(value: float, decimals: int = 1) -> str:
    """Dansk talformat — komma som decimaltegn."""
    return f'{value:.{decimals}f}'.replace('.', ',')


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
        return t('ud for {sted}', sted=short_name(near[0].name))
    return t('vendepunktet')


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
    # Havnen, hvis strækket bliver brudt af en overnatning. Uden den stod der
    # "6,1 sømil, 1 t undervejs" over et tidsrum på et døgn, og læseren måtte
    # selv gætte, at natten lå indeni.
    night: str = ''

    @property
    def headline(self) -> str:
        # Er begge ender det samme sted, siger pilen ingenting. Så lad være.
        head = self.frm if self.frm == self.to else f'{self.frm} → {self.to}'
        return f'{self.number}. {head[0].upper()}{head[1:]}'

    @property
    def heading(self) -> str:
        return t('kurs {grader}° {retning}', grader=self.course,
                 retning=compass(self.course))

    @property
    def sentence(self) -> str:
        # Kursen står som mærkat på kortet, så den gentages ikke her.
        parts = [t('{sm} sømil, {tid} undervejs.',
                   sm=num(self.distance_nm), tid=spell(self.hours))]

        if round(self.wind_min) == round(self.wind_max):
            parts.append(t('Vinden står {kn} knob fra {retning}.',
                           kn=num(self.wind_max, 0), retning=self.wind_from))
        else:
            parts.append(t('Vinden står {fra}–{til} knob fra {retning}.',
                           fra=num(self.wind_min, 0),
                           til=num(self.wind_max, 0), retning=self.wind_from))

        if self.is_motor:
            if self.speed_min < self.speed_max - 0.5:
                parts.append(t('Farten svinger mellem {fra} og {til} knob.',
                               fra=num(self.speed_min),
                               til=num(self.speed_max)))
            else:
                parts.append(t('Der holdes {kn} knob.',
                               kn=num(self.speed_max)))
        elif self.motor_share > 0.6:
            # Står motoren på det meste af strækket, er sejlføringen ikke det,
            # der beskriver turen. Så er det motorsejlads.
            parts.append(t('Der er for lidt vind til at sejle strækket — '
                           'motoren må trække det meste af vejen.'))
        elif self.sail == 'i vindøjet':
            parts.append(t('Kursen ligger så tæt på vinden, at strækket skal '
                           'krydses.'))
        else:
            parts.append(t('Det sejles for {sejlføring} på {halse}.',
                           sejlføring=t_in_sentence(self.sail),
                           halse=t(self.tack)))

        if self.wave_max >= 0.1:
            # To hele sætninger frem for en indskudt bisætning: tysk bøjer
            # "i modsø" efter køn, og det kan ikke limes sammen af stumper.
            parts.append(
                t('Bølger op til {m} meter.', m=num(self.wave_max))
                if self.sea == CALM else
                t('Bølger op til {m} meter i {sø}.', m=num(self.wave_max),
                  sø=t(self.sea)))
        if not self.is_motor and 0 < self.motor_share <= 0.6:
            parts.append(t('{tid} af det for motor.',
                           tid=spell(self.hours * self.motor_share)))
        if self.night:
            parts.append(t('Strækket brydes af natten i {havn} — timerne dér '
                           'er ikke talt med.', havn=self.night))
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


def _night_in(trace: list, plan: Plan, start: float, end: float) -> str:
    """Havnen, hvis der ligger en overnatning inde i strækket.

    Et hul i sporet, hvor tiden går uden at sømilene gør, er en nat ved kaj.
    Hvilken havn det var, findes ved at se, hvilket ophold der begynder dér.
    """
    for (a1, t1), (a2, t2) in zip(trace, trace[1:]):
        if (t2 - t1).total_seconds() / 3600 <= 2:
            continue
        # Natten hører til dét stræk, hvor døgnet sluttede. Hullet i sporet
        # strækker sig over kanten mellem to stræk, og uden det her stod den
        # samme nat på dem begge.
        if not start - 0.01 <= a1 < end - 0.01:
            continue
        if not plan.stops:
            return ''
        near = min(plan.stops, key=lambda s: abs((s.arrive - t1).total_seconds()))
        return near.name
    return ''


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
            night=_night_in(trace, plan, st.start_nm, st.end_nm),
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

    where = t('ved marchfart') if boat.is_motor else t('i jævn vind')
    text = t('{sm} sømil · ca. {tid} {hvordan}', sm=num(route.total_nm),
             tid=spell(hours), hvordan=where)
    return text, days


def days_note(days: int, limits: Limits) -> str:
    """Én linje om hvad antallet af sejldøgn betyder for turen."""
    if days <= 1:
        return t('Kan nås inden for ét sejldøgn ({fra}–{til}).',
                 fra=f'{limits.day_start:02d}', til=f'{limits.day_end:02d}')
    nights = plural(days - 1, 'overnatning', 'overnatninger')
    return t('Kræver {sejldøgn} — altså {overnatninger} undervejs, medmindre '
             'du slår mørkesejlads til.',
             sejldøgn=plural(days, 'sejldøgn', 'sejldøgn'),
             overnatninger=nights)


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
            return t('Der er næsten ingen sø. Det bliver en behagelig tur.')
        if head > len(rows) * 0.5 and worst_felt > 1.0:
            return t('Søen kommer ind forfra det meste af vejen. Båden '
                     'stamper, og der bliver vådt på fordækket — hold godt '
                     'fast under skiftene.')
        if worst_felt > 1.2:
            return t('Der er sø nok til at man mærker den. Sørg for at alt er '
                     'surret, og at kabyssen kan bruges med én hånd.')
        return t('Søen er til at leve med, og turen bør være behagelig.')

    # Motorbåd: farten er det, søen tager fra dig.
    if lost >= 3:
        speed = t('Marchfarten er {kn} knob, men søen tager omkring {tab} '
                  'knob af den — du kommer frem med {snit} i snit',
                  kn=num(boat.cruise_kn, 0), tab=num(lost, 0),
                  snit=num(plan.avg_speed_kn))
    else:
        speed = t('Marchfarten er {kn} knob, og den kan holdes stort set hele '
                  'vejen ({snit} i snit)', kn=num(boat.cruise_kn, 0),
                  snit=num(plan.avg_speed_kn))

    if calm > len(rows) * 0.7:
        feel = t('Vandet er så småt, at turen bliver stille og hurtig.')
    elif head > len(rows) * 0.4 and worst_felt > 0.8:
        feel = (t('Søen står ind forfra. Det banker i skroget, og det bliver '
                  'en tur, hvor man tager farten af og sætter den på igen.')
                if boat.hull == PLANING else
                t('Søen står ind forfra. Der er stampen i det, men båden '
                  'bliver ved.'))
    elif worst_felt > 0.8:
        feel = t('Søen kommer skråt ind. Regn med rulning — sørg for at alt '
                 'står fast.')
    else:
        feel = t('Der er lidt sø, men ikke nok til at det bliver ubehageligt.')

    fuel = (' ' + t('Der går omkring {liter} liter brændstof på turen.',
                    liter=num(plan.fuel_l, 0)) if plan.fuel_l >= 5 else '')
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

    head = t('Ruten {navne} er på {sm} sømil fordelt på {ben}. ',
             navne=names, sm=num(plan.total_nm),
             ben=plural(legs, 'ben', 'ben'))
    if plan.incomplete:
        # Planen rakte ikke hele vejen. Så hører timetallet til dét, den nåede
        # — ikke til hele ruten — og der er ingen ankomst at melde.
        opening = head + t(
            'Vejrudsigten rækker ikke hele vejen. Kaster du los {afgang}, når '
            'du {nået} sømil på {tid} under vejs med {båd}, før prognosen '
            'slipper op {slut}',
            afgang=full(plan.depart), nået=num(plan.reached_nm),
            tid=spell(plan.under_way_h), båd=boat.name,
            slut=full(plan.arrival))
    else:
        opening = head + t(
            'Med {båd} tager den beregnet {tid} under vejs. Du kaster los '
            '{afgang} og er fremme {ankomst}',
            båd=boat.name, tid=spell(plan.under_way_h),
            afgang=full(plan.depart), ankomst=full(plan.arrival))
    if plan.stops:
        nights = plural(plan.nights, 'overnatning', 'overnatninger')
        stops = ', '.join(s.name for s in plan.stops)
        opening += t(' — med {overnatninger} undervejs i {havne}.',
                     overnatninger=nights, havne=stops)
    else:
        opening += '.' if plan.incomplete else t(' i én stræk.')

    paragraphs = [opening]

    rows = plan.segments
    winds = [s.wind_kn for s in rows]
    first_dir, last_dir = compass(rows[0].wind_dir), compass(rows[-1].wind_dir)

    wind_text = t('Vinden ligger mellem {fra} og {til} knob ({styrke} på det '
                  'kraftigste)', fra=num(min(winds), 0),
                  til=num(max(winds), 0), styrke=beaufort(max(winds)))
    wind_text += (t(' og drejer fra {fra} til {til} undervejs.',
                    fra=first_dir, til=last_dir)
                  if first_dir != last_dir
                  else t(' fra {retning} hele vejen.', retning=first_dir))

    if boat.is_motor:
        middle = wind_text
    else:
        sails = Counter(point_of_sail(s.twa) for s in rows)
        dominant = sails.most_common(1)[0][0]
        middle = wind_text + (
            t(' Store dele af turen ligger i vindøjet og skal krydses.')
            if dominant == 'i vindøjet'
            else t(' Det meste sejles for {sejlføring}.',
                   sejlføring=t_in_sentence(dominant)))

    if plan.worst_wave_m >= 0.1:
        middle += t(' Bølgerne når op på {m} meter.',
                    m=num(plan.worst_wave_m))
    else:
        middle += t(' Der er ingen nævneværdig søgang i prognosen.')

    paragraphs.append(middle)

    feel = ride(boat, plan)
    if feel:
        paragraphs.append(feel)

    practical = []
    if plan.motor_hours and not boat.is_motor:
        practical.append(t('{n} af timerne er så vindsvage, at motoren må '
                           'hjælpe', n=plan.motor_hours))
    if plan.night_hours:
        practical.append(t('{n} timer ligger uden for dit sejldøgn',
                           n=plan.night_hours))
    gusts = max(s.gust_kn for s in rows)
    if gusts > plan.worst_wind_kn + 5:
        practical.append(t('vindstødene går op til {kn} knob, altså noget '
                           'over middelvinden', kn=num(gusts, 0)))
    if practical:
        text = ', '.join(practical)
        paragraphs.append(text[0].upper() + text[1:] + '.')

    return paragraphs


# ── Dag for dag ───────────────────────────────────────────────────────────────
def day_lines(plan: Plan) -> list[str]:
    """Turen sat op som de sejldøgn, den falder i."""
    out = []
    for i, d in enumerate(plan.days, start=1):
        out.append(t('Dag {nr} · {dato}: {fra} → {til}, {sm} sømil, '
                     '{afgang}–{ankomst} ({tid} under vejs).',
                     nr=i, dato=day(d.date, short=False), fra=d.frm, til=d.to,
                     sm=num(d.nm), afgang=clock(d.depart),
                     ankomst=clock(d.arrive), tid=spell(d.under_way_h)))
    return out


def _weatherbound(o) -> str:
    """Sig det rent: du kommer ikke væk igen med det samme.

    Det er den besked, der ændrer en plan — og den, ingen opdager selv, fordi
    man kigger på vejret frem til man er fremme, ikke bagefter.
    """
    days = plural(o.stuck_days, 'sejldøgn', 'sejldøgn')
    if o.worst_wave_m >= 0.3:
        head = t('Du bliver formentlig blæst inde i {sted}. Efter ankomsten '
                 'viser prognosen {døgn} i træk uden et vindue, du kan sejle '
                 'i — op til {kn} knobs vind og {m} meter sø. ',
                 sted=o.place, døgn=days, kn=num(o.worst_wind_kn, 0),
                 m=num(o.worst_wave_m))
    else:
        head = t('Du bliver formentlig blæst inde i {sted}. Efter ankomsten '
                 'viser prognosen {døgn} i træk uden et vindue, du kan sejle '
                 'i — op til {kn} knobs vind. ',
                 sted=o.place, døgn=days, kn=num(o.worst_wind_kn, 0))

    if o.runs_out:
        return head + t(
            'Og det holder ikke op, før prognosen gør: den rækker til {dato}, '
            'og der blæser det stadig. Regn med at ligge stille, til vejret '
            'vender, og læg hjemturen som en tur for sig.',
            dato=day(o.checked_to, short=False))
    return head + t(
        'Først {tidspunkt} er der noget at sejle i igen. Skal du på arbejde '
        'inden da, så vælg en anden afgang — eller en havn, du kommer hjem '
        'fra.', tidspunkt=full(o.next_window))


# ── Advarsler ─────────────────────────────────────────────────────────────────
# Tre niveauer, fordi de ikke er lige meget. "Du kommer ikke hjem igen" og
# "husk lanterner" stod før med det samme ikon i den samme farve, og så holder
# man op med at læse dem. Nu kan man se på tegnet, hvad der haster.
NOTE_STOP, NOTE_WARN, NOTE_INFO, NOTE_GOOD = 'stop', 'warn', 'info', 'good'

NOTE_ICON = {NOTE_STOP: 'report', NOTE_WARN: 'warning_amber',
             NOTE_INFO: 'info', NOTE_GOOD: 'check_circle'}
NOTE_TONE = {NOTE_STOP: 'var(--stop)', NOTE_WARN: 'var(--warn)',
             NOTE_INFO: 'var(--txt-3)', NOTE_GOOD: 'var(--go)'}


@dataclass(frozen=True)
class Note:
    """Én ting at tage stilling til, og hvor meget den haster."""
    level: str
    text: str

    def __str__(self) -> str:      # så gammel kode, der bare vil have teksten
        return self.text           # stadig virker

# Fra og med her ude regnes en vejrudsigt for en tendens. De første tre-fire
# døgn holder ret godt; derefter er det retningen, der overlever, ikke timerne.
UNCERTAIN_AFTER_DAYS = 5
def warnings(plan: Plan, limits: Limits, boat: Boat,
             outlook=None) -> list[Note]:
    """Det skipperen skal tage stilling til, før der kastes los.

    `outlook` er, hvad prognosen siger om dagene *efter* ankomsten. Den står
    forrest, for det er den, der afgør, om turen overhovedet skal lægges nu.
    """
    out = []

    if outlook is not None and outlook.matters:
        out.append(Note(NOTE_STOP, _weatherbound(outlook)))

    # Hvor langt ude i prognosen slutter turen? En vejrudsigt på ni døgn er
    # ikke samme vare som en på to. Vinden kan ligge anderledes, og timerne kan
    # rykke — og det skal stå der, ikke gemmes i en disclaimer.
    ahead = (plan.arrival.date() - date.today()).days
    if ahead >= UNCERTAIN_AFTER_DAYS and not plan.incomplete:
        out.append(Note(NOTE_INFO, t(
            'Turen slutter {døgn} ude i prognosen. Så langt frem er en '
            'vejrudsigt en tendens, ikke en tidsplan: retningen holder tit, '
            'men styrken og timerne rykker sig. Læg planen, og se den efter '
            'igen et par dage før afgang.',
            døgn=plural(ahead, 'døgn', 'døgn'))))

    if plan.incomplete:
        rest = max(0.0, plan.total_nm - plan.reached_nm)
        out.append(Note(NOTE_STOP, t(
            'Turen når ikke frem inden for den vejrudsigt, vi har. Du kommer '
            '{nået} af {ialt} sømil — de sidste {rest} sømil kan først '
            'planlægges, når prognosen rækker så langt. Læg turen tidligere, '
            'eller planlæg den sidste del om nogle dage.',
            nået=num(plan.reached_nm), ialt=num(plan.total_nm),
            rest=num(rest))))

    for stop in plan.stops:
        if stop.late:
            out.append(Note(NOTE_STOP, t(
                'Du er først fortøjet i {havn} kl. {tid} — efter dit '
                'sejldøgn, der slutter {slut}:00. Der var ingen havn tættere '
                'på, du kunne nå. Overvej at afgå tidligere, eller at lægge '
                'et stop ind før.',
                havn=stop.name, tid=clock(stop.arrive), slut=limits.day_end)))

    if plan.stops and not any(s.late for s in plan.stops):
        first = plan.stops[0]
        out.append(Note(NOTE_INFO, t(
            'Turen kan ikke sejles inden for ét sejldøgn. Planen lægger '
            '{overnatninger} ind — første gang i {havn} kl. {tid}. Vil du '
            'hele vejen i én stræk, skal du slå mørkesejlads til.',
            overnatninger=plural(plan.nights, 'overnatning', 'overnatninger'),
            havn=first.name, tid=clock(first.arrive))))

    early = [s for s in plan.stops
             if (s.arrive.replace(hour=limits.day_end, minute=0)
                 - s.arrive).total_seconds() > 3 * 3600]
    if early:
        first = early[0]
        out.append(Note(NOTE_INFO, t(
            'Du ligger fortøjet i {havn} allerede kl. {tid}, og der er timer '
            'tilbage af dagen. Det er med vilje: næste stræk er for langt til '
            'at nås inden kl. {slut}:00, og der er ingen havn imellem. Sejler '
            'du videre nu, ender du i mørke.',
            havn=first.name, tid=clock(first.arrive),
            slut=f'{limits.day_end:02d}')))

    if plan.red_hours:
        worst = [s for s in plan.segments if s.status == STOP]
        out.append(Note(NOTE_STOP, t(
            '{n} timer ligger over dine grænser — fra {hvornår}. Der er op '
            'til {kn} knob og {m} meter bølger. Overvej at udskyde eller søge '
            'havn undervejs.',
            n=plan.red_hours, hvornår=day_time(worst[0].time),
            kn=num(max(s.wind_kn for s in worst), 0),
            m=num(max(s.wave_m for s in worst)))))
    elif plan.yellow_hours:
        out.append(Note(NOTE_WARN, t(
            '{n} timer nærmer sig dine grænser ({kn} knob og {m} meter). '
            '{råd}, og hold øje med om prognosen flytter sig.',
            n=plan.yellow_hours, kn=num(limits.max_wind, 0),
            m=num(limits.max_wave),
            råd=t('Sæt farten ned i tide') if boat.is_motor
            else t('Reb i god tid'))))

    if plan.night_hours:
        night = [s for s in plan.segments if s.night]
        out.append(Note(NOTE_WARN, t(
            '{n} timer sejles uden for sejldøgnet, første gang omkring {tid}. '
            'Sørg for lanterner, vagtplan og at besætningen er udhvilet.',
            n=plan.night_hours, tid=clock(night[0].time))))

    gusts = max((s.gust_kn for s in plan.segments), default=0)
    if gusts >= limits.max_wind:
        out.append(Note(NOTE_WARN, t(
            'Vindstødene når {kn} knob. Middelvinden holder sig lavere, men '
            '{hvad} skal passe til stødene, ikke til middelværdien.',
            kn=num(gusts, 0),
            hvad=t('farten') if boat.is_motor else t('rebningen'))))

    if boat.is_motor and plan.fuel_l:
        out.append(Note(NOTE_INFO, t(
            'Regn med omkring {liter} liter brændstof. Læg en fjerdedel '
            'oveni til reserve og til at ligge og vente.',
            liter=num(plan.fuel_l, 0))))

    longest = max((d.hours for d in plan.days), default=0)
    if longest >= 14:
        out.append(Note(NOTE_WARN, t(
            'Den længste dag er på {tid} i træk. Aftal hvem der styrer '
            'hvornår, og hvor I kan afbryde undervejs.',
            tid=duration(longest))))

    if not out:
        out.append(Note(NOTE_GOOD, t(
            'Prognosen holder sig inden for dine grænser hele vejen, og du er '
            'i havn inden sejldøgnet er omme. Det ser ud til at blive en god '
            'tur.')))
    return out


# ── Hele planen ───────────────────────────────────────────────────────────────
def as_text(boat: Boat, route: Route, plan: Plan, limits: Limits) -> str:
    """Hele planen som ren tekst — til udklipsholderen eller en mail til gasten."""
    # Rubrikkerne sættes op i en kolonne. Den tyske "Ankunft:" er ikke lige så
    # lang som den danske "Ankomst:", så bredden regnes ud af de ord, der
    # faktisk står der — ellers står tallene i takker.
    navne = [t('Båd'), t('Afgang'), t('Ankomst'), t('Distance'),
             t('Varighed'), t('Brændstof'), t('Ophold')]
    bred = max(len(n) for n in navne) + 1
    baad, afgang, ankomst, distance, varighed, braendstof, ophold = navne

    def rubrik(navn: str, værdi: str) -> str:
        return f'{navn + ":":<{bred}} {værdi}'

    lines = [
        f'{t("SEJLPLAN")} — {" → ".join(w.name for w in route.waypoints)}',
        '=' * 60,
        '',
        rubrik(baad, f'{boat.name} ({t(boat.kind)}, {num(boat.length_m)} m)'),
        rubrik(afgang, full(plan.depart)),
        rubrik(ankomst, full(plan.arrival)),
        rubrik(distance, t('{sm} sømil', sm=num(plan.total_nm))),
        rubrik(varighed, t('{tid} under vejs · snitfart {kn} knob',
                           tid=spell(plan.under_way_h),
                           kn=num(plan.avg_speed_kn))),
    ]
    if boat.is_motor:
        lines.append(rubrik(braendstof,
                            t('ca. {liter} liter', liter=num(plan.fuel_l, 0))))
    if plan.stops:
        lines.append(rubrik(ophold, ', '.join(s.name for s in plan.stops)))

    lines += ['', t('OVERBLIK'), '-' * 60]
    lines += overview(boat, route, plan)

    if len(plan.days) > 1:
        lines += ['', t('DAG FOR DAG'), '-' * 60]
        lines += day_lines(plan)

    lines += ['', t('VÆR OPMÆRKSOM PÅ'), '-' * 60]
    lines += [f'- {w}' for w in warnings(plan, limits, boat)]

    lines += ['', t('STRÆK FOR STRÆK'), '-' * 60]
    for brief in stretch_briefs(route, plan, boat):
        lines += [f'{brief.headline}  ({brief.starts} → {brief.ends})',
                  f'  {brief.sentence}', '']

    # Overskriften sættes op efter de samme bredder som rækkerne nedenfor.
    # Skrevet i hånden passede den kun til de danske ord, og på tysk stod
    # tallene under den forkerte overskrift.
    lines += [t('TIME FOR TIME'), '-' * 60,
              f'{t("Tid"):<15}{t("Vind"):<11}{t("Bølger"):<8}'
              f'{t("Fart"):<10}{t("Sejlføring")}']
    kn, m = t('kn'), t('m')
    for s in plan.segments:
        mode = t('motor') if s.motoring else t(point_of_sail(s.twa))
        lines.append(
            f'{day_time(s.time):<15}'
            f'{num(s.wind_kn, 0):>2} {kn} {compass(s.wind_dir):<4}'
            f'{num(s.wave_m):>5} {m}  '
            f'{num(s.speed_kn):>5} {kn}  {mode}')

    lines += ['', t('Prognoser er prognoser. Planen erstatter ikke søkort, '
                    'farvandsudsigt eller almindelig sømandskab.')]
    return chr(10).join(lines)
