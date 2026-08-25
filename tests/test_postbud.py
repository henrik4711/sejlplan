"""Beskeder skal leveres, ikke hentes.

Før lå en besked og ventede, til modtagerens browser tilfældigvis spurgte
efter den — op til tyve sekunder på en sætning, der som regel er "vi ligger
ved ydermolen, kom over". Prøverne her siger, at der bliver sagt til, og at
der kun bliver sagt til den, det angår.
"""
from __future__ import annotations

import asyncio

import pytest

from app import chat, fleetmap, postbud


@pytest.fixture(autouse=True)
def rent_bord():
    """Tom database og ingen lyttere.

    Uden det her bar prøverne over fra sidste kørsel: chat holder igen, når
    man har skrevet tre gange uden svar, og efter tre kørsler var det præcis
    dét, der skete. En prøve, der virker den første gang og ikke den fjerde,
    er værre end ingen prøve.
    """
    postbud._abonnenter.clear()
    _tøm()
    yield
    postbud._abonnenter.clear()
    _tøm()


def _tøm() -> None:
    with chat._open() as con:
        con.execute('DELETE FROM messages')
        con.execute('DELETE FROM blocks')
    with fleetmap._open() as con:
        con.execute('DELETE FROM positions')


async def test_besked_bliver_leveret_med_det_samme():
    modtager = postbud.subscribe('B')
    ok, grund = chat.send('A', 'Havfruen', 'B', 'Vi ligger ved ydermolen')
    assert ok, grund
    h = await asyncio.wait_for(modtager.kø.get(), 1.0)
    assert h.slags == postbud.BESKED
    assert h.fra_navn == 'Havfruen'


async def test_kun_modtageren_faar_besked():
    """En tredje båd må ikke kunne se, at der overhovedet blev skrevet."""
    modtager = postbud.subscribe('B')
    tredje = postbud.subscribe('C')
    chat.send('A', 'Havfruen', 'B', 'Hej')
    await asyncio.wait_for(modtager.kø.get(), 1.0)
    assert tredje.kø.empty()


async def test_flytning_siger_til_de_andre_men_ikke_en_selv():
    mig = postbud.subscribe('A')
    anden = postbud.subscribe('B')
    fleetmap.show('A', 'Havfruen', 55.5, 12.2)
    assert mig.kø.empty(), 'man skal ikke have besked om sin egen bevægelse'
    h = await asyncio.wait_for(anden.kø.get(), 1.0)
    assert h.slags == postbud.FLÅDE
    fleetmap.hide('A')


def test_haendelsen_baerer_ingen_position():
    """Den siger "kig igen" — ikke hvor nogen er. Opslaget bagefter går
    gennem de samme regler som altid."""
    anden = postbud.subscribe('B')
    fleetmap.show('A', 'Havfruen', 55.5, 12.2)
    h = anden.kø.get_nowait()
    felter = {f for f in vars(h) if not f.startswith('_')}
    assert felter == {'slags', 'fra_mærke', 'fra_navn'}
    fleetmap.hide('A')


def test_afmelding_rydder_op():
    a = postbud.subscribe('A')
    assert postbud.lyttere('A') == 1
    postbud.unsubscribe(a)
    assert postbud.lyttere('A') == 0
    assert 'A' not in postbud._abonnenter


def test_fuld_koe_smider_de_aeldste_vaek():
    """En browser, der ikke har hentet i lang tid, skal ikke holde
    hukommelse i live — og det er den nyeste hændelse, der betyder noget."""
    a = postbud.subscribe('A')
    for _ in range(postbud.KØ_MAX + 10):
        postbud.besked_til('A', 'B', 'Anden')
    assert a.kø.qsize() == postbud.KØ_MAX


def test_baade_grupperes_efter_havn():
    """Det er dét, man vil vide: ligger der nogen i Marstal i aften."""
    from app import harbours
    havn = harbours.search('Marstal', limit=1)[0]
    fleetmap.show('X', 'Havfruen', havn.lat, havn.lon)
    fleetmap.show('Y', 'Vinden', 55.0, 11.0)   # midt i Storebælt
    både = fleetmap.others('Z')
    grupper, undervejs = fleetmap.by_harbour(både)
    navne = {h.name for h, _ in grupper}
    assert havn.name in navne
    assert any(b.mark == 'Y' for b in undervejs)
    fleetmap.hide('X')
    fleetmap.hide('Y')
