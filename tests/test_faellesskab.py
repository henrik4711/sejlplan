"""Fællesskabet: hvad der er åbent, og hvad der er lukket.

De tre funktioner — at vise sin båd, at melde plads og at skrive til hinanden
— virker kun, når der er nogen at være sammen med. En flåde med én båd i
fortæller den første bruger, at han er alene, og det er det indtryk, han tager
med sig. Derfor er de lukkede som standard.

Prøverne her passer på to ting, der begge kan gå galt i stilhed:

**At lukket også betyder væk.** Ikke bare en knap, der ikke virker, men en
knap, der ikke er tegnet — og et manualafsnit, der ikke sender nogen ud at
lede efter den.

**At teksterne bliver stående.** Emnet skal være oversat den dag, kontakten
bliver sat. Så oversættelsestjekket skal stadig kunne se det, mens fladen ikke
kan.
"""
from __future__ import annotations

import pytest
from nicegui.testing import User

from app import chat, config, fleetmap, landing
from app import help as helptext
from app.ui import berth

pytestmark = pytest.mark.module_under_test('main')

# De emner, der hører til hver sin kontakt.
BAG_KONTAKT = {
    'plads': config.PLADSMELDING,
    'andre-baade': config.FLÅDE,
    'hvem-er-her': config.FLÅDE,
    'beskeder': config.BESKEDER,
}


@pytest.fixture
def åbent(monkeypatch):
    """Alt åbent — som den dag, der er brugere nok."""
    for navn in (config.FLÅDE, config.PLADSMELDING, config.BESKEDER):
        monkeypatch.setitem(config.ÅBNE, navn, True)


@pytest.fixture
def lukket(monkeypatch):
    """Alt lukket. Det er standarden, men prøven skal ikke hvile på, at
    ingen har sat en variabel i det miljø, den tilfældigvis kører i."""
    for navn in (config.FLÅDE, config.PLADSMELDING, config.BESKEDER):
        monkeypatch.setitem(config.ÅBNE, navn, False)


# ── Kontakten ────────────────────────────────────────────────────────────────
def test_alt_er_lukket_som_standard():
    """Standarden er lukket. Åbner man ved et uheld — en tom variabel, en
    stavefejl — står den første bruger alene i en flåde."""
    for værdi in config.fællesskab().values():
        assert værdi is False


@pytest.mark.parametrize('værdi', ['', 'fra', 'nej', 'false', '0', 'måske',
                                   'ja tak', 'TILFØJ'])
def test_kun_et_tydeligt_ja_aabner(monkeypatch, værdi):
    monkeypatch.setenv('SEJLPLAN_FLAADE', værdi)
    assert config._til('SEJLPLAN_FLAADE') is False, f'{værdi!r} åbnede'


@pytest.mark.parametrize('værdi', ['til', 'TIL', ' ja ', '1', 'true', 'on'])
def test_de_almindelige_maader_at_sige_ja_paa(monkeypatch, værdi):
    monkeypatch.setenv('SEJLPLAN_FLAADE', værdi)
    assert config._til('SEJLPLAN_FLAADE') is True, f'{værdi!r} åbnede ikke'


def test_beskeder_kan_ikke_aabnes_alene(monkeypatch):
    """Samtalen begynder ved at trykke på en båd på kortet. Uden flåden er
    indbakken en knap, der ikke fører nogen steder hen."""
    monkeypatch.setitem(config.ÅBNE, config.BESKEDER, True)
    monkeypatch.setitem(config.ÅBNE, config.FLÅDE, False)
    assert config.åben(config.BESKEDER) is False
    assert chat.available() is False


# ── Funktionerne ─────────────────────────────────────────────────────────────
def test_funktionerne_er_slaaet_fra_naar_de_er_lukkede(lukket):
    """Lager alene er ikke nok. Der skal også være en kontakt, der er sat."""
    assert fleetmap.available() is False
    assert chat.available() is False
    assert berth.available() is False


def test_funktionerne_kommer_igen_naar_de_aabnes(åbent):
    assert fleetmap.available() is True
    assert chat.available() is True
    assert berth.available() is True


# ── Manualen ─────────────────────────────────────────────────────────────────
def test_manualen_tier_om_det_der_er_lukket(lukket):
    """Et afsnit om en knap, der ikke er tegnet, sender folk ud at lede efter
    noget, der ikke er der — og så er det manualen, der er forkert."""
    synlige = {t.id for t in helptext.åbne_emner()}
    for emne in BAG_KONTAKT:
        assert emne not in synlige, f'{emne} står i manualen alligevel'


def test_manualen_har_dem_igen_naar_der_aabnes(åbent):
    synlige = {t.id for t in helptext.åbne_emner()}
    for emne in BAG_KONTAKT:
        assert emne in synlige, f'{emne} kom ikke med tilbage'


def test_teksterne_bliver_staaende(lukket):
    """Emnet forsvinder fra fladen, ikke fra koden. Så oversættelsen er der
    den dag, kontakten bliver sat — og oversættelsestjekket kan stadig se
    den, så den ikke bliver meldt forældet og ryddet væk imens."""
    alle = {t.id for t in helptext.TOPICS}
    i_tjekket = {t.id for _g, emner in helptext.groups(alle=True)
                 for t in emner}
    for emne in BAG_KONTAKT:
        assert emne in alle, f'{emne} er væk fra koden'
        assert emne in i_tjekket, f'{emne} er væk fra oversættelsestjekket'
        assert helptext.by_id(emne) is not None


AFSNIT = ('Er der plads i havnen?', 'Se andre både',
          'Beskeder mellem både', 'Hvem er der lige nu')


def test_den_printede_manual_naevner_dem_ikke(lukket, sprog):
    from app.ui import help as hui
    doc = hui.document()
    for tekst in AFSNIT:
        assert tekst not in doc, f'"{tekst}" står i den printede manual'


def test_den_printede_manual_har_dem_naar_der_er_aabent(åbent, sprog):
    """Modstykket til prøven ovenfor. Uden den kunne den første stå og være
    grøn, fordi afsnittene aldrig kom med i manualen overhovedet."""
    from app.ui import help as hui
    doc = hui.document()
    for tekst in AFSNIT:
        assert tekst in doc, f'"{tekst}" mangler i manualen, også når der er åbent'


# ── Fladen ───────────────────────────────────────────────────────────────────
def _tekst(elementer) -> str:
    return ' '.join(
        str(getattr(e, 'text', '') or '') + str(getattr(e, 'content', '') or '')
        for e in elementer)


async def test_fladen_bygges_uden_dem(user: User, lukket):
    """Siden skal stå, også når tre af dens funktioner ikke findes."""
    await user.open(landing.APP_PATH)
    assert len(user.client.elements) > 40, 'fladen blev aldrig bygget'


async def test_meld_plads_er_ikke_tegnet(user: User, lukket):
    """Ikke en knap, der ikke virker — en knap, der ikke er der."""
    await user.open(landing.APP_PATH)
    tekst = _tekst(user.client.elements.values())
    for ord_ in ('Meld plads', 'Meld om der er plads'):
        assert ord_ not in tekst, f'"{ord_}" står stadig i fladen'


async def test_meld_plads_er_tegnet_naar_den_er_aaben(user: User, åbent):
    """Modstykket. Uden den kunne prøven ovenfor være grøn, fordi knappen
    slet ikke hører til på forsiden — og så målte den ingenting."""
    await user.open(landing.APP_PATH)
    tekst = _tekst(user.client.elements.values())
    assert 'Meld plads' in tekst, 'knappen kom ikke, selv om der er åbent'


class _Stub:
    """Lige nok af en planlægger til at tegne flådelinjen."""
    sharing = False


async def test_flaadelinjen_er_ikke_tegnet(user: User, lukket):
    """"Vis min båd for andre" står nede i planen, ikke på forsiden — så den
    tegnes her for sig, med og uden kontakt."""
    from app.ui import fleet as fleetui
    await user.open(landing.APP_PATH)
    før = set(user.client.elements)
    with user.client.content:
        fleetui.line(_Stub())
    assert set(user.client.elements) == før, 'flådelinjen blev tegnet alligevel'


async def test_flaadelinjen_er_tegnet_naar_den_er_aaben(user: User, åbent):
    from app.ui import fleet as fleetui
    await user.open(landing.APP_PATH)
    før = set(user.client.elements)
    with user.client.content:
        fleetui.line(_Stub())
    nye = [user.client.elements[i]
           for i in set(user.client.elements) - før]
    assert 'Vis min båd for andre' in _tekst(nye), 'linjen kom ikke'
