"""Både: hvor hurtigt de sejler, og hvor meget de kan holde til.

En sejlbåd beskrives af sit polardiagram — farten ved en given vindvinkel og
vindstyrke. En motorbåd har ikke noget polardiagram; den har en marchfart, og
det afgørende for både fart og komfort er søen, ikke vinden. De to slags både
regnes derfor forskelligt, og det er værd at være omhyggelig med: en planende
båd, der sejler 24 knob i smult vande, gør 10 i halvanden meters modsø, og
turen føles som at blive rystet i en spand.

`skrog` styrer, hvor hårdt søen går ud over farten:

    planende          mister mest — skroget skal op at plane, og det kan det
                      ikke i en stejl modsø
    halvplanende      taber jævnt, men bliver ved med at komme frem
    fortrængning      mærker søen mindst; farten er alligevel bundet af skroget
"""
from __future__ import annotations

from dataclasses import dataclass, field

SAIL, MOTOR = 'Sejlbåd', 'Motorbåd'

PLANING, SEMI, DISPLACEMENT = 'planende', 'halvplanende', 'fortrængning'

# Hvor hårdt søen tager på farten. Tallet går ind i 1/(1+k·bølge²), så en
# planende båd halverer farten i omkring en meters modsø.
SEA_DRAG = {PLANING: 0.95, SEMI: 0.5, DISPLACEMENT: 0.22}

# Under den her andel af marchfarten går man ikke — så sætter man sig til rette
# og sejler den fart, skroget kan bære.
SLOWEST = 0.32


@dataclass(frozen=True)
class Boat:
    id: str
    name: str
    icon: str
    kind: str                     # SAIL eller MOTOR
    length_m: float
    desc: str

    max_wind_kn: float            # komfortgrænse – foreslås når båden vælges
    max_wave_m: float

    hull_speed_kn: float = 7.0    # fartgrænse for et fortrængningsskrog
    motor_speed_kn: float = 5.5   # sejlbådens fart for motor
    fuel_lph: float = 3.0         # forbrug ved den fart

    cruise_kn: float = 0.0        # motorbådens marchfart i smult vande
    hull: str = DISPLACEMENT
    crew_note: str = ''           # ét ord om hvad båden er god til

    polar: dict[int, dict[int, float]] = field(default_factory=dict)

    @property
    def is_motor(self) -> bool:
        return self.kind == MOTOR

    @property
    def cruise(self) -> float:
        """Den fart båden holder, når intet står i vejen."""
        return self.cruise_kn if self.is_motor else self.motor_speed_kn

    @property
    def summary(self) -> str:
        if self.is_motor:
            return f'{self.length_m:g} m · {self.cruise_kn:g} kn march · {self.hull}'
        return f'{self.length_m:g} m · {self.hull_speed_kn:g} kn skrogfart'


BOATS: dict[str, Boat] = {
    # ── Sejlbåde ─────────────────────────────────────────────────────────────
    'jeanneau': Boat(
        id='jeanneau', name='Jeanneau Espace 1000', icon='sailing', kind=SAIL,
        length_m=10, hull_speed_kn=7.2, desc='Familiekrydser',
        crew_note='rolig og tilgivende', max_wind_kn=20, max_wave_m=1.5,
        motor_speed_kn=5.5, fuel_lph=2.5,
        polar={
            30:  {5: 2.5, 10: 4.0, 15: 5.0, 20: 5.5, 25: 5.8},
            45:  {5: 3.0, 10: 4.8, 15: 5.8, 20: 6.3, 25: 6.5},
            60:  {5: 3.5, 10: 5.2, 15: 6.2, 20: 6.8, 25: 7.0},
            75:  {5: 3.8, 10: 5.5, 15: 6.5, 20: 7.0, 25: 7.2},
            90:  {5: 4.0, 10: 5.8, 15: 6.8, 20: 7.1, 25: 7.2},
            110: {5: 4.2, 10: 5.6, 15: 6.5, 20: 6.9, 25: 7.0},
            135: {5: 3.5, 10: 4.8, 15: 5.5, 20: 6.0, 25: 6.2},
            150: {5: 2.8, 10: 4.0, 15: 4.8, 20: 5.2, 25: 5.5},
            180: {5: 2.5, 10: 3.5, 15: 4.2, 20: 4.8, 25: 5.0},
        }),
    'bavaria': Boat(
        id='bavaria', name='Bavaria 34', icon='sailing', kind=SAIL,
        length_m=10.4, hull_speed_kn=7.4, desc='Weekendbåd',
        crew_note='rummelig og hurtig nok', max_wind_kn=22, max_wave_m=1.8,
        motor_speed_kn=6.0, fuel_lph=3.0,
        polar={
            30:  {5: 2.8, 10: 4.5, 15: 5.5, 20: 6.0, 25: 6.3},
            45:  {5: 3.3, 10: 5.2, 15: 6.2, 20: 6.8, 25: 7.0},
            60:  {5: 3.8, 10: 5.8, 15: 6.8, 20: 7.3, 25: 7.5},
            75:  {5: 4.0, 10: 6.0, 15: 7.0, 20: 7.5, 25: 7.6},
            90:  {5: 4.2, 10: 6.2, 15: 7.2, 20: 7.5, 25: 7.6},
            110: {5: 4.0, 10: 6.0, 15: 7.0, 20: 7.3, 25: 7.4},
            135: {5: 3.5, 10: 5.2, 15: 6.0, 20: 6.5, 25: 6.6},
            150: {5: 3.0, 10: 4.5, 15: 5.2, 20: 5.8, 25: 6.0},
            180: {5: 2.8, 10: 3.8, 15: 4.5, 20: 5.0, 25: 5.2},
        }),
    'hr29': Boat(
        id='hr29', name='Hallberg-Rassy 29', icon='sailing', kind=SAIL,
        length_m=9, hull_speed_kn=6.8, desc='Langturssejler',
        crew_note='tåler mest af dem alle', max_wind_kn=25, max_wave_m=2.0,
        motor_speed_kn=5.0, fuel_lph=2.2,
        polar={
            30:  {5: 2.3, 10: 3.8, 15: 4.8, 20: 5.2, 25: 5.5},
            45:  {5: 2.8, 10: 4.5, 15: 5.5, 20: 6.0, 25: 6.2},
            60:  {5: 3.2, 10: 5.0, 15: 6.0, 20: 6.5, 25: 6.7},
            75:  {5: 3.5, 10: 5.2, 15: 6.2, 20: 6.7, 25: 6.8},
            90:  {5: 3.8, 10: 5.5, 15: 6.5, 20: 6.8, 25: 6.8},
            110: {5: 3.5, 10: 5.2, 15: 6.2, 20: 6.5, 25: 6.6},
            135: {5: 3.0, 10: 4.5, 15: 5.2, 20: 5.8, 25: 6.0},
            150: {5: 2.5, 10: 3.8, 15: 4.5, 20: 5.0, 25: 5.2},
            180: {5: 2.2, 10: 3.2, 15: 4.0, 20: 4.5, 25: 4.8},
        }),

    # ── Motorbåde ────────────────────────────────────────────────────────────
    # Marchfarten er den, man holder i smult vande. Hvad søen gør ved den,
    # regner `sailing.motor_speed` ud time for time.
    'trawler': Boat(
        id='trawler', name='Trawler 11 m', icon='directions_boat', kind=MOTOR,
        length_m=11, desc='Fortrængningsbåd', crew_note='langsom, men uanfægtet',
        max_wind_kn=24, max_wave_m=1.8,
        cruise_kn=8.0, hull=DISPLACEMENT, hull_speed_kn=8.5, fuel_lph=11.0),
    'semi10': Boat(
        id='semi10', name='Motorbåd 10 m', icon='directions_boat', kind=MOTOR,
        length_m=10, desc='Halvplanende', crew_note='den brede middelvej',
        max_wind_kn=18, max_wave_m=1.2,
        cruise_kn=14.0, hull=SEMI, hull_speed_kn=7.5, fuel_lph=42.0),
    'planing9': Boat(
        id='planing9', name='Daycruiser 9 m', icon='speed', kind=MOTOR,
        length_m=9, desc='Planende', crew_note='hurtig i smult vande, hård i sø',
        max_wind_kn=14, max_wave_m=0.8,
        cruise_kn=24.0, hull=PLANING, hull_speed_kn=7.0, fuel_lph=70.0),
    'flybridge': Boat(
        id='flybridge', name='Flybridge 14 m', icon='directions_boat', kind=MOTOR,
        length_m=14, desc='Stor planende', crew_note='komfort og rækkevidde',
        max_wind_kn=20, max_wave_m=1.5,
        cruise_kn=20.0, hull=PLANING, hull_speed_kn=8.8, fuel_lph=120.0),
}

DEFAULT_BOAT = 'jeanneau'

SAILBOATS = [b for b in BOATS.values() if not b.is_motor]
MOTORBOATS = [b for b in BOATS.values() if b.is_motor]


# ── Din egen båd ─────────────────────────────────────────────────────────────
# De syv både ovenfor er eksempler. Ingen sejler ejer et eksempel — man ejer en
# bestemt båd med en bestemt fart og et bestemt forbrug, og det er den, planen
# skal regne på.
#
# For en motorbåd er det ligetil: marchfart, skrogtype, forbrug. For en sejlbåd
# ville det rigtige være et polardiagram, men det har de færreste liggende. I
# stedet spørger vi om ét tal, enhver sejler kender — farten ved halvvind i
# jævn vind — og skalerer en almindelig krydsers diagram, så det rammer dét
# tal. Formen på kurven er den samme; niveauet er brugerens eget.
CUSTOM_ID = 'min'

REFERENCE = 'jeanneau'          # diagrammet, der skaleres
REFERENCE_TWA = 90              # halvvind
REFERENCE_TWS = 10              # jævn vind


def reference_speed() -> float:
    """Krydserens fart ved halvvind i 10 knob — det tal, brugerens fart måles mod."""
    row = BOATS[REFERENCE].polar[REFERENCE_TWA]
    return row[REFERENCE_TWS]


def scaled_polar(speed_kn: float) -> dict[int, dict[int, float]]:
    """Referencediagrammet skaleret, så halvvind i 10 knob giver `speed_kn`."""
    factor = max(0.3, min(2.5, speed_kn / reference_speed()))
    return {angle: {wind: round(value * factor, 2) for wind, value in row.items()}
            for angle, row in BOATS[REFERENCE].polar.items()}


def custom_boat(spec: dict) -> Boat:
    """Byg brugerens egen båd ud af det, han har tastet ind."""
    motor = str(spec.get('kind') or SAIL) == MOTOR
    name = str(spec.get('name') or '').strip() or 'Min båd'
    length = _number(spec.get('length_m'), 10.0, 3, 40)

    if motor:
        cruise = _number(spec.get('cruise_kn'), 12.0, 3, 60)
        return Boat(
            id=CUSTOM_ID, name=name, icon='directions_boat', kind=MOTOR,
            length_m=length, desc='Din egen', crew_note='som du har tastet den ind',
            max_wind_kn=_number(spec.get('max_wind_kn'), 18.0, 5, 40),
            max_wave_m=_number(spec.get('max_wave_m'), 1.2, 0.3, 4),
            cruise_kn=cruise,
            hull=str(spec.get('hull') or SEMI),
            hull_speed_kn=_hull_speed(length),
            fuel_lph=_number(spec.get('fuel_lph'), 40.0, 1, 400))

    reach = _number(spec.get('reach_kn'), reference_speed(), 2, 20)
    return Boat(
        id=CUSTOM_ID, name=name, icon='sailing', kind=SAIL,
        length_m=length, desc='Din egen', crew_note='som du har tastet den ind',
        max_wind_kn=_number(spec.get('max_wind_kn'), 20.0, 5, 40),
        max_wave_m=_number(spec.get('max_wave_m'), 1.5, 0.3, 4),
        hull_speed_kn=_hull_speed(length),
        motor_speed_kn=_number(spec.get('motor_speed_kn'), 5.5, 2, 12),
        fuel_lph=_number(spec.get('fuel_lph'), 3.0, 0.5, 40),
        polar=scaled_polar(reach))


def _hull_speed(length_m: float) -> float:
    """Skrogfart efter den gamle tommelfingerregel: 1,34 · √(vandlinje i fod).

    Vandlinjen sættes til 85 % af længden overalt — det passer nogenlunde for
    en almindelig lystbåd og er bedre end at gætte på et rundt tal.
    """
    waterline_ft = max(1.0, length_m * 0.85) * 3.28084
    return round(1.34 * waterline_ft ** 0.5, 1)


def _number(value, fallback: float, low: float, high: float) -> float:
    """Læs et tal fra brugerens indtastning og hold det inden for det mulige."""
    try:
        return max(low, min(high, float(value)))
    except (TypeError, ValueError):
        return fallback
