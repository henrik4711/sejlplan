"""Det gemte skal komme tilbage — hele vejen.

`Session.snapshot()` skrev datovinduet ned, og `Session.load()` læste alt
andet tilbage end netop det. En gemt plan åbnede derfor altid på
standardvinduet, uden at nogen fik det at vide: ingen fejl, ingen besked,
bare andre datoer end dem, man selv havde valgt.

Fejlen kunne ikke ses fra nogen af siderne hver for sig. Derfor prøver vi
rundturen: gem, læs ind igen, og hævd at det, der kom ud, er det, der gik ind.
Den form fanger også det næste felt, nogen glemmer.
"""
from __future__ import annotations

from datetime import date, timedelta

import pytest

from app.sailing import Waypoint
from app.state import MAX_FORECAST_DAYS, Session


def _session(**limits) -> Session:
    s = Session()
    s.waypoints = [Waypoint(lat=55.46, lon=12.28, name='Køge'),
                   Waypoint(lat=55.12, lon=12.04, name='Præstø')]
    for k, v in limits.items():
        setattr(s.limits, k, v)
    return s


# ── Rundturen ─────────────────────────────────────────────────────────────────
def test_hvert_gemt_graensefelt_kommer_tilbage():
    """Ingen felter må falde på gulvet undervejs.

    Datovinduet gjorde netop det. Prøven gennemgår hvert felt, `snapshot`
    skriver, i stedet for at nævne dem enkeltvis — så et nyt felt, der bliver
    gemt men ikke læst, falder her af sig selv.
    """
    i_morgen = date.today() + timedelta(days=1)
    om_tre = date.today() + timedelta(days=3)
    før = _session(max_wind=17.0, max_wave=1.2,
                   date_from=i_morgen.isoformat(), date_to=om_tre.isoformat(),
                   day_start=6, day_end=22, night_ok=True, use_motor=False)

    efter = Session().load(før.snapshot())

    for felt in før.snapshot()['limits']:
        assert getattr(efter.limits, felt) == getattr(før.limits, felt), \
            f'{felt} overlevede ikke en gem-og-hent'


def test_datovinduet_overlever():
    """Selve fejlen, skrevet ud for sig — den skal ikke kunne snige sig ind igen."""
    fra = (date.today() + timedelta(days=2)).isoformat()
    til = (date.today() + timedelta(days=5)).isoformat()
    efter = Session().load(_session(date_from=fra, date_to=til).snapshot())
    assert efter.limits.date_from == fra
    assert efter.limits.date_to == til


# ── Og hvis vi flytter det, skal det siges ────────────────────────────────────
def test_et_vindue_i_fortiden_flyttes_frem_og_siges_hoejt():
    i_går = (date.today() - timedelta(days=2)).isoformat()
    s = Session().load(_session(date_from=i_går,
                                date_to=date.today().isoformat()).snapshot())
    assert s.limits.date_from == date.today().isoformat()
    assert s.dates_moved == i_går, 'flytningen skete i stilhed'


def test_et_gyldigt_vindue_giver_ingen_besked():
    fra = (date.today() + timedelta(days=1)).isoformat()
    s = Session().load(_session(date_from=fra,
                                date_to=fra).snapshot())
    assert s.dates_moved == ''


def test_vinduet_kan_ikke_raekke_ud_over_prognosen():
    langt_ude = (date.today() + timedelta(days=90)).isoformat()
    s = Session().load(_session(date_from=langt_ude,
                                date_to=langt_ude).snapshot())
    horisont = date.today() + timedelta(days=MAX_FORECAST_DAYS - 1)
    assert date.fromisoformat(s.limits.date_from) <= horisont
    assert s.dates_moved == langt_ude


def test_noget_vaerre_end_en_dato_vaelter_ikke_noget():
    """Er det gemte i stykker, skal vi lande på standarden — ikke på en fejl."""
    d = _session().snapshot()
    d['limits']['date_from'] = 'ikke en dato'
    d['limits']['date_to'] = None
    s = Session().load(d)
    assert date.fromisoformat(s.limits.date_from) >= date.today()
    assert date.fromisoformat(s.limits.date_to) >= \
        date.fromisoformat(s.limits.date_from)
