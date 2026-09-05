"""Rangeringen skal kunne læses, ikke bare adlydes.

`score()` vejer ni ting mod hinanden, og resultatet var et tal, ingen så.
Atten afgangskort med samme grønne mærkat — hvor nr. 2 havde mindre vind end
nr. 1 — lignede en fejl i stedet for en afvejning.

`why_ranked()` regner den tungeste forskel ud og skriver den i ord. Prøverne
her hævder, at ordene passer til tallene: den, der koster mest, er også den,
der bliver nævnt.
"""
from __future__ import annotations

import re
from datetime import datetime, timedelta

import pytest

from app.sailing import Limits, Plan, Stop, why_ranked

I_MORGEN = datetime.now().replace(hour=7, minute=0, second=0, microsecond=0) \
    + timedelta(days=1)


def _plan(**kw) -> Plan:
    grund = dict(
        depart=I_MORGEN,
        arrival=I_MORGEN + timedelta(hours=6),
        total_nm=30.0, reached_nm=30.0, hours=6, under_way_h=6.0,
        avg_speed_kn=5.0, worst_wind_kn=14.0, worst_wave_m=0.6,
        red_hours=0, yellow_hours=0, night_hours=0, motor_hours=0, fuel_l=0.0,
    )
    grund.update(kw)
    return Plan(**grund)


LIMITS = Limits(max_wind=20.0, max_wave=1.5,
                date_from=I_MORGEN.date().isoformat(),
                date_to=(I_MORGEN.date() + timedelta(days=2)).isoformat())


def test_den_bedste_faar_ros_ikke_en_undskyldning():
    bedste = _plan()
    nøgle, _, art = why_ranked(bedste, bedste, LIMITS)
    assert art == 'god'
    assert nøgle == 'bedst'


def test_frarådede_timer_vejer_tungest():
    bedste = _plan()
    værre = _plan(red_hours=3, yellow_hours=1)
    nøgle, tal, art = why_ranked(værre, bedste, LIMITS)
    assert art == 'pris'
    assert nøgle == 'frarådet'
    assert tal['n'] == 3


def test_vind_over_graensen_bliver_nævnt_med_tallet():
    bedste = _plan()
    hård = _plan(worst_wind_kn=26.0)
    nøgle, tal, art = why_ranked(hård, bedste, LIMITS)
    assert art == 'pris'
    assert nøgle == 'vind' and tal['kn'] == '26'


def test_en_overnatning_mere_bliver_nævnt():
    bedste = _plan()
    lang = _plan(stops=[Stop(name='Rødvig', detail='Stevns', lat=55.2, lon=12.4,
                             arrive=I_MORGEN + timedelta(hours=5),
                             depart=I_MORGEN + timedelta(hours=20),
                             detour_nm=0.4, late=False)])
    nøgle, tal, art = why_ranked(lang, bedste, LIMITS)
    assert art == 'pris'
    assert nøgle == 'nætter' and tal['n'] == 1


def test_langsommere_i_snit_bliver_nævnt_naar_vejret_er_ens():
    bedste = _plan(avg_speed_kn=5.5)
    træg = _plan(avg_speed_kn=4.2)
    nøgle, tal, art = why_ranked(træg, bedste, LIMITS)
    assert art == 'pris'
    assert nøgle == 'langsommere' and tal['kn'] == '1,3'


def test_en_afgang_der_ikke_naar_frem_siger_hvor_langt_den_kom():
    bedste = _plan()
    kort = _plan(incomplete=True, reached_nm=18.0)
    nøgle, tal, art = why_ranked(kort, bedste, LIMITS)
    assert art == 'pris'
    assert nøgle == 'kort'
    assert tal == {'nået': '18', 'ialt': '30'}


def test_hver_noegle_kan_skrives_ud_paa_hvert_sprog():
    """Fladen slår nøglen op uden at spørge. Ingen af dem må mangle.

    Prøven går gennem `Planner._why_line`s egen tabel, så en ny nøgle i
    `why_ranked` uden en sætning i fladen falder her — ikke hos en bruger.
    """
    import inspect

    from app.ui.planner import Planner
    kilde = inspect.getsource(Planner._why_line)

    bedste = _plan()
    kandidater = (bedste,
                  _plan(depart=I_MORGEN + timedelta(hours=6)),
                  _plan(arrived_late=True),
                  _plan(yellow_hours=2),
                  _plan(worst_wave_m=2.1),
                  _plan(incomplete=True, reached_nm=4.0),
                  _plan(red_hours=1),
                  _plan(worst_wind_kn=30.0),
                  _plan(avg_speed_kn=3.0),
                  _plan(arrival=I_MORGEN + timedelta(hours=20)))
    set_noegler = set()
    for kandidat in kandidater:
        nøgle, tal, art = why_ranked(kandidat, bedste, LIMITS)
        assert art in ('god', 'pris', '')
        set_noegler.add(nøgle)
        assert f"'{nøgle}': lambda:" in kilde,             f'nøglen {nøgle} har ingen sætning i fladen'
    # Og den anden vej: ingen sætninger, der aldrig kan nås.
    i_fladen = set(re.findall(r"'(\w+)': lambda:", kilde))
    assert set_noegler <= i_fladen
