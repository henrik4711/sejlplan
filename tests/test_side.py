"""Siden skal kunne bygges — på hvert sprog, der kan vælges.

Den her findes, fordi hele forsiden gav 500 uden at nogen prøve sagde noget.
`harbours.py` manglede sin import af `t()`, og `t()` bliver først kaldt, når
kortet skubber havnene ud — altså når siden bygges, ikke når modulet
importeres. Alle moduler importerede fint. Fladen var død.

Den fandt også noget andet: siden ventede på svar fra browseren, før den
tegnede noget som helst. Kom svaret ikke, kom siden heller ikke. Prøven her
bygger siden uden en browser, der svarer på JavaScript — så hvis nogen igen
lægger en ventetid foran tegningen, står der ingenting, og prøven falder.
"""
from __future__ import annotations

import pytest
from nicegui.testing import User

from app import i18n

pytestmark = pytest.mark.module_under_test('main')

# Hvert sprog undtagen dansk — dansk har sin egen prøve ovenfor. Listen
# hentes fra i18n, så et nyt sprog er dækket fra den dag, det står i
# vælgeren.
FREMMEDE = [k for k in i18n.LANGUAGES if k != i18n.DA]


MINDST = 40


async def test_forsiden_bygges(user: User):
    await user.open('/')
    assert len(user.client.elements) > MINDST, 'fladen blev aldrig bygget'


@pytest.mark.parametrize('sprog', FREMMEDE)
async def test_forsiden_bygges_paa_fremmedsprog(user: User, sprog):
    """En oversættelse kan vælte siden helt for sig selv.

    En dom blev engang slået op i en tabel med en oversat nøgle, og fladen
    holdt kun på dansk. Derfor bygges siden her på hvert sprog.
    """
    with i18n.using(sprog):
        await user.open('/')
        assert len(user.client.elements) > MINDST, (
            f'fladen blev aldrig bygget på {sprog}')


async def test_sproget_kommer_fra_cookien(user: User):
    """Cookien følger med anmodningen, så sproget er kendt uden ventetid."""
    from nicegui import app
    from app import i18n
    await user.open('/')
    app.storage.user.pop(i18n.STORAGE_KEY, None)
    i18n.adopt({i18n.COOKIE: 'de'}, 'da-DK,da')
    assert i18n.lang() == i18n.DE


async def test_serverens_valg_slaar_cookien(user: User):
    """Har brugeren valgt i den her session, er det dét, der gælder."""
    from nicegui import app
    from app import i18n
    await user.open('/')
    app.storage.user[i18n.STORAGE_KEY] = i18n.DA
    i18n.adopt({i18n.COOKIE: 'de'}, 'de-DE,de')
    assert i18n.lang() == i18n.DA


def test_manualen_har_alle_emner():
    from app import help as helptext
    assert len(helptext.TOPICS) >= 25
