"""Sprog.

Dansk er kilden. Hver tekst i programmet står stadig på dansk i koden — den
danske sætning *er* nøglen — og oversættelserne slås op i den. Det har to
følger, som begge er værd at have:

Man kan lægge sprog til lidt ad gangen. Mangler en tysk sætning, falder den
tilbage til den danske i stedet for at vise et tomt felt eller `plan.header.3`.
Programmet virker hele vejen igennem fra første dag.

Og koden kan læses. `t('Find bedste afgangstider')` siger, hvad der står på
knappen; `t('btn.search_departures')` gør ikke.

Prisen er, at retter man en dansk sætning, mister den sin oversættelse i
stilhed. Derfor findes `tools/check_translations.py`, som siger hvilke der
mangler.

Sproget hører til brugeren, ikke til serveren: det ligger i sessionen sammen med
båden og ruterne og rejser med den kopi, browseren får.
"""
from __future__ import annotations

from nicegui import app

DA = 'da'
DE = 'de'

# Sprogene i den rækkefølge, de står i vælgeren.
LANGUAGES = {
    DA: ('Dansk', '🇩🇰'),
    DE: ('Deutsch', '🇩🇪'),
}

STORAGE_KEY = 'sprog'

# Oversættelserne. Nøglen er den danske sætning, præcis som den står i koden.
_TABLES: dict[str, dict[str, str]] = {}


def _table(code: str) -> dict[str, str]:
    """Hent et sprogs tabel. Indlæses første gang, det bruges."""
    if code not in _TABLES:
        if code == DE:
            from .lang import de, de_manual
            # Manualens prosa ligger for sig. Den fylder mere end hele resten
            # af fladen, og den skal kunne rettes uden at røre knapperne.
            _TABLES[DE] = {**de.WORDS, **de_manual.WORDS}
        else:
            _TABLES[code] = {}
    return _TABLES[code]


def lang() -> str:
    """Brugerens sprog. Dansk, hvis der ikke er valgt noget."""
    try:
        code = app.storage.user.get(STORAGE_KEY)
    except (RuntimeError, KeyError):
        return DA
    return code if code in LANGUAGES else DA


def set_lang(code: str) -> None:
    if code not in LANGUAGES:
        return
    try:
        app.storage.user[STORAGE_KEY] = code
    except (RuntimeError, KeyError):
        pass


def from_browser(header: str) -> str:
    """Gæt sproget ud af browserens Accept-Language, første gang nogen kommer.

    Et gæt, ikke en beslutning — brugeren kan altid vælge om, og valget vinder
    derefter.
    """
    for part in (header or '').split(','):
        code = part.split(';')[0].strip().lower()[:2]
        if code in LANGUAGES:
            return code
    return DA


def t(text: str, **kwargs) -> str:
    """Teksten på brugerens sprog. Pladsholdere sættes ind med `{navn}`.

    Findes oversættelsen ikke, står den danske. Det er med vilje: en halvt
    oversat flade er brugbar, en flade med huller i er ikke.
    """
    code = lang()
    out = _table(code).get(text, text) if code != DA else text
    if kwargs:
        try:
            return out.format(**kwargs)
        except (KeyError, IndexError, ValueError):
            # En pladsholder, der ikke passer, må ikke vælte en side. Så
            # hellere den danske sætning med de rigtige tal i.
            try:
                return text.format(**kwargs)
            except Exception:
                return text
    return out


def plural(n: int, one: str, many: str) -> str:
    """Tal og ord, bøjet. Begge ord oversættes hver for sig."""
    return f'{n} {t(one) if n == 1 else t(many)}'

