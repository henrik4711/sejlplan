"""Korte beskeder mellem både, der begge er synlige.

Det her er den del, jeg havde betænkeligheder ved, og de var ikke ubegrundede:
i det øjeblik én bruger kan skrive noget, en anden læser, findes der en
forpligtelse, der ikke går væk igen. Nogen skal kunne blokere, nogen skal kunne
anmelde, og nogen skal kigge på anmeldelserne — også i juli.

Så bygges det med værnene fra dag ét, ikke som noget der lægges ovenpå bagefter:

**Kun mellem både, der begge er synlige på kortet.** Man skriver til en, man kan
se — ikke til en fremmed adresse. Slukker modtageren for sin synlighed, kan der
ikke skrives til ham.

**Blokering virker begge veje og med det samme.** Har man blokeret en, kan han
hverken skrive eller se, at man er der.

**Anmeldelse gemmer beskeden.** Ellers står ord mod ord, og så kan ingen gøre
noget ved det.

**Beskeder dør.** Efter et døgn er de væk. Det er ikke en indbakke, man samler
på — det er "vi ligger ved ydermolen, kom over til en kop kaffe".
"""
from __future__ import annotations

import secrets
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timedelta

from . import postbud
from .config import settings

DB_NAME = 'sejlplan.db'

TEXT_MAX = 240

# Så længe lever en besked. Det er ikke en indbakke — det er en besked mellem
# to både, der ligger i det samme farvand lige nu.
KEEP_HOURS = 24

# Så mange beskeder må én båd sende i timen. Nok til en samtale, for lidt til
# at genere nogen med.
MAX_PER_HOUR = 20

# Så mange gange må man skrive til en, der ikke svarer, før man må vente.
# Uden det kan man skrive tyve beskeder til den samme, der ikke vil snakke.
MAX_UNANSWERED = 3


@dataclass
class Message:
    id: str
    from_mark: str
    from_name: str
    to_mark: str
    text: str
    when: datetime
    seen: int

    @property
    def age(self) -> str:
        m = (datetime.now() - self.when).total_seconds() / 60
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
        CREATE TABLE IF NOT EXISTS messages (
            id        TEXT PRIMARY KEY,
            from_mark TEXT NOT NULL,
            from_name TEXT NOT NULL DEFAULT '',
            to_mark   TEXT NOT NULL,
            text      TEXT NOT NULL,
            when_at   TEXT NOT NULL,
            seen      INTEGER NOT NULL DEFAULT 0
        )""")
    con.execute('CREATE INDEX IF NOT EXISTS messages_to '
                'ON messages (to_mark, when_at)')
    con.execute("""
        CREATE TABLE IF NOT EXISTS blocks (
            owner   TEXT NOT NULL,
            blocked TEXT NOT NULL,
            when_at TEXT NOT NULL,
            PRIMARY KEY (owner, blocked)
        )""")
    con.execute("""
        CREATE TABLE IF NOT EXISTS abuse (
            id       TEXT PRIMARY KEY,
            msg_id   TEXT NOT NULL,
            msg_text TEXT NOT NULL,
            from_mark TEXT NOT NULL,
            by_mark  TEXT NOT NULL,
            when_at  TEXT NOT NULL,
            handled  INTEGER NOT NULL DEFAULT 0
        )""")
    con.commit()
    return con


def _row(r: sqlite3.Row) -> Message:
    return Message(id=r['id'], from_mark=r['from_mark'],
                   from_name=r['from_name'], to_mark=r['to_mark'],
                   text=r['text'], when=datetime.fromisoformat(r['when_at']),
                   seen=r['seen'])


def available() -> bool:
    return bool(settings.storage_dir)


# ── Blokering ────────────────────────────────────────────────────────────────
def block(owner: str, other: str) -> None:
    """Bloker en båd. Virker begge veje: han kan hverken skrive eller se mig."""
    if not owner or not other or owner == other:
        return
    with _open() as con:
        con.execute('INSERT OR IGNORE INTO blocks (owner,blocked,when_at) '
                    'VALUES (?,?,?)',
                    (owner, other,
                     datetime.now().isoformat(timespec='seconds')))


def unblock(owner: str, other: str) -> None:
    with _open() as con:
        con.execute('DELETE FROM blocks WHERE owner = ? AND blocked = ?',
                    (owner, other))


def blocked_by_either(a: str, b: str) -> bool:
    """Har en af de to blokeret den anden?"""
    if not a or not b:
        return False
    with _open() as con:
        r = con.execute(
            'SELECT 1 FROM blocks WHERE (owner=? AND blocked=?) '
            'OR (owner=? AND blocked=?) LIMIT 1', (a, b, b, a)).fetchone()
    return r is not None


def blocked_list(owner: str) -> set[str]:
    with _open() as con:
        rows = con.execute(
            'SELECT blocked FROM blocks WHERE owner = ?', (owner,)).fetchall()
        mine = {r['blocked'] for r in rows}
        rows = con.execute(
            'SELECT owner FROM blocks WHERE blocked = ?', (owner,)).fetchall()
        return mine | {r['owner'] for r in rows}


# ── Beskeder ─────────────────────────────────────────────────────────────────
def send(from_mark: str, from_name: str, to_mark: str,
         text: str) -> tuple[bool, str]:
    """Send én besked. Giver (lykkedes, grund hvis ikke)."""
    text = (text or '').strip()[:TEXT_MAX]
    if not text or not from_mark or not to_mark or from_mark == to_mark:
        return False, 'Der er ingen besked at sende.'
    if blocked_by_either(from_mark, to_mark):
        # Vi siger ikke hvem der har blokeret hvem. Det ville i sig selv være
        # en oplysning, man kunne bruge til noget.
        return False, 'Beskeden kunne ikke sendes.'

    hour = (datetime.now() - timedelta(hours=1)).isoformat(timespec='seconds')
    with _open() as con:
        n = con.execute('SELECT COUNT(*) c FROM messages '
                        'WHERE from_mark = ? AND when_at > ?',
                        (from_mark, hour)).fetchone()['c']
        if n >= MAX_PER_HOUR:
            return False, 'Du har sendt rigeligt den seneste time.'

        # Skriver man til en, der ikke svarer, er der en grænse.
        ubesvaret = con.execute(
            'SELECT COUNT(*) c FROM messages WHERE from_mark = ? AND to_mark = ? '
            'AND when_at > (SELECT COALESCE(MAX(when_at), \'\') FROM messages '
            'WHERE from_mark = ? AND to_mark = ?)',
            (from_mark, to_mark, to_mark, from_mark)).fetchone()['c']
        if ubesvaret >= MAX_UNANSWERED:
            return False, ('Du har skrevet tre gange uden svar. Vent til han '
                           'svarer.')

        con.execute(
            'INSERT INTO messages (id,from_mark,from_name,to_mark,text,when_at)'
            ' VALUES (?,?,?,?,?,?)',
            (secrets.token_urlsafe(12), from_mark, from_name.strip()[:30],
             to_mark, text, datetime.now().isoformat(timespec='seconds')))

    # Sig til modtageren med det samme. Før lå beskeden og ventede, til hans
    # browser tilfældigvis spurgte efter den — op til tyve sekunder på en
    # sætning, der som regel er "vi ligger ved ydermolen, kom over".
    postbud.besked_til(to_mark, from_mark, from_name.strip()[:30])
    return True, ''


def inbox(mark: str) -> list[Message]:
    """Beskeder til mig, nyeste sidst — som en samtale læses."""
    if not mark:
        return []
    cut = (datetime.now() - timedelta(hours=KEEP_HOURS)).isoformat(
        timespec='seconds')
    spærret = blocked_list(mark)
    with _open() as con:
        rows = con.execute(
            'SELECT * FROM messages WHERE to_mark = ? AND when_at > ? '
            'ORDER BY when_at', (mark, cut)).fetchall()
    return [m for m in (_row(r) for r in rows) if m.from_mark not in spærret]


def thread(mine: str, other: str) -> list[Message]:
    """Hele samtalen mellem to både."""
    cut = (datetime.now() - timedelta(hours=KEEP_HOURS)).isoformat(
        timespec='seconds')
    with _open() as con:
        rows = con.execute(
            'SELECT * FROM messages WHERE when_at > ? AND '
            '((from_mark=? AND to_mark=?) OR (from_mark=? AND to_mark=?)) '
            'ORDER BY when_at', (cut, mine, other, other, mine)).fetchall()
    return [_row(r) for r in rows]


def unread(mark: str) -> int:
    if not mark:
        return 0
    return sum(1 for m in inbox(mark) if not m.seen)


def mark_seen(mark: str, other: str = '') -> None:
    with _open() as con:
        if other:
            con.execute('UPDATE messages SET seen = 1 WHERE to_mark = ? '
                        'AND from_mark = ?', (mark, other))
        else:
            con.execute('UPDATE messages SET seen = 1 WHERE to_mark = ?',
                        (mark,))


# ── Anmeldelse ───────────────────────────────────────────────────────────────
def report_abuse(msg_id: str, by_mark: str) -> bool:
    """Anmeld en besked.

    Teksten gemmes med anmeldelsen. Ellers ville beskeden dø efter et døgn, og
    så stod ord mod ord — og så kan ingen gøre noget ved det.
    """
    with _open() as con:
        r = con.execute('SELECT * FROM messages WHERE id = ?',
                        (msg_id,)).fetchone()
        if r is None:
            return False
        con.execute(
            'INSERT OR REPLACE INTO abuse '
            '(id,msg_id,msg_text,from_mark,by_mark,when_at) '
            'VALUES (?,?,?,?,?,?)',
            (secrets.token_urlsafe(10), msg_id, r['text'], r['from_mark'],
             by_mark, datetime.now().isoformat(timespec='seconds')))
    return True


def open_abuse() -> list[dict]:
    """De anmeldelser, ingen har set på endnu. Til den, der driver stedet."""
    with _open() as con:
        rows = con.execute(
            'SELECT * FROM abuse WHERE handled = 0 ORDER BY when_at DESC'
        ).fetchall()
    return [dict(r) for r in rows]


def sweep() -> int:
    """Beskeder dør efter et døgn. Anmeldelser gør ikke."""
    cut = (datetime.now() - timedelta(hours=KEEP_HOURS)).isoformat(
        timespec='seconds')
    with _open() as con:
        return con.execute('DELETE FROM messages WHERE when_at < ?',
                           (cut,)).rowcount
