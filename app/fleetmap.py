"""Hvor de andre både er.

Det her er den mest følsomme oplysning, appen håndterer. En position siger ikke
kun "her er en båd" — den siger også "her er et hjem, der står tomt", og "her
ligger nogen alene i en øde ankerplads". Derfor er reglerne ikke pynt, de er
selve konstruktionen:

**Man er usynlig som udgangspunkt.** Der er ingen, der bliver delt ved et uheld.
Man skal selv tænde for det, og man vælger et bådnavn — ikke sit eget.

**Man ser kun andre, hvis man selv er synlig.** Symmetrien er både rimelig og
sikker: ingen kan ligge og kigge på andre uden selv at være der. Slukker man,
forsvinder man fra andres kort og de fra ens eget, med det samme.

**Positionen udløber af sig selv.** Kommer der ingen ny inden for en halv time,
er båden væk. Der findes ingen historik — hver ny position skriver den gamle
over. Man kan ikke slå op, hvor nogen var i går, fordi det ikke er gemt nogen
steder.

**Der slettes med det samme.** Slukker man, forsvinder rækken. Ikke markeres
som skjult — slettes.
"""
from __future__ import annotations

import math
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timedelta

from .config import settings

DB_NAME = 'sejlplan.db'

# Kommer der ingen ny position inden for det her, er båden væk fra kortet.
# Halvtreds minutter i en havn med dårligt signal ville være for kort; en halv
# time rammer en båd, der sejler.
FRESH_MIN = 30

# Så mange både vises ad gangen. Flere end det er ikke information, det er en
# sværm — og de fjerneste er alligevel ikke interessante.
MAX_SHOWN = 120

# Længere væk end det er de ikke i nærheden af én længere.
NEAR_NM = 60.0

NM_PER_RADIAN = 3440.065
NAME_MAX = 30


@dataclass
class Boat:
    """En anden båd, som den ser ud på kortet."""
    mark: str
    name: str
    lat: float
    lon: float
    course: float | None
    speed_kn: float | None
    when: datetime
    # Sættes af fladen, når båden har skrevet og venter på svar. Den hører
    # ikke til i databasen — den er en egenskab ved den, der kigger.
    unread: int = 0

    @property
    def age_min(self) -> float:
        return (datetime.now() - self.when).total_seconds() / 60

    @property
    def age(self) -> str:
        m = self.age_min
        if m < 2:
            return 'lige nu'
        if m < 60:
            return f'for {m:.0f} min siden'
        return f'for {m / 60:.0f} timer siden'


def _open() -> sqlite3.Connection:
    folder = settings.storage_dir
    folder.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(folder / DB_NAME, timeout=10)
    con.row_factory = sqlite3.Row
    con.execute("""
        CREATE TABLE IF NOT EXISTS positions (
            mark    TEXT PRIMARY KEY,
            name    TEXT NOT NULL DEFAULT '',
            lat     REAL NOT NULL,
            lon     REAL NOT NULL,
            course  REAL,
            speed   REAL,
            when_at TEXT NOT NULL
        )""")
    con.commit()
    return con


def _row(r: sqlite3.Row) -> Boat:
    return Boat(mark=r['mark'], name=r['name'], lat=r['lat'], lon=r['lon'],
                course=r['course'], speed_kn=r['speed'],
                when=datetime.fromisoformat(r['when_at']))


def available() -> bool:
    return bool(settings.storage_dir)


def show(mark: str, name: str, lat: float, lon: float,
         course: float | None = None, speed_kn: float | None = None) -> None:
    """Læg eller opdatér én båds position. Den gamle skrives over.

    Der er præcis én række per båd. Det er ikke en optimering — det er selve
    grunden til, at der ikke findes en historik at slå op i.
    """
    if not mark:
        return
    clean = (name or 'Båd').strip()[:NAME_MAX] or 'Båd'
    with _open() as con:
        con.execute(
            'INSERT INTO positions (mark,name,lat,lon,course,speed,when_at) '
            'VALUES (?,?,?,?,?,?,?) ON CONFLICT(mark) DO UPDATE SET '
            'name=excluded.name, lat=excluded.lat, lon=excluded.lon, '
            'course=excluded.course, speed=excluded.speed, '
            'when_at=excluded.when_at',
            (mark, clean, float(lat), float(lon),
             None if course is None else float(course),
             None if speed_kn is None else float(speed_kn),
             datetime.now().isoformat(timespec='seconds')))


def hide(mark: str) -> None:
    """Sluk. Rækken slettes — den markeres ikke som skjult."""
    if not mark:
        return
    with _open() as con:
        con.execute('DELETE FROM positions WHERE mark = ?', (mark,))


def others(mark: str, lat: float | None = None,
           lon: float | None = None) -> list[Boat]:
    """De andre både, der er synlige lige nu.

    `mark` er ens egen — man skal ikke se sig selv som en fremmed båd. Er der
    givet en position, sorteres de nærmeste først og de fjerne skæres fra.
    """
    cut = (datetime.now() - timedelta(minutes=FRESH_MIN)).isoformat(
        timespec='seconds')
    with _open() as con:
        rows = con.execute(
            'SELECT * FROM positions WHERE when_at > ? AND mark != ? '
            'ORDER BY when_at DESC LIMIT ?',
            (cut, mark or '', MAX_SHOWN * 3)).fetchall()

    boats = [_row(r) for r in rows]
    if lat is None or lon is None:
        return boats[:MAX_SHOWN]

    near = [(distance_nm(lat, lon, b.lat, b.lon), b) for b in boats]
    near = [(d, b) for d, b in near if d <= NEAR_NM]
    near.sort(key=lambda row: row[0])
    return [b for _d, b in near[:MAX_SHOWN]]


def count(mark: str = '') -> int:
    cut = (datetime.now() - timedelta(minutes=FRESH_MIN)).isoformat(
        timespec='seconds')
    with _open() as con:
        r = con.execute('SELECT COUNT(*) c FROM positions '
                        'WHERE when_at > ? AND mark != ?',
                        (cut, mark or '')).fetchone()
    return int(r['c'])


def sweep() -> int:
    """Ryd de udløbne væk. De er alligevel usynlige — nu findes de heller ikke."""
    cut = (datetime.now() - timedelta(minutes=FRESH_MIN * 2)).isoformat(
        timespec='seconds')
    with _open() as con:
        return con.execute('DELETE FROM positions WHERE when_at < ?',
                           (cut,)).rowcount


def distance_nm(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = math.radians
    a = (math.sin(r(lat2 - lat1) / 2) ** 2
         + math.cos(r(lat1)) * math.cos(r(lat2)) * math.sin(r(lon2 - lon1) / 2) ** 2)
    return 2 * NM_PER_RADIAN * math.asin(math.sqrt(min(1.0, a)))
