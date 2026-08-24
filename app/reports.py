"""Meldinger fra havnen: er der plads?

Det eneste, man ikke kan regne sig frem til. Vejret kommer fra en model,
afstanden fra et søkort — men om der er en plads tilbage ved ydermolen i
Marstal klokken fire, det ved kun den, der ligger der nu.

Derfor er det her ikke en opslagstavle. En opslagstavle uden brugere er værre
end ingenting: man åbner den, ser tomt, og kommer aldrig tilbage. Det her er ét
spørgsmål med tre svar, som tager to sekunder at give, og som er noget værd,
selv hvis kun én person svarer.

Tre valg, der følger af det:

**Ingen fritekst.** Tre knapper kan ikke bruges til at skændes, sælge eller
chikanere, og så skal ingen moderere noget. Der var et bemærkningsfelt et
øjeblik; med det fandtes der ét sted i Sejlplan, hvor én bruger kunne skrive
noget, en anden læste — og så følger anmeldelse, blokering og support med.
Feltet er væk. `note` bliver stående i tabellen, så gamle rækker kan læses, men
den skrives aldrig mere.

**Ingen konti.** Man melder fra sin egen browser, og browseren husker, at det
var den. Nok til at man kan slette sin egen melding og til at holde igen med
hvor mange, der kan gives.

**Meldinger dør af sig selv.** En melding fra i forgårs siger intet om i aften.
Efter halvandet døgn er den væk fra fladen, og efter en uge fra databasen.
"""
from __future__ import annotations

import secrets
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timedelta

from .config import settings

DB_NAME = 'sejlplan.db'

# De tre svar. Rækkefølgen er den, de står i på skærmen.
LEVELS = {
    'god': ('God plads', 'sentiment_satisfied', 'var(--go)'),
    'faa': ('Få pladser', 'sentiment_neutral', 'var(--warn)'),
    'fuld': ('Fuld', 'sentiment_dissatisfied', 'var(--stop)'),
}

# Så gammel må en melding være og stadig vises. En melding fra i forgårs siger
# intet om i aften.
FRESH_HOURS = 36

# Så længe bliver den i databasen, så man kan nå at slette sin egen.
KEEP_DAYS = 7

# Så mange meldinger må én browser give i døgnet. Nok til en tur langs kysten,
# for lidt til at fylde noget med.
MAX_PER_DAY = 12

# Meldingernes vægt halveres for hver af de her timer. En melding fra i
# formiddags tæller, men den, der kom for et kvarter siden, tæller fire gange
# så meget — for det er den, der ved noget om nu.
HALF_LIFE_H = 4.0



@dataclass
class Report:
    """Én melding fra én havn."""
    id: str
    harbour: str          # position, samme nøgle som havneguidens links
    name: str             # havnens navn, som den hed da meldingen kom
    level: str
    note: str
    when: datetime
    author: str

    @property
    def label(self) -> str:
        return LEVELS.get(self.level, LEVELS['god'])[0]

    @property
    def icon(self) -> str:
        return LEVELS.get(self.level, LEVELS['god'])[1]

    @property
    def tone(self) -> str:
        return LEVELS.get(self.level, LEVELS['god'])[2]

    @property
    def age(self) -> str:
        """Hvor gammel meldingen er, sagt som man siger det.

        Alderen er det vigtigste ved en melding. "Fuld" for tre timer siden er
        noget andet end "fuld" i går aftes.
        """
        from .i18n import t
        minutes = (datetime.now() - self.when).total_seconds() / 60
        if minutes < 45:
            return t('lige nu')
        hours = minutes / 60
        if hours < 2:
            return t('for en time siden')
        if hours < 20:
            return t('for {n} timer siden', n=f'{hours:.0f}')
        if hours < 34:
            return t('i går')
        return t('for {n} dage siden', n=f'{hours / 24:.0f}')

    @property
    def fresh(self) -> bool:
        return datetime.now() - self.when < timedelta(hours=FRESH_HOURS)


def key_of(lat: float, lon: float) -> str:
    """Havnens nøgle: dens position. Samme som til havneguidens links."""
    return f'{lat:.4f},{lon:.4f}'


def _open() -> sqlite3.Connection:
    folder = settings.storage_dir
    folder.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(folder / DB_NAME, timeout=10)
    con.row_factory = sqlite3.Row
    con.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id       TEXT PRIMARY KEY,
            harbour  TEXT NOT NULL,
            name     TEXT NOT NULL DEFAULT '',
            level    TEXT NOT NULL,
            note     TEXT NOT NULL DEFAULT '',
            when_at  TEXT NOT NULL,
            author   TEXT NOT NULL DEFAULT ''
        )""")
    con.execute('CREATE INDEX IF NOT EXISTS reports_harbour '
                'ON reports (harbour, when_at)')
    con.commit()
    return con


def _row(r: sqlite3.Row) -> Report:
    return Report(id=r['id'], harbour=r['harbour'], name=r['name'],
                  level=r['level'], note=r['note'],
                  when=datetime.fromisoformat(r['when_at']), author=r['author'])


def add(lat: float, lon: float, name: str, level: str,
        author: str) -> Report | None:
    """Læg en melding. Falsk hvis browseren har meldt rigeligt i dag."""
    if level not in LEVELS:
        return None
    if count_today(author) >= MAX_PER_DAY:
        return None

    rep = Report(id=secrets.token_urlsafe(12), harbour=key_of(lat, lon),
                 name=name.strip()[:80], level=level, note='',
                 when=datetime.now(), author=author)
    with _open() as con:
        con.execute('INSERT INTO reports (id,harbour,name,level,note,when_at,'
                    'author) VALUES (?,?,?,?,?,?,?)',
                    (rep.id, rep.harbour, rep.name, rep.level, rep.note,
                     rep.when.isoformat(timespec='seconds'), rep.author))
    return rep


def count_today(author: str) -> int:
    if not author:
        return 0
    cut = (datetime.now() - timedelta(days=1)).isoformat(timespec='seconds')
    with _open() as con:
        r = con.execute('SELECT COUNT(*) c FROM reports '
                        'WHERE author = ? AND when_at > ?', (author, cut)).fetchone()
    return int(r['c'])


@dataclass
class Verdict:
    """Hvad havnen melder — vejet sammen af de meldinger, der er.

    Én melding kan være forkert, eller den kan være fra en, der lå ved en
    anden bro. Tre, der siger det samme inden for et par timer, er noget
    andet. Så vi lægger dem sammen — men de friske vejer tungest, for det er
    dem, der ved noget om nu.
    """
    level: str
    newest: Report
    votes: int
    agree: int

    @property
    def label(self) -> str:
        return LEVELS.get(self.level, LEVELS['god'])[0]

    @property
    def icon(self) -> str:
        return LEVELS.get(self.level, LEVELS['god'])[1]

    @property
    def tone(self) -> str:
        return LEVELS.get(self.level, LEVELS['god'])[2]

    @property
    def age(self) -> str:
        return self.newest.age

    @property
    def note(self) -> str:
        """Hvor mange der har meldt — men kun når det siger noget."""
        if self.votes < 2:
            return ''
        if self.agree == self.votes:
            return f'{self.votes} meldinger'
        return f'{self.agree} af {self.votes} meldinger'


def _weigh(rows: list[Report]) -> Verdict | None:
    """Vej meldingerne sammen. Den friskeste tæller mest."""
    if not rows:
        return None
    now = datetime.now()
    vaegt: dict[str, float] = {}
    for r in rows:
        alder = max(0.0, (now - r.when).total_seconds() / 3600)
        vaegt[r.level] = vaegt.get(r.level, 0.0) + 0.5 ** (alder / HALF_LIFE_H)

    level = max(vaegt, key=lambda k: vaegt[k])
    rows = sorted(rows, key=lambda r: r.when, reverse=True)
    return Verdict(level=level, newest=rows[0], votes=len(rows),
                   agree=sum(1 for r in rows if r.level == level))


def latest(lat: float, lon: float) -> Verdict | None:
    """Havnens dom lige nu, vejet af de meldinger der er."""
    cut = (datetime.now() - timedelta(hours=FRESH_HOURS)).isoformat(timespec='seconds')
    with _open() as con:
        rows = con.execute(
            'SELECT * FROM reports WHERE harbour = ? AND when_at > ? '
            'ORDER BY when_at DESC',
            (key_of(lat, lon), cut)).fetchall()
    return _weigh([_row(r) for r in rows])


def recent(keys: list[str]) -> dict[str, Verdict]:
    """Dommen for hver af de havne — ét opslag i stedet for tyve.

    Havnelisten viser en håndfuld havne ad gangen. Ét kald til databasen for
    dem alle er forskellen på en liste, der er der med det samme, og en, der
    hakker.
    """
    if not keys:
        return {}
    cut = (datetime.now() - timedelta(hours=FRESH_HOURS)).isoformat(timespec='seconds')
    marks = ','.join('?' * len(keys))
    with _open() as con:
        rows = con.execute(
            f'SELECT * FROM reports WHERE harbour IN ({marks}) AND when_at > ? '
            f'ORDER BY when_at DESC', (*keys, cut)).fetchall()

    samlet: dict[str, list[Report]] = {}
    for r in rows:
        samlet.setdefault(r['harbour'], []).append(_row(r))
    return {k: v for k, v in ((k, _weigh(rs)) for k, rs in samlet.items()) if v}


def mine(author: str, limit: int = 20) -> list[Report]:
    if not author:
        return []
    with _open() as con:
        rows = con.execute(
            'SELECT * FROM reports WHERE author = ? ORDER BY when_at DESC '
            'LIMIT ?', (author, limit)).fetchall()
    return [_row(r) for r in rows]


def remove(report_id: str, author: str) -> bool:
    """Slet sin egen melding. Kun sin egen."""
    with _open() as con:
        cur = con.execute('DELETE FROM reports WHERE id = ? AND author = ?',
                          (report_id, author))
        return cur.rowcount > 0


def sweep() -> int:
    """Ryd det gamle væk. En melding fra sidste uge er ikke information."""
    cut = (datetime.now() - timedelta(days=KEEP_DAYS)).isoformat(timespec='seconds')
    with _open() as con:
        return con.execute('DELETE FROM reports WHERE when_at < ?',
                           (cut,)).rowcount
