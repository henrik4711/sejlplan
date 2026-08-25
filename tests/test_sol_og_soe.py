"""Solen og søens stejlhed.

To tal, ingen kan efterse i hånden, og som begge ændrer, hvad planen siger.
Solen afgør, om der står "sørg for lanterner"; stejlheden afgør, om en time
er grøn eller rød.
"""
from __future__ import annotations

from datetime import date, datetime

import pytest

from app import sun
from app.sailing import felt_wave, steepness_factor

# Kendte tider, slået op i en almanak. Et par minutters afvigelse er fint —
# vi skal afgøre, om der skal tændes lanterner, ikke navigere efter solen.
KENDTE = [
    # sted,        lat,    lon,   dato,             op,      ned
    ('København', 55.68, 12.57, date(2026, 6, 21), '04:26', '21:58'),
    ('København', 55.68, 12.57, date(2026, 12, 21), '08:37', '15:39'),
    ('Skagen', 57.72, 10.58, date(2026, 6, 21), '04:15', '22:22'),
    ('Gedser', 54.57, 11.93, date(2026, 6, 21), '04:35', '21:51'),
]


@pytest.mark.parametrize('sted,lat,lon,d,op,ned', KENDTE)
def test_solen_rammer_almanakken(sted, lat, lon, d, op, ned):
    tider = sun.sunrise_sunset(lat, lon, d)
    assert tider is not None
    faktisk_op, faktisk_ned = tider
    for faktisk, ventet, hvad in ((faktisk_op, op, 'solopgang'),
                                  (faktisk_ned, ned, 'solnedgang')):
        t, m = (int(x) for x in ventet.split(':'))
        afvigelse = abs((faktisk.hour * 60 + faktisk.minute) - (t * 60 + m))
        assert afvigelse <= 4, f'{sted} {hvad}: {faktisk:%H:%M} mod {ventet}'


def test_solen_gaar_senere_ned_mod_nord_om_sommeren():
    """Halvanden times forskel på Gedser og Skagen ved midsommer. Det er dét,
    et fast klokkeslæt ikke kunne fange."""
    d = date(2026, 6, 21)
    _, gedser = sun.sunrise_sunset(54.57, 11.93, d)
    _, skagen = sun.sunrise_sunset(57.72, 10.58, d)
    assert skagen > gedser
    assert (skagen - gedser).total_seconds() / 60 > 25


def test_midnatssol_og_polarnat():
    """Nordkap. Sejlplan kan lægge en rute derop, og så skal svaret passe."""
    assert sun.sunrise_sunset(71.17, 25.78, date(2026, 6, 21)) is None
    assert not sun.dark(71.17, 25.78, datetime(2026, 6, 21, 1, 0))
    assert sun.sunrise_sunset(71.17, 25.78, date(2026, 12, 21)) is None
    assert sun.dark(71.17, 25.78, datetime(2026, 12, 21, 12, 0))


def test_mørket_er_solen_ikke_uret():
    """Fejlen, det her retter: en aften i juni klokken ni er ikke mørke, og
    en aften sidst i september klokken halv otte er."""
    assert not sun.dark(57.72, 10.58, datetime(2026, 6, 21, 21, 0))
    assert sun.dark(57.72, 10.58, datetime(2026, 9, 25, 19, 30))


@pytest.mark.parametrize('time_', range(0, 24))
def test_mørket_er_sammenhaengende(time_):
    """Det bliver mørkt én gang i døgnet og lyst én gang. Ikke frem og
    tilbage — det ville betyde en fejl i sammenligningen."""
    d = date(2026, 8, 15)
    lat, lon = 55.68, 12.57
    op, ned = sun.sunrise_sunset(lat, lon, d)
    t = datetime(d.year, d.month, d.day, time_)
    assert sun.dark(lat, lon, t) == (t < op or t >= ned)


# ── Søens stejlhed ───────────────────────────────────────────────────────────
def test_kort_periode_foeles_haardere_end_lang():
    """Samme højde, to helt forskellige dage. Det er hele pointen."""
    assert steepness_factor(1.5, 4) > steepness_factor(1.5, 9)
    assert steepness_factor(1.5, 4) > 1.2
    assert steepness_factor(1.5, 9) < 0.85


def test_uden_periode_aendres_intet():
    """Mangler tallet, skal modellen opføre sig som før og ikke gætte."""
    for manglende in (None, 0, -1):
        assert steepness_factor(1.5, manglende) == 1.0
        assert felt_wave(1.5, 'modsø', manglende) == felt_wave(1.5, 'modsø')


@pytest.mark.parametrize('h', [0.2, 0.8, 1.5, 3.0, 6.0])
@pytest.mark.parametrize('s', [2, 4, 6, 9, 14, 20])
def test_faktoren_holder_sig_inden_for_graenserne(h, s):
    """Uden en grænse kunne en meget lang dønning regne en høj sø ned til
    ingenting — og det er den ikke."""
    f = steepness_factor(h, s)
    assert 0.75 <= f <= 1.35


def test_retningen_vejer_stadig_med():
    """Stejlheden lægges oveni retningen, den erstatter den ikke."""
    assert felt_wave(1.5, 'modsø', 5) > felt_wave(1.5, 'medsø', 5)
