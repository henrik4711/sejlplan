"""Central konfiguration. Alt hentes fra .env, med fornuftige standardværdier."""
from __future__ import annotations

import os
import secrets
from dataclasses import dataclass, field
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:  # dotenv er valgfri – .env kan også være sat som rigtige env-vars
    def load_dotenv(*_args, **_kwargs):
        return False

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / '.env')


def _env(name: str, default: str = '') -> str:
    return (os.getenv(name) or default).strip()


# Alt andet end et tydeligt ja er et nej. En kontakt, der står til "måske",
# findes ikke — og en, der åbner sig selv på en stavefejl, er værre end en,
# der bliver lukket.
_JA = {'til', '1', 'ja', 'true', 'on', 'yes', 'åben'}


def _til(name: str) -> bool:
    return _env(name).lower() in _JA


# ── Fællesskabet ─────────────────────────────────────────────────────────────
# At vise sin båd, at melde plads i havnen og at skrive til hinanden virker kun,
# når der er nogen at være sammen med. En flåde med én båd i er ikke en halv
# flåde — den fortæller den første bruger, at han er alene, og det er det
# indtryk, han tager med sig. Derfor er de tre lukkede som standard og åbnes
# med vilje, når der er brugere nok.
#
# De åbnes hver for sig, for de har ikke samme tærskel: en pladsmelding hjælper
# den næste, der kommer til havnen, allerede når vi er få, mens bådene på
# kortet først giver mening, når der er nogen at se.
FLÅDE = 'flåde'
PLADSMELDING = 'pladsmelding'
BESKEDER = 'beskeder'

_KONTAKTER = {
    FLÅDE: 'SEJLPLAN_FLAADE',
    PLADSMELDING: 'SEJLPLAN_PLADSMELDING',
    BESKEDER: 'SEJLPLAN_BESKEDER',
}

ÅBNE: dict[str, bool] = {navn: _til(nøgle)
                         for navn, nøgle in _KONTAKTER.items()}


def åben(hvad: str) -> bool:
    """Er funktionen åben? Lukket er standard — vi åbner med vilje."""
    if hvad == BESKEDER:
        # Beskeder kræver, at man kan se hinanden: samtalen begynder ved at
        # trykke på en båd på kortet. Åbner man kun beskederne, er der ingen
        # at skrive til, og indbakken er en knap, der ikke fører nogen steder
        # hen.
        return ÅBNE.get(BESKEDER, False) and ÅBNE.get(FLÅDE, False)
    return ÅBNE.get(hvad, False)


def fællesskab() -> dict[str, bool]:
    """Hvad der er åbent lige nu. Til opstartslinjen og til /api/status."""
    return {navn: åben(navn) for navn in _KONTAKTER}


SECRET_FILE = ROOT / '.storage_secret'


def _storage_secret() -> str:
    """Hemmeligheden der signerer brugersessioner.

    Uden en fast værdi får serveren en ny ved hver genstart, og så mister alle
    brugere deres gemte rute. Er der ingen i .env, laver vi én og lægger den i
    en fil ved siden af — så virker det ud af boksen, også lokalt.
    """
    from_env = _env('SEJLPLAN_STORAGE_SECRET')
    if from_env and not from_env.startswith('skift-mig'):
        return from_env

    try:
        if SECRET_FILE.exists():
            saved = SECRET_FILE.read_text(encoding='utf-8').strip()
            if saved:
                return saved
        generated = secrets.token_urlsafe(32)
        SECRET_FILE.write_text(generated, encoding='utf-8')
        return generated
    except OSError:
        # Skrivebeskyttet filsystem – så kører vi videre uden at kunne gemme.
        return secrets.token_urlsafe(32)


@dataclass(frozen=True)
class Settings:
    """Serverindstillinger. Læses én gang ved opstart."""

    anthropic_key: str = field(default_factory=lambda: _env('ANTHROPIC_API_KEY'))
    ai_model: str = field(default_factory=lambda: _env('SEJLPLAN_AI_MODEL', 'claude-opus-5'))
    storage_secret: str = field(default_factory=_storage_secret)
    host: str = field(default_factory=lambda: _env('SEJLPLAN_HOST', '0.0.0.0'))
    # Railway, Heroku og de fleste andre platforme fortæller via PORT hvilken
    # port de har åbnet for os. Vores egen variabel vinder, så man kan sætte
    # noget andet lokalt uden at røre platformens.
    port: int = field(default_factory=lambda: int(
        _env('SEJLPLAN_PORT') or _env('PORT') or '8090'))
    contact: str = field(default_factory=lambda: _env('SEJLPLAN_CONTACT', 'sejlplan@example.com'))

    # Hvor serveren lægger det, den skal huske, mens ingen er logget på —
    # vejrvagterne. Railways filsystem forsvinder ved hver udrulning, så her
    # skal peges på et volume, hvis vagterne skal overleve.
    data_dir: str = field(default_factory=lambda: _env('SEJLPLAN_DATA_DIR'))

    # Adressen brugeren ser i browseren. Den skal med i mails, så linket i dem
    # fører hjem — serveren kender den ikke selv.
    site_url: str = field(default_factory=lambda: _env(
        'SEJLPLAN_SITE_URL', 'http://localhost:8090').rstrip('/'))

    # Afsendelse af mail. Uden dem er vejrvagten slået fra, og fladen siger det.
    smtp_host: str = field(default_factory=lambda: _env('SEJLPLAN_SMTP_HOST'))
    smtp_port: int = field(default_factory=lambda: int(
        _env('SEJLPLAN_SMTP_PORT') or '587'))
    smtp_user: str = field(default_factory=lambda: _env('SEJLPLAN_SMTP_USER'))
    smtp_password: str = field(default_factory=lambda: _env('SEJLPLAN_SMTP_PASSWORD'))
    mail_from: str = field(default_factory=lambda: _env('SEJLPLAN_MAIL_FROM'))

    @property
    def storage_dir(self) -> Path:
        """Mappen til det, der skal overleve en genstart."""
        return Path(self.data_dir) if self.data_dir else ROOT / '.data'

    @property
    def storage_is_durable(self) -> bool:
        """Er der peget på et rigtigt volume?

        Uden det ligger vagterne på et filsystem, der bliver kasseret ved næste
        udrulning — og en vagt, der forsvinder i stilhed, er værre end ingen.
        """
        return bool(self.data_dir)

    @property
    def mail_available(self) -> bool:
        return bool(self.smtp_host and self.mail_from)

    @property
    def watch_available(self) -> bool:
        """Vejrvagten kræver en postkasse. Et volume er stærkt anbefalet.

        Uden volume virker den — indtil næste udrulning, hvor filen forsvinder
        sammen med resten af serverens disk. Derfor slår vi den ikke fra, men
        siger det højt i fladen: en vagt, man har lagt og glemt, er god; en
        vagt, der forsvinder i stilhed, er værre end ingen.
        """
        return self.mail_available

    @property
    def ai_available(self) -> bool:
        """AI-fanen skjuler sig selv pænt, hvis serveren ikke har en nøgle."""
        return bool(self.anthropic_key)

    @property
    def user_agent(self) -> str:
        return f'Sejlplan/2.0 ({self.contact})'


settings = Settings()

# Tidszone brugt til alle visninger og til vejr-API'erne.
TIMEZONE = 'Europe/Copenhagen'
