"""Bådene i vælgeren skal kunne bære en plan — og sige det på hvert sprog.

To ting går galt uden at larme, når en båd lægges til.

Polardiagrammet er en tabel skrevet i hånden. Mangler en vinkel eller en
vindstyrke, står der ingen fejl — planlæggeren finder bare en anden fart, og
turen bliver regnet forkert. Så prøven her holder hver båds diagram op mod
referencens: samme vinkler, samme vindstyrker, og farter i nærheden af det, et
skrog af den længde kan bære.

Bådens beskrivelse og det ene ord om, hvad den er god til, står som data og går
gennem `t()` først ude på kortet. Er de ikke i sprogtabellen, falder de tilbage
til dansk — kortet ser rigtigt ud, det står bare på det forkerte sprog. Derfor
slås de op her.
"""
from __future__ import annotations

import pytest

from app import i18n
from app.boats import BOATS, REFERENCE, SAILBOATS

FREMMEDE = [k for k in i18n.LANGUAGES if k != i18n.DA]

VINKLER = sorted(BOATS[REFERENCE].polar)
VINDE = sorted(BOATS[REFERENCE].polar[VINKLER[0]])

# Skrogfarten er en tommelfingerregel, ikke en mur: en let båd på rumskøde
# løber et stykke over den. Et cifferskifte i tabellen gør den derimod dobbelt
# så hurtig, og dét er det, prøven skal fange.
OVER_SKROGFART = 1.10


@pytest.mark.parametrize('nøgle', sorted(BOATS))
def test_baaden_kender_sit_eget_id(nøgle: str):
    """Vælgeren gemmer nøglen; alt andet slår båden op på `id`."""
    assert BOATS[nøgle].id == nøgle


@pytest.mark.parametrize('båd', SAILBOATS, ids=lambda b: b.id)
def test_polardiagrammet_er_helt(båd):
    assert sorted(båd.polar) == VINKLER, 'diagrammet mangler en vinkel'
    for vinkel, række in båd.polar.items():
        assert sorted(række) == VINDE, f'{vinkel}° mangler en vindstyrke'
        for vind, fart in række.items():
            assert 0 < fart <= båd.hull_speed_kn * OVER_SKROGFART, (
                f'{vinkel}° i {vind} kn giver {fart} kn — for meget for et '
                f'skrog med {båd.hull_speed_kn} kn skrogfart')


@pytest.mark.parametrize('kode', FREMMEDE)
@pytest.mark.parametrize('båd', list(BOATS.values()), ids=lambda b: b.id)
def test_bådens_ord_er_oversat(båd, kode: str):
    tabel = i18n._saml(kode)
    for tekst in (båd.desc, båd.crew_note):
        if tekst:
            assert tekst in tabel, f'{båd.name}: "{tekst}" mangler på {kode}'
