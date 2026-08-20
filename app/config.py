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
