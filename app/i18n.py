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

from contextlib import contextmanager
from contextvars import ContextVar

from nicegui import app

DA = 'da'
DE = 'de'

# Sprogene i den rækkefølge, de står i vælgeren.
LANGUAGES = {
    DA: ('Dansk', '🇩🇰'),
    DE: ('Deutsch', '🇩🇪'),
}

STORAGE_KEY = 'sprog'

# Brugerens egen kopi. Egen nøgle, fordi sproget skal overleve, også når
# sessionen ikke har en rute at redde.
BROWSER_KEY = 'sejlplan_sprog'

# Oversættelserne. Nøglen er den danske sætning, præcis som den står i koden.
_TABLES: dict[str, dict[str, str]] = {}


def _table(code: str) -> dict[str, str]:
    """Hent et sprogs tabel. Indlæses første gang, det bruges."""
    if code not in _TABLES:
        if code == DE:
            from .lang import de, de_manual, de_plan, de_ui
            # Prosaen ligger for sig: manualen og sejlplanens egen tekst
            # fylder tilsammen mere end hele resten af fladen, og de skal
            # kunne rettes uden at røre knapperne.
            _TABLES[DE] = {**de.WORDS, **de_ui.WORDS, **de_manual.WORDS,
                           **de_plan.WORDS}
        else:
            _TABLES[code] = {}
    return _TABLES[code]


# Et sprog, der er sat med vilje, uden at der er en browser at spørge.
# Vejrvagten skriver sine mails fra en baggrundstråd dage efter, at brugeren
# lagde vagten — dér findes der ingen session, og uden det her ville en tysk
# sejler få sin gevinst på dansk.
_forced: ContextVar[str | None] = ContextVar('sejlplan_sprog', default=None)


@contextmanager
def using(code: str):
    """Kør et stykke arbejde på et bestemt sprog."""
    token = _forced.set(code if code in LANGUAGES else DA)
    try:
        yield
    finally:
        _forced.reset(token)


def lang() -> str:
    """Brugerens sprog. Dansk, hvis der ikke er valgt noget."""
    valgt = _forced.get()
    if valgt:
        return valgt
    try:
        code = app.storage.user.get(STORAGE_KEY)
    except (RuntimeError, KeyError):
        return DA
    return code if code in LANGUAGES else DA


def set_lang(code: str, client=None) -> None:
    """Husk sproget — både på serveren og hos brugeren selv.

    Serverens sessionsfil ligger på et filsystem, der forsvinder, hver gang
    appen bliver lagt ud på ny. Uden kopien hos brugeren ville en tysk sejler
    finde fladen på dansk igen, hver gang vi rettede en knapfarve.
    """
    if code not in LANGUAGES:
        return
    try:
        app.storage.user[STORAGE_KEY] = code
    except (RuntimeError, KeyError):
        pass
    if client is not None:
        try:
            client.run_javascript(
                f'try {{ localStorage.setItem("{BROWSER_KEY}", "{code}") }}'
                f' catch (e) {{}}')
        except Exception:
            pass


async def adopt_from_browser(client, header: str = '') -> None:
    """Hent sproget fra browserens kopi, hvis serveren har glemt det.

    Har serveren et sprog, vinder det: det er dét, brugeren sidst valgte i
    den her session. Ellers spørger vi browseren, og først derefter gætter vi
    på Accept-Language.
    """
    try:
        if app.storage.user.get(STORAGE_KEY) in LANGUAGES:
            return
    except (RuntimeError, KeyError):
        return
    try:
        await client.connected(timeout=8.0)
        code = await client.run_javascript(
            f'localStorage.getItem("{BROWSER_KEY}")', timeout=4.0)
    except Exception:
        code = None
    if code not in LANGUAGES:
        code = from_browser(header)
    set_lang(code, client)


def from_browser(header: str) -> str:
    """Gæt sproget ud af browserens Accept-Language, første gang nogen kommer.

    Et gæt, ikke en beslutning — brugeren kan altid vælge om, og valget vinder
    derefter.
    """
    # Kun browserens førstevalg tæller. Kigger man hele listen igennem, får
    # en engelsksproget browser med tysk som andetsprog fladen på tysk — og
    # det er ikke, hvad nogen har bedt om.
    første = (header or '').split(',')[0].split(';')[0].strip().lower()[:2]
    return første if første in LANGUAGES else DA


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


# Dansk bøjer ikke altid i flertal — "et sejldøgn", "to sejldøgn", "et ben",
# "to ben". Tysk gør: ein Etmal, zwei Etmale. Så flertalsformen slås op for
# sig, med nøglen "ordet|flertal". Findes den ikke, bruges entalsordet, og for
# dansk er det altid det rigtige.
PLURAL_MARK = '|flertal'

# Nogle ord skifter form, når de sættes ind i en sætning. Dansk siger "for
# halvvind" og "halvvind" med samme ord; tysk siger "halber Wind", men "bei
# halbem Wind". Så sætningsformen slås op for sig, med nøglen "ordet|sætning".
SENTENCE_MARK = '|sætning'


def t_in_sentence(text: str) -> str:
    """Ordet, som det lyder inde i en sætning. Dansk bøjer ikke — så det er
    det samme ord, og opslaget falder igennem til `t()`."""
    return _table(lang()).get(text + SENTENCE_MARK) or t(text)



def plural(n: int, one: str, many: str) -> str:
    """Tal og ord, bøjet. Begge ord oversættes hver for sig."""
    if n == 1:
        return f'{n} {t(one)}'
    tabel = _table(lang())
    ord_ = tabel.get(many + PLURAL_MARK) or t(many)
    return f'{n} {ord_}'

