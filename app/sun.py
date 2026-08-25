"""Hvornår solen står op og går ned — dér hvor båden er.

Mørke var indtil nu et klokkeslæt: alt uden for skipperens sejldøgn talte som
mørkesejlads. Det er forkert i begge ender af sæsonen. En tur, der lægger til i
Skagen klokken ni en aften i juni, blev talt som to timer i mørke, hvor solen
stod højt. En tur, der lægger til klokken halv otte sidst i september, blev
talt som nul, hvor det var bælgmørkt.

Tallet er ikke kosmetik — det er dét, der udløser "sørg for lanterner,
vagtplan og en udhvilet besætning". Så det skal være solen, og solen afhænger
af både dato og position: i juni er der halvanden times forskel på solnedgang
i Gedser og i Skagen.

Regnestykket er NOAA's, og det koster ingen forbindelse — det er ren
astronomi. Nøjagtigheden er inden for et minut eller to, og det er rigeligt til
at afgøre, om der skal tændes lanterner.

**Lanterner føres fra solnedgang til solopgang.** Derfor er det dét, `dark`
svarer på. Den borgerlige tusmørke — hvor man stadig kan se, men skal føre lys
— ligger cirka en halv time udenfor i danske farvande om sommeren, og den
kommer med som `twilight`, hvor teksten har brug for at kunne skelne.
"""
from __future__ import annotations

import math
from datetime import date, datetime, timedelta
from functools import lru_cache
from zoneinfo import ZoneInfo

from .config import TIMEZONE

# Solens midtpunkt står 0,833° under horisonten ved op- og nedgang: 0,5° for
# solskiven selv og 0,333° for lysets brydning i atmosfæren.
_HORISONT = 90.833

# Borgerlig tusmørke: solen 6° under horisonten. Derefter kan man ikke længere
# skimte en ubelyst båd.
_TUSMØRKE = 96.0

_ZONE = ZoneInfo(TIMEZONE)


def _dagsvinkel(d: date, time_utc: float = 12.0) -> float:
    """Årets vinkel i radianer — hvor langt vi er henne i omløbet."""
    dage = 366 if _skudår(d.year) else 365
    n = d.timetuple().tm_yday
    return 2 * math.pi / dage * (n - 1 + (time_utc - 12) / 24)


def _skudår(år: int) -> bool:
    return år % 4 == 0 and (år % 100 != 0 or år % 400 == 0)


def _tidsligning(g: float) -> float:
    """Forskellen mellem soltid og urets tid, i minutter."""
    return 229.18 * (0.000075
                     + 0.001868 * math.cos(g) - 0.032077 * math.sin(g)
                     - 0.014615 * math.cos(2 * g) - 0.040849 * math.sin(2 * g))


def _deklination(g: float) -> float:
    """Solens højde over ækvator, i radianer."""
    return (0.006918
            - 0.399912 * math.cos(g) + 0.070257 * math.sin(g)
            - 0.006758 * math.cos(2 * g) + 0.000907 * math.sin(2 * g)
            - 0.002697 * math.cos(3 * g) + 0.001480 * math.sin(3 * g))


def _timevinkel(lat: float, decl: float, zenit: float) -> float | None:
    """Hvor langt fra middag solen står i den højde. None: den når det aldrig.

    Nord for polarcirklen sker begge dele: midnatssol om sommeren og mørke
    hele døgnet om vinteren. Det gælder Nordkap, ikke Skagen, men Sejlplan
    kan lægge en rute derop, og så skal svaret være rigtigt.
    """
    lat_r = math.radians(lat)
    led = (math.cos(math.radians(zenit)) / (math.cos(lat_r) * math.cos(decl))
           - math.tan(lat_r) * math.tan(decl))
    if led > 1 or led < -1:
        return None
    return math.acos(led)


# Positionen rundes, før den slås op. En tiendedel grad i længde er
# fireogtyve sekunder på solnedgangen, og planen spørger for hver eneste
# sejltime — uden det her blev solen regnet forfra tusind gange for det samme
# svar, og en fuld prøvekørsel gik fra otte til seksogfyrre sekunder.
_OPLØSNING = 10


def _tider(lat: float, lon: float, d: date,
           zenit: float) -> tuple[datetime, datetime] | None:
    """(op, ned) i lokal tid — eller None, hvis solen aldrig krydser."""
    return _tider_cached(round(lat * _OPLØSNING) / _OPLØSNING,
                         round(lon * _OPLØSNING) / _OPLØSNING, d, zenit)


@lru_cache(maxsize=4096)
def _tider_cached(lat: float, lon: float, d: date,
                  zenit: float) -> tuple[datetime, datetime] | None:
    g = _dagsvinkel(d)
    decl = _deklination(g)
    ha = _timevinkel(lat, decl, zenit)
    if ha is None:
        return None
    ha_grader = math.degrees(ha)
    eq = _tidsligning(g)

    def lokal(minutter_utc: float) -> datetime:
        start = datetime(d.year, d.month, d.day, tzinfo=ZoneInfo('UTC'))
        return (start + timedelta(minutes=minutter_utc)) \
            .astimezone(_ZONE).replace(tzinfo=None)

    op = lokal(720 - 4 * (lon + ha_grader) - eq)
    ned = lokal(720 - 4 * (lon - ha_grader) - eq)
    return op, ned


def sunrise_sunset(lat: float, lon: float,
                   d: date) -> tuple[datetime, datetime] | None:
    """Solopgang og solnedgang, lokal tid. None ved midnatssol eller polarnat."""
    return _tider(lat, lon, d, _HORISONT)


def twilight(lat: float, lon: float,
             d: date) -> tuple[datetime, datetime] | None:
    """Borgerlig tusmørke: hvornår det bliver lyst nok, og mørkt nok."""
    return _tider(lat, lon, d, _TUSMØRKE)


def _lys_hele_døgnet(lat: float, d: date) -> bool:
    """Er det midnatssol eller polarnat? Afgøres på solens middagshøjde."""
    decl = _deklination(_dagsvinkel(d))
    højde_middag = 90 - abs(lat - math.degrees(decl))
    return højde_middag > 0


def dark(lat: float, lon: float, t: datetime) -> bool:
    """Er det mørkt her og nu — altså skal der føres lanterner?

    Fra solnedgang til solopgang. Det er reglen for lanterneføring, og det er
    derfor dét, der tælles: det er den beslutning, tallet skal bruges til.
    """
    tider = sunrise_sunset(lat, lon, t.date())
    if tider is None:
        # Solen krydser ikke horisonten i dag. Så er det enten lyst hele
        # døgnet eller mørkt hele døgnet.
        return not _lys_hele_døgnet(lat, t.date())
    op, ned = tider
    if ned < op:
        # Solnedgangen falder før solopgangen i lokal tid — det sker tæt på
        # datoskiftet. Så er det lyst mellem dem, ikke omvendt.
        return ned <= t < op
    return t < op or t >= ned


def dusk(lat: float, lon: float, d: date) -> datetime | None:
    """Hvornår det bliver mørkt i aften. Til teksten, ikke til tællingen."""
    tider = sunrise_sunset(lat, lon, d)
    return tider[1] if tider else None


def dawn(lat: float, lon: float, d: date) -> datetime | None:
    """Hvornår det bliver lyst i morgen tidlig."""
    tider = sunrise_sunset(lat, lon, d)
    return tider[0] if tider else None
