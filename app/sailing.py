"""Navigation, fart og selve gennemsejlingen af en tur.

Rene funktioner uden UI- eller netværksafhængigheder, så de kan testes isoleret
og køres i en baggrundstråd.

Det bærende begreb er **sejldøgnet**. Siger man, at man vil være i havn senest
kl. 20, er det ikke et ønske om at afgå senest kl. 20 — det er et krav om at
ligge fortøjet kl. 20. Rækker turen ikke, skal den deles, og så skal der findes
en havn undervejs at overnatte i. Derfor sejler `sail()` turen igennem dag for
dag: den sejler, til dagen er omme, finder den havn man kan nå, lægger til, og
tager fat igen næste morgen.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta

from .boats import SEA_DRAG, SLOWEST, Boat

NM_PER_RADIAN = 3440.065  # jordens radius i sømil

# Under denne fart giver det ikke længere mening at ligge og sejle: motoren
# tændes. Sat lavt med vilje – man motorsejler ikke for at vinde en halv knob.
MOTOR_THRESHOLD_KN = 3.0

# Loft på hvor lang en tur der overhovedet regnes igennem.
MAX_SAIL_HOURS = 24 * 8

# ── Statusniveauer for en sejltime ────────────────────────────────────────────
GO, WARN, STOP = 'go', 'warn', 'stop'

STATUS_LABEL = {GO: 'God', WARN: 'Skærpet', STOP: 'Frarådes'}
STATUS_COLOR = {GO: '#27AE60', WARN: '#E67E22', STOP: '#E74C3C'}

_COMPASS = ['N', 'NNØ', 'NØ', 'ØNØ', 'Ø', 'ØSØ', 'SØ', 'SSØ',
            'S', 'SSV', 'SV', 'VSV', 'V', 'VNV', 'NV', 'NNV']

_BEAUFORT = [(1, 'Stille'), (4, 'Svag vind'), (7, 'Let vind'), (11, 'Let brise'),
             (17, 'Jævn vind'), (22, 'Frisk vind'), (28, 'Kuling'), (34, 'Hård kuling'),
             (41, 'Stormende kuling'), (48, 'Storm')]

# Søen ind fra siden føles mildere end lige i stævnen, og medsø mildest af alt.
HEAD, BEAM, FOLLOWING = 'modsø', 'tværsø', 'medsø'
CALM = 'smult vande'

_SEA_WEIGHT = {HEAD: 1.15, BEAM: 0.85, FOLLOWING: 0.55, CALM: 0.0}


# ── Geometri ──────────────────────────────────────────────────────────────────
def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Storcirkelafstand i sømil."""
    r = math.radians
    a = (math.sin(r(lat2 - lat1) / 2) ** 2
         + math.cos(r(lat1)) * math.cos(r(lat2)) * math.sin(r(lon2 - lon1) / 2) ** 2)
    return 2 * NM_PER_RADIAN * math.asin(math.sqrt(min(1.0, a)))


def bearing(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Retvisende kurs i grader (0-360)."""
    r = math.radians
    dl = r(lon2 - lon1)
    x = math.sin(dl) * math.cos(r(lat2))
    y = math.cos(r(lat1)) * math.sin(r(lat2)) - math.sin(r(lat1)) * math.cos(r(lat2)) * math.cos(dl)
    return (math.degrees(math.atan2(x, y)) + 360) % 360


def true_wind_angle(course: float, wind_dir: float) -> float:
    """Vindens vinkel ind på båden. 0° = lige i stævnen, 180° = agten ind."""
    return abs(((course - wind_dir + 180) % 360) - 180)


def compass(deg: float) -> str:
    return _COMPASS[round(deg / 22.5) % 16]


def point_of_sail(twa: float) -> str:
    """Sejlstillingen ved en given vindvinkel — det skipperen mærker på båden."""
    if twa < 35:
        return 'i vindøjet'
    if twa < 55:
        return 'skarp bidevind'
    if twa < 80:
        return 'bidevind'
    if twa < 100:
        return 'halvvind'
    if twa < 150:
        return 'rumskøds'
    return 'læns'


def tack(course: float, wind_dir: float) -> str:
    """Hvilken halse man ligger på — altså hvilken side vinden kommer ind fra."""
    relative = (wind_dir - course + 360) % 360
    if relative < 5 or relative > 355:
        return 'lige forfra'
    if relative < 175:
        return 'styrbords halse'
    if relative > 185:
        return 'bagbords halse'
    return 'lige agterfra'


def beaufort(knots: float) -> str:
    for limit, label in _BEAUFORT:
        if knots < limit:
            return label
    return 'Orkan'


def sea_direction(course: float, wave_dir: float, wave_m: float) -> str:
    """Hvor søen kommer fra i forhold til kursen. Det er dét, turen føles efter."""
    if wave_m < 0.2:
        return CALM
    angle = true_wind_angle(course, wave_dir)
    if angle < 60:
        return HEAD
    if angle < 120:
        return BEAM
    return FOLLOWING


def felt_wave(wave_m: float, sea: str) -> float:
    """Den bølgehøjde, turen føles som — søens retning vejet ind."""
    return wave_m * _SEA_WEIGHT.get(sea, 1.0)


# ── Ruten ─────────────────────────────────────────────────────────────────────
@dataclass
class Waypoint:
    lat: float
    lon: float
    name: str
    # Hvor stedet ligger, sagt som en sejler ville sige det: "Køge Bugt",
    # "Det Sydfynske Øhav". Punktet er valgt på navn, ikke på koordinater, så
    # det er farvandet man vil mindes om — ikke decimalgraderne.
    detail: str = ''

    @property
    def where(self) -> str:
        """Undertekst til listen. Koordinater kun når der ikke er andet."""
        return self.detail or f'{self.lat:.3f}°N {self.lon:.3f}°Ø'

    def as_dict(self) -> dict:
        return {'lat': self.lat, 'lon': self.lon, 'name': self.name,
                'detail': self.detail}

    @staticmethod
    def from_dict(d: dict) -> 'Waypoint':
        return Waypoint(float(d['lat']), float(d['lon']),
                        str(d.get('name') or 'Waypoint'), str(d.get('detail') or ''))


@dataclass
class Step:
    """Et lige stykke af ruten: samme kurs hele vejen."""
    lat: float
    lon: float
    to_lat: float
    to_lon: float
    course: float
    distance_nm: float
    leg: int          # 0-baseret benindeks
    start_nm: float   # hvor langt inde i ruten stykket begynder


@dataclass
class Stretch:
    """Et stræk med én kurs: dét man styrer efter, indtil man skal vende."""
    number: int
    leg: int
    course: float
    distance_nm: float
    start_nm: float
    end_nm: float

    @property
    def middle_nm(self) -> float:
        return (self.start_nm + self.end_nm) / 2


def _merge_short(stretches: list['Stretch'], min_nm: float) -> list['Stretch']:
    """Læg de korte stræk ind i naboen. Kortest først, så de ikke hober sig op."""
    out = list(stretches)
    while len(out) > 1:
        i = min(range(len(out)), key=lambda k: out[k].distance_nm)
        if out[i].distance_nm >= min_nm:
            break
        before = out[i - 1] if i > 0 and out[i - 1].leg == out[i].leg else None
        after = out[i + 1] if i + 1 < len(out) and out[i + 1].leg == out[i].leg else None
        host = before or after
        if host is None:
            break
        def off(other: 'Stretch') -> float:
            return abs(((other.course - out[i].course + 180) % 360) - 180)

        if before and after:
            host = before if off(before) <= off(after) else after
        if off(host) > 90:
            break   # naboen går den anden vej; så er det korte stræk et rigtigt sving
        host.course = _mean_course(host.course, host.distance_nm,
                                   out[i].course, out[i].distance_nm)
        host.distance_nm += out[i].distance_nm
        host.start_nm = min(host.start_nm, out[i].start_nm)
        host.end_nm = max(host.end_nm, out[i].end_nm)
        out.pop(i)

    for number, stretch in enumerate(out, start=1):
        stretch.number = number
    return out


def _mean_course(a: float, wa: float, b: float, wb: float) -> float:
    """Vægtet middelkurs. Regnet over enhedscirklen, så 350° og 10° giver 0°."""
    x = math.cos(math.radians(a)) * wa + math.cos(math.radians(b)) * wb
    y = math.sin(math.radians(a)) * wa + math.sin(math.radians(b)) * wb
    return (math.degrees(math.atan2(y, x)) + 360) % 360


@dataclass
class Route:
    """Brugerens punkter og den streg, der faktisk sejles imellem dem."""

    waypoints: list[Waypoint]
    tracks: list[list[tuple[float, float]]] = field(default_factory=list)
    exact: list[bool] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.tracks:
            self.tracks = [[(a.lat, a.lon), (b.lat, b.lon)]
                           for a, b in zip(self.waypoints, self.waypoints[1:])]
        if not self.exact:
            self.exact = [True] * len(self.tracks)
        self.steps = self._steps()
        self.total_nm = round(sum(s.distance_nm for s in self.steps), 1)

    def _steps(self) -> list[Step]:
        out, along = [], 0.0
        for leg, track in enumerate(self.tracks):
            for (la, lo), (lb, lob) in zip(track, track[1:]):
                d = haversine(la, lo, lb, lob)
                if d < 1e-6:
                    continue
                out.append(Step(la, lo, lb, lob, bearing(la, lo, lb, lob), d, leg, along))
                along += d
        return out

    @property
    def ok(self) -> bool:
        """Er hele ruten efterprøvet fri af land?"""
        return all(self.exact)

    def leg_nm(self, leg: int) -> float:
        return round(sum(s.distance_nm for s in self.steps if s.leg == leg), 1)

    def stretches(self, turn_deg: float = 18.0, min_nm: float = 2.0) -> list['Stretch']:
        """Ruten delt op dér, hvor kursen reelt skifter.

        Brugerens ben siger kun hvor han vil hen. En tur fra Køge til Præstø er
        ét ben, men den sejles mod øst, så mod syd, så mod vest — og det er de
        stræk, planen skal gælde for. Vi lægger derfor de lige stykker sammen,
        så længe kursen holder sig inden for `turn_deg`, og bryder når den ikke
        gør. Stykker under `min_nm` er en krusning på kysten, ikke et kursskift,
        og lægges ind i det foregående stræk.
        """
        out: list[Stretch] = []
        for step in self.steps:
            last = out[-1] if out else None
            same_leg = last is not None and last.leg == step.leg
            turned = last is None or not same_leg or                 abs(((step.course - last.course + 180) % 360) - 180) > turn_deg
            if turned and (last is None or last.distance_nm >= min_nm or not same_leg):
                out.append(Stretch(len(out) + 1, step.leg, step.course,
                                   step.distance_nm, step.start_nm,
                                   step.start_nm + step.distance_nm))
                continue

            # Samme retning: forlæng strækket og vægt kursen efter afstanden.
            total = last.distance_nm + step.distance_nm
            last.course = _mean_course(last.course, last.distance_nm,
                                       step.course, step.distance_nm)
            last.distance_nm = total
            last.end_nm = step.start_nm + step.distance_nm

        return _merge_short(out, min_nm)

    def at(self, along_nm: float) -> tuple[float, float, float, int]:
        """Position, kurs og benindeks efter `along_nm` sømils sejlads."""
        if not self.steps:
            wp = self.waypoints[0]
            return wp.lat, wp.lon, 0.0, 0
        for s in self.steps:
            if along_nm <= s.start_nm + s.distance_nm or s is self.steps[-1]:
                t = max(0.0, min(1.0, (along_nm - s.start_nm) / s.distance_nm))
                return (s.lat + (s.to_lat - s.lat) * t,
                        s.lon + (s.to_lon - s.lon) * t,
                        s.course, s.leg)
        s = self.steps[-1]
        return s.to_lat, s.to_lon, s.course, s.leg


# ── Fart ──────────────────────────────────────────────────────────────────────
def polar_speed(boat: Boat, twa: float, tws: float) -> float:
    """Bådfart fra polardiagrammet, bilineært interpoleret på vinkel og vindstyrke."""
    if boat.is_motor or not boat.polar:
        return boat.motor_speed_kn

    angles = sorted(boat.polar)
    twa = max(angles[0], min(angles[-1], twa))
    tws = max(0.0, min(25.0, tws))

    lo_a = max((a for a in angles if a <= twa), default=angles[0])
    hi_a = min((a for a in angles if a >= twa), default=angles[-1])

    def at_angle(angle: int) -> float:
        row = boat.polar[angle]
        speeds = sorted(row)
        lo_w = max((w for w in speeds if w <= tws), default=speeds[0])
        hi_w = min((w for w in speeds if w >= tws), default=speeds[-1])
        if lo_w == hi_w:
            return row[lo_w]
        t = (tws - lo_w) / (hi_w - lo_w)
        return row[lo_w] + (row[hi_w] - row[lo_w]) * t

    s_lo = at_angle(lo_a)
    if lo_a == hi_a:
        return s_lo
    s_hi = at_angle(hi_a)
    return s_lo + (s_hi - s_lo) * (twa - lo_a) / (hi_a - lo_a)


def motor_speed(boat: Boat, wave_m: float, sea: str) -> float:
    """Motorbådens fart i den sø, der er.

    Farten falder med kvadratet på den bølgehøjde, man rent faktisk mærker.
    En planende båd taber mest — den kan ikke holde sig oppe at plane i en
    stejl modsø og må ned i fortrængning. Under en tredjedel af marchfarten
    går man ikke; så sætter man sig til rette og sejler skrogfart.
    """
    cruise = boat.cruise_kn or boat.motor_speed_kn
    felt = felt_wave(wave_m, sea)
    if felt <= 0.05:
        return cruise

    slowed = cruise / (1.0 + SEA_DRAG.get(boat.hull, 0.4) * felt * felt)
    return max(slowed, min(cruise, max(boat.hull_speed_kn * 0.85, cruise * SLOWEST)))


def wave_penalty(speed: float, wave_m: float, sea: str) -> float:
    """Bølger koster fart for en sejlbåd. Aldrig mere end 70 %."""
    felt = felt_wave(wave_m, sea)
    if felt < 0.35:
        return speed
    loss = 0.10 * (felt - 0.35) + 0.10 * max(0.0, felt - 1.0)
    return max(speed * (1 - min(0.7, loss * 2)), speed * 0.3)


def status_of(wind_kn: float, felt_m: float, max_wind: float, max_wave: float) -> str:
    if wind_kn <= max_wind and felt_m <= max_wave:
        return GO
    if wind_kn <= max_wind * 1.2 and felt_m <= max_wave * 1.3:
        return WARN
    return STOP


# ── Grænser ───────────────────────────────────────────────────────────────────
@dataclass
class Limits:
    """Brugerens komfortgrænser og sejldøgn."""

    max_wind: float = 20.0
    max_wave: float = 1.5
    date_from: str = ''
    date_to: str = ''
    day_start: int = 7      # tidligst ud af havn
    day_end: int = 20       # senest fortøjet igen
    night_ok: bool = False  # må turen sejles videre i mørke?
    use_motor: bool = True

    @property
    def day_hours(self) -> int:
        return max(1, self.day_end - self.day_start)


# ── Turen ─────────────────────────────────────────────────────────────────────
@dataclass
class Segment:
    """Én sejltime."""
    time: datetime
    leg: int
    along_nm: float
    lat: float
    lon: float
    course: int
    twa: int
    wind_kn: float
    wind_dir: int
    gust_kn: float
    wave_m: float
    sea: str
    felt_m: float
    speed_kn: float
    status: str
    motoring: bool
    night: bool


@dataclass
class Stop:
    """En overnatning undervejs."""
    name: str
    detail: str
    lat: float
    lon: float
    arrive: datetime
    depart: datetime
    detour_nm: float
    late: bool = False      # kunne ikke nås inden for sejldøgnet

    @property
    def hours_ashore(self) -> float:
        return (self.depart - self.arrive).total_seconds() / 3600


@dataclass
class Day:
    """Ét sejldøgn: fra kaj til kaj."""
    date: date
    frm: str
    to: str
    depart: datetime
    arrive: datetime
    nm: float
    hours: int
    red_hours: int
    yellow_hours: int
    night_hours: int


@dataclass
class Plan:
    """Resultatet af at afgå på et bestemt tidspunkt."""
    depart: datetime
    arrival: datetime
    total_nm: float
    hours: int              # timer med fart i
    avg_speed_kn: float
    worst_wind_kn: float
    worst_wave_m: float
    red_hours: int
    yellow_hours: int
    night_hours: int
    motor_hours: int
    fuel_l: float
    score: float = 0.0
    segments: list[Segment] = field(default_factory=list)
    stops: list[Stop] = field(default_factory=list)
    days: list[Day] = field(default_factory=list)
    incomplete: bool = False    # nåede ikke frem inden for prognosen
    arrived_late: bool = False  # fremme, men efter sejldøgnet var omme

    @property
    def verdict(self) -> str:
        if self.red_hours:
            return STOP
        if self.yellow_hours:
            return WARN
        return GO

    @property
    def nights(self) -> int:
        return len(self.stops)

    @property
    def elapsed_hours(self) -> float:
        return (self.arrival - self.depart).total_seconds() / 3600

    @property
    def late_arrival(self) -> bool:
        return self.arrived_late or any(s.late for s in self.stops)

    @property
    def one_day(self) -> bool:
        return not self.stops


# ── Gennemsejlingen ───────────────────────────────────────────────────────────
def _nearest(series: list[dict], t: datetime) -> dict:
    """Nærmeste timeprognose. Serien er sorteret, så indekset kan regnes direkte."""
    if not series:
        return {'wind_kn': 0.0, 'wind_dir': 0.0, 'wave_m': 0.0,
                'gust_kn': 0.0, 'wave_dir': 0.0}
    idx = round((t - series[0]['time']).total_seconds() / 3600)
    return series[max(0, min(len(series) - 1, idx))]


def _day_end(t: datetime, limits: Limits) -> datetime:
    """Hvornår sejldøgnet, `t` hører til, lukker."""
    end = t.replace(hour=limits.day_end, minute=0, second=0, microsecond=0)
    return end if t < end else end + timedelta(days=1)


def _is_night(t: datetime, limits: Limits) -> bool:
    """Mørkesejlads: uden for sejldøgnet. Groft, men det er dét man mærker."""
    return not (limits.day_start <= t.hour < limits.day_end)


def _hour(boat: Boat, route: Route, along: float, t: datetime,
          weather: list, limits: Limits) -> Segment:
    """Regn én sejltime igennem fra positionen `along` sømil inde i ruten."""
    from .weather import series_at
    lat, lon, course, leg = route.at(along)
    wx = _nearest(series_at(weather, along, route.total_nm), t)
    wind, wdir = wx['wind_kn'], wx['wind_dir']
    wave, gust = wx['wave_m'], wx['gust_kn']
    wdir_wave = wx.get('wave_dir') or wdir

    sea = sea_direction(course, wdir_wave, wave)
    felt = felt_wave(wave, sea)
    twa = true_wind_angle(course, wdir)

    if boat.is_motor:
        speed = motor_speed(boat, wave, sea)
        motoring = True
    else:
        speed = wave_penalty(polar_speed(boat, twa, wind), wave, sea)
        # Hård vind koster fart: reb, styrtsøer, mindre effektiv sejlføring.
        if wind > limits.max_wind:
            speed *= max(0.4, 1 - (wind - limits.max_wind) * 0.05)
        motoring = False
        if limits.use_motor and speed < MOTOR_THRESHOLD_KN:
            speed, motoring = boat.motor_speed_kn, True

    return Segment(
        time=t, leg=leg + 1, along_nm=along, lat=lat, lon=lon,
        course=round(course), twa=round(twa),
        wind_kn=round(wind, 1), wind_dir=round(wdir), gust_kn=round(gust, 1),
        wave_m=round(wave, 2), sea=sea, felt_m=round(felt, 2),
        speed_kn=round(max(speed, 0.5), 1),
        status=status_of(wind, felt, limits.max_wind, limits.max_wave),
        motoring=motoring, night=_is_night(t, limits),
    )


def _harbour_for_night(stopovers: list, reached: list[tuple[float, datetime]],
                       along_now: float, deadline: datetime, speed_kn: float,
                       floor_nm: float = 0.0,
                       ceiling_nm: float = float('inf')) -> tuple | None:
    """Den havn, man kommer længst med og stadig kan nå inden dagen er omme.

    `reached` er dagens (sømil, klokkeslæt)-spor, så vi kan slå op, hvornår
    båden passerede et givet punkt på ruten. Afstikkeren ind til havnen lægges
    oveni med den fart, båden holdt.

    `floor_nm` holder os fra at foreslå en havn, man allerede lå i i morges, og
    `ceiling_nm` fra at kalde selve destinationen for en overnatning.
    """
    best, best_along = None, -1.0
    fallback, fallback_time = None, None

    for h, along_h, detour_nm in stopovers:
        if along_h > along_now + 0.1 or not (floor_nm <= along_h <= ceiling_nm):
            continue
        passed = _time_at(reached, along_h)
        if passed is None:
            continue
        arrive = passed + timedelta(hours=detour_nm / max(2.0, speed_kn))
        if arrive <= deadline:
            if along_h > best_along:
                best, best_along = (h, along_h, detour_nm, arrive, False), along_h
        elif fallback_time is None or arrive < fallback_time:
            fallback, fallback_time = (h, along_h, detour_nm, arrive, True), arrive

    return best or fallback


def _time_at(reached: list[tuple[float, datetime]], along: float) -> datetime | None:
    """Interpolér, hvornår båden passerede et bestemt punkt på ruten."""
    if not reached or along < reached[0][0] - 0.01:
        return None
    for (a1, t1), (a2, t2) in zip(reached, reached[1:]):
        if a1 - 0.01 <= along <= a2 + 0.01:
            span = a2 - a1
            f = 0.0 if span <= 0 else (along - a1) / span
            return t1 + (t2 - t1) * f
    return reached[-1][1]


def sail(boat: Boat, route: Route, depart: datetime,
         weather: list, limits: Limits,
         stopovers: list | None = None) -> Plan | None:
    """Sejl ruten igennem fra `depart`, dag for dag, med de ophold der skal til.

    `stopovers` er (havn, sømil inde i ruten, afstikker i sømil) — havne tæt nok
    på ruten til at kunne bruges som overnatning. Er listen tom, sejles der
    videre i mørket, og timerne bliver talt som mørketimer.
    """
    if len(route.waypoints) < 2 or not route.steps:
        return None

    stopovers = stopovers or []
    horizon = _forecast_end(weather)

    segments: list[Segment] = []
    stops: list[Stop] = []
    days: list[Day] = []

    along, t = 0.0, depart
    total = route.total_nm
    day_from = route.waypoints[0].name
    day_start_t, day_first = t, len(segments)
    reached: list[tuple[float, datetime]] = [(0.0, t)]
    incomplete = False

    day_from_nm = 0.0
    arrived_late = False
    deadline = _day_end(t, limits)

    while along < total - 0.01:
        if len(segments) >= MAX_SAIL_HOURS or (horizon and t > horizon):
            incomplete = True
            break

        seg = _hour(boat, route, along, t, weather, limits)
        segments.append(seg)
        along = min(total, along + seg.speed_kn)
        t += timedelta(hours=1)
        reached.append((along, t))

        home = along >= total - 0.01
        if limits.night_ok or t <= deadline or not stopovers:
            if home:
                break
            continue

        # Sejldøgnet er omme. Enten er vi slet ikke fremme, eller også er vi
        # først fremme efter lukketid — og så er svaret det samme: find en havn
        # på vejen at ligge i, og tag den sidste del i morgen.
        pick = _harbour_for_night(stopovers, reached, along, deadline, seg.speed_kn,
                                  floor_nm=day_from_nm + 1.0, ceiling_nm=total - 1.0)
        if pick is None:
            if home:
                arrived_late = True
                break
            continue    # ingen havn at gå i — så må natten sejles

        h, along_h, detour_nm, arrive, late = pick
        along = along_h
        next_out = (arrive + timedelta(days=1)).replace(
            hour=limits.day_start, minute=0, second=0, microsecond=0)
        if next_out <= arrive:
            next_out += timedelta(days=1)

        # Timerne efter ankomst hører ikke til turen.
        segments = [s for s in segments if s.time < arrive]
        stops.append(Stop(h.name, h.detail, h.lat, h.lon, arrive, next_out, detour_nm, late))
        days.append(_day(day_from, h.name, day_start_t, arrive,
                         along_h - day_from_nm + detour_nm, segments[day_first:]))

        day_from, day_start_t = h.name, next_out
        day_first, day_from_nm = len(segments), along_h
        deadline = _day_end(next_out, limits)
        # Ud af havnen igen koster den samme afstikker.
        t = next_out + timedelta(hours=detour_nm / max(2.0, seg.speed_kn))
        reached = [(along, t)]

    if not segments:
        return None

    days.append(_day(day_from, route.waypoints[-1].name, day_start_t, t,
                     max(0.0, along - day_from_nm), segments[day_first:]))

    hours = len(segments)
    fuel = sum(_fuel_for(boat, s) for s in segments)

    return Plan(
        depart=depart,
        arrival=t,
        total_nm=total,
        hours=hours,
        avg_speed_kn=round(total / hours, 1) if hours else 0.0,
        worst_wind_kn=round(max(s.wind_kn for s in segments), 1),
        worst_wave_m=round(max(s.wave_m for s in segments), 1),
        red_hours=sum(1 for s in segments if s.status == STOP),
        yellow_hours=sum(1 for s in segments if s.status == WARN),
        night_hours=sum(1 for s in segments if s.night),
        motor_hours=sum(1 for s in segments if s.motoring),
        fuel_l=round(fuel),
        segments=segments,
        stops=stops,
        days=days,
        incomplete=incomplete,
        arrived_late=arrived_late,
    )


def _fuel_for(boat: Boat, seg: Segment) -> float:
    """Brændstof for én time. Sejlbåde bruger kun noget, når motoren går."""
    if not seg.motoring:
        return 0.0
    if not boat.is_motor:
        return boat.fuel_lph
    # Forbruget følger farten: sætter søen båden ned, falder det også.
    cruise = boat.cruise_kn or boat.motor_speed_kn
    return boat.fuel_lph * min(1.0, (seg.speed_kn / cruise) ** 1.6 + 0.15)


def _day(frm: str, to: str, depart: datetime, arrive: datetime,
         nm: float, rows: list[Segment]) -> Day:
    return Day(
        date=depart.date(), frm=frm, to=to, depart=depart, arrive=arrive,
        nm=round(nm, 1), hours=len(rows),
        red_hours=sum(1 for s in rows if s.status == STOP),
        yellow_hours=sum(1 for s in rows if s.status == WARN),
        night_hours=sum(1 for s in rows if s.night),
    )


def _forecast_end(weather: list) -> datetime | None:
    ends = [rows[-1]['time'] for rows in weather if rows]
    return min(ends) if ends else None


# ── Rangering ─────────────────────────────────────────────────────────────────
def score(p: Plan, limits: Limits) -> float:
    """Lavere er bedre. Vægtene afspejler hvad der faktisk ødelægger en sejlads."""
    s = 0.0
    s += p.red_hours * 12                                    # timer man helst ikke vil sejle i
    s += p.yellow_hours * 2.5                                # ubehagelige, men til at klare
    s += max(0.0, p.worst_wind_kn - limits.max_wind) * 5     # hvor langt over grænsen toppen går
    s += max(0.0, p.worst_wave_m - limits.max_wave) * 8
    s += p.hours * 0.4                                       # kortere passage vinder ved lige vejr
    s += p.elapsed_hours * 0.08                              # og den der er hjemme først
    s += p.depart.hour * 0.1                                 # ved lige vejr: kast los om morgenen
    s += p.nights * 6                                        # en overnatning undervejs koster
    s += sum(st.detour_nm for st in p.stops) * 0.5           # og især en lang afstikker
    # Hver gang man ligger og leder efter kajen efter lukketid, tæller det.
    s += 25 * (sum(1 for st in p.stops if st.late) + bool(p.arrived_late))
    if not limits.night_ok:
        s += p.night_hours * 3
    if p.incomplete:
        s += 200                                             # nåede slet ikke frem
    return round(s, 2)


def find_windows(boat: Boat, route: Route, weather: list,
                 limits: Limits, stopovers: list | None = None,
                 max_results: int = 10) -> list[Plan]:
    """Prøv hver mulig afgangstime i vinduet og returnér de bedste, spredte forslag."""
    if len(route.waypoints) < 2:
        return []

    start = datetime.fromisoformat(limits.date_from).replace(
        hour=0, minute=0, second=0, microsecond=0)
    end = datetime.fromisoformat(limits.date_to).replace(
        hour=23, minute=0, second=0, microsecond=0)
    earliest = datetime.now().replace(minute=0, second=0, microsecond=0)

    candidates: list[Plan] = []
    cursor = start
    while cursor <= end:
        # Man kaster ikke los før dagen begynder, og heller ikke i går.
        # Der er ingen mening i en afgang en time før man skal ligge fortøjet.
        if (limits.day_start <= cursor.hour <= max(limits.day_start, limits.day_end - 2)
                and cursor >= earliest):
            p = sail(boat, route, cursor, weather, limits, stopovers)
            if p and p.hours:
                p.score = score(p, limits)
                candidates.append(p)
        cursor += timedelta(hours=1)

    candidates.sort(key=lambda p: p.score)

    # Undertryk næsten-identiske naboer, så listen viser reelt forskellige valg
    # i stedet for den samme formiddag klokken 08, 09, 10 og 11.
    chosen: list[Plan] = []
    for p in candidates:
        if all(abs((p.depart - c.depart).total_seconds()) >= 3 * 3600 for c in chosen):
            chosen.append(p)
        if len(chosen) >= max_results:
            break
    return chosen
