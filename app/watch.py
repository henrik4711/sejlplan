"""Vejrvagten: hold øje med en tur, og sig til når vejret er der.

En pensionist skal ikke sidde og opdatere en side i fjorten dage. Han vil sige
"vi skal til Ærø engang i september — sig til, når det ser godt ud", og så gå
i gang med noget andet.

Det kan lade sig gøre, fordi prognosen ruller frem: en dato ti døgn ude er ikke
dækket i dag, men den er det om tre. Så vagten venter, til der er tal for
dagene, regner turen igennem med brugerens egen båd og egne grænser, og skriver
først når der faktisk er et vindue.

Én vagt giver én besked. Ikke en strøm af mails, hver gang modellen flytter sig
en halv knob — så holder folk op med at læse dem. Kommer beskeden, er vagten
brugt, og man kan lægge en ny.

Vagterne bor i en SQLite-fil, fordi de skal overleve, at ingen er logget på.
Ligger den ikke på et volume, forsvinder de ved næste udrulning — og derfor
slår fladen vagten fra, hvis der ikke er peget på et.
"""
from __future__ import annotations

import json
import secrets
import sqlite3
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path

from .config import settings

DB_NAME = 'sejlplan.db'

# Hvor godt skal det være, før vi skriver? `god` er kun timer inden for
# brugerens egne grænser; `ok` accepterer også de skærpede.
QUALITY = {'god': 'kun gode forhold', 'ok': 'gode eller skærpede forhold'}

# En vagt, der aldrig får svar, skal ikke ligge for evigt. Når vinduet er
# forbi, er den udløbet.
GRACE_DAYS = 2


@dataclass
class Watch:
    """Én bruger, én rute, ét datovindue, én besked."""
    id: str
    email: str
    name: str
    waypoints: list
    boat: dict
    limits: dict
    date_from: str
    date_to: str
    quality: str
    created: str
    confirmed: int = 0
    notified: str = ''
    cancelled: int = 0
    # Sproget skal med. Mailen bliver skrevet dage senere af en baggrundstråd,
    # der ikke har nogen browsersession at spørge — havde den ikke stået her,
    # ville en tysk sejler få sin gevinst på dansk.
    lang: str = 'da'

    @property
    def title(self) -> str:
        if not self.waypoints:
            return 'Tur'
        first, last = self.waypoints[0], self.waypoints[-1]
        if len(self.waypoints) == 1:
            return str(first.get('name') or 'Tur')
        return f"{first.get('name')} → {last.get('name')}"

    @property
    def window(self) -> tuple[date, date]:
        return (date.fromisoformat(self.date_from),
                date.fromisoformat(self.date_to))

    @property
    def expired(self) -> bool:
        return date.today() > self.window[1] + timedelta(days=GRACE_DAYS)

    @property
    def live(self) -> bool:
        """Skal vagten overhovedet kigges på?"""
        return (bool(self.confirmed) and not self.cancelled
                and not self.notified and not self.expired)


# ── Hvor de bor ───────────────────────────────────────────────────────────────
def _path() -> Path:
    folder = settings.storage_dir
    folder.mkdir(parents=True, exist_ok=True)
    return folder / DB_NAME


def _open() -> sqlite3.Connection:
    con = sqlite3.connect(_path(), timeout=10)
    con.row_factory = sqlite3.Row
    con.execute("""
        CREATE TABLE IF NOT EXISTS watches (
            id        TEXT PRIMARY KEY,
            email     TEXT NOT NULL,
            name      TEXT NOT NULL DEFAULT '',
            waypoints TEXT NOT NULL,
            boat      TEXT NOT NULL,
            limits    TEXT NOT NULL,
            date_from TEXT NOT NULL,
            date_to   TEXT NOT NULL,
            quality   TEXT NOT NULL DEFAULT 'god',
            created   TEXT NOT NULL,
            confirmed INTEGER NOT NULL DEFAULT 0,
            notified  TEXT NOT NULL DEFAULT '',
            cancelled INTEGER NOT NULL DEFAULT 0
        )""")
    # Tilføjet efter at der allerede lå vagter i databasen. En vagt uden sprog
    # er dansk — det var det eneste, der fandtes, da den blev lagt.
    if 'lang' not in {r['name'] for r in
                      con.execute('PRAGMA table_info(watches)')}:
        con.execute("ALTER TABLE watches ADD COLUMN lang TEXT "
                    "NOT NULL DEFAULT 'da'")
    con.commit()
    return con


def _row(r: sqlite3.Row) -> Watch:
    return Watch(
        id=r['id'], email=r['email'], name=r['name'],
        waypoints=json.loads(r['waypoints']), boat=json.loads(r['boat']),
        limits=json.loads(r['limits']), date_from=r['date_from'],
        date_to=r['date_to'], quality=r['quality'], created=r['created'],
        confirmed=r['confirmed'], notified=r['notified'],
        cancelled=r['cancelled'],
        lang=(r['lang'] if 'lang' in r.keys() else 'da') or 'da')


# ── Læg, hent, ryd ────────────────────────────────────────────────────────────
def create(email: str, name: str, waypoints: list, boat: dict, limits: dict,
           date_from: str, date_to: str, quality: str = 'god',
           lang: str = 'da') -> Watch:
    """Læg en vagt. Den er stille, til brugeren har bekræftet sin adresse."""
    watch = Watch(
        id=secrets.token_urlsafe(18), email=email.strip().lower(),
        name=name.strip(), waypoints=waypoints, boat=boat, limits=limits,
        date_from=date_from, date_to=date_to,
        quality=quality if quality in QUALITY else 'god',
        created=datetime.now().isoformat(timespec='seconds'), lang=lang)

    with _open() as con:
        con.execute(
            'INSERT INTO watches (id,email,name,waypoints,boat,limits,'
            'date_from,date_to,quality,created,lang) '
            'VALUES (?,?,?,?,?,?,?,?,?,?,?)',
            (watch.id, watch.email, watch.name,
             json.dumps(watch.waypoints, ensure_ascii=False),
             json.dumps(watch.boat, ensure_ascii=False),
             json.dumps(watch.limits, ensure_ascii=False),
             watch.date_from, watch.date_to, watch.quality, watch.created,
             watch.lang))
    return watch


def get(watch_id: str) -> Watch | None:
    with _open() as con:
        r = con.execute('SELECT * FROM watches WHERE id = ?',
                        (watch_id,)).fetchone()
    return _row(r) if r else None


def confirm(watch_id: str) -> Watch | None:
    """Adressen er bekræftet. Først nu må vi skrive til den."""
    with _open() as con:
        con.execute('UPDATE watches SET confirmed = 1 WHERE id = ?', (watch_id,))
    return get(watch_id)


def cancel(watch_id: str) -> Watch | None:
    with _open() as con:
        con.execute('UPDATE watches SET cancelled = 1 WHERE id = ?', (watch_id,))
    return get(watch_id)


def mark_notified(watch_id: str) -> None:
    with _open() as con:
        con.execute('UPDATE watches SET notified = ? WHERE id = ?',
                    (datetime.now().isoformat(timespec='seconds'), watch_id))


def pending() -> list[Watch]:
    """De vagter, der skal kigges på nu."""
    with _open() as con:
        rows = con.execute(
            'SELECT * FROM watches WHERE confirmed = 1 AND cancelled = 0 '
            "AND notified = '' ORDER BY created").fetchall()
    return [w for w in (_row(r) for r in rows) if not w.expired]


def for_email(email: str) -> list[Watch]:
    with _open() as con:
        rows = con.execute(
            'SELECT * FROM watches WHERE email = ? ORDER BY created DESC',
            (email.strip().lower(),)).fetchall()
    return [_row(r) for r in rows]


def sweep() -> int:
    """Fjern det, der er overstået. En database skal ikke bare vokse."""
    cut = (date.today() - timedelta(days=60)).isoformat()
    with _open() as con:
        cur = con.execute(
            'DELETE FROM watches WHERE date_to < ? OR cancelled = 1', (cut,))
        return cur.rowcount
