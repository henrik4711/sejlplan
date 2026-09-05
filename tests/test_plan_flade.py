"""Sejlplanens flade: rækkefølgen, begrundelserne og "hvad nu".

Tre ting, der før var forkerte, og som ingen prøve ville have fanget:

* Skippervurderingen — det bedste indhold i produktet — lå nederst bag en
  lukket harmonika, hvor en førstegangsbruger aldrig fandt den.
* Atten afgangskort så fuldstændig ens ud. Rangeringen var et tal, ingen så.
* Bunden af planen var en knap, der lavede den samme analyse om igen. Der
  stod intet om, hvad man ellers kunne gøre.

Prøverne bygger fladen uden en browser og læser, hvad der faktisk står. De
bruger en fast plan og et fast vejr, så de hverken rører nettet eller
afhænger af, hvad vinden gør i dag.
"""
from __future__ import annotations

import inspect
import re
from datetime import datetime, timedelta

import pytest

from app.sailing import Limits, Plan, Segment
from app.ui.planner import Planner

I_MORGEN = (datetime.now() + timedelta(days=1)).replace(
    hour=7, minute=0, second=0, microsecond=0)


def _kode(fn) -> str:
    """Kilden uden kommentarer og docstring.

    Prøverne herunder handler om, hvad koden gør — ikke om, hvad der står i
    kommentarerne. Uden det her falder en prøve, fordi en kommentar nævner
    den tekst, den skal sikre sig ikke bliver tegnet.
    """
    kilde = inspect.getsource(getattr(fn, 'func', fn))
    kilde = re.sub(r'"""(?!\s*\n\s*def).*?"""', '', kilde, count=1, flags=re.S)
    return '\n'.join(linje.split('#')[0] for linje in kilde.splitlines())


def _segment(time: datetime, along: float) -> Segment:
    return Segment(
        time=time, leg=0, along_nm=along, lat=55.3, lon=12.2,
        course=139, twa=145, wind_kn=13.0, wind_dir=300, gust_kn=18.0,
        wave_m=0.6, sea='let', felt_m=0.6, speed_kn=5.0, through_kn=4.8,
        cur_kn=0.3, cur_along_kn=0.2, status='go', motoring=False,
        night=False)


def _plan(depart: datetime, **kw) -> Plan:
    timer = kw.pop('hours', 6)
    grund = dict(
        depart=depart,
        arrival=depart + timedelta(hours=timer),
        total_nm=30.0, reached_nm=30.0, hours=timer,
        under_way_h=float(timer), avg_speed_kn=5.0,
        worst_wind_kn=14.0, worst_wave_m=0.6,
        red_hours=0, yellow_hours=0, night_hours=0, motor_hours=0, fuel_l=0.0,
        segments=[_segment(depart + timedelta(hours=i), i * 5.0)
                  for i in range(timer)],
    )
    grund.update(kw)
    return Plan(**grund)


# ── Begrundelsen på hvert afgangskort ─────────────────────────────────────────
def test_hvert_afgangskort_faar_en_begrundelse():
    """Rangeringen skal kunne læses. Uden linjen er den et tal, ingen ser."""
    p = Planner.__new__(Planner)          # ingen browser, kun metoden
    p.s = type('S', (), {'limits': Limits(
        max_wind=20.0, max_wave=1.5,
        date_from=I_MORGEN.date().isoformat(),
        date_to=I_MORGEN.date().isoformat())})()

    bedste = _plan(I_MORGEN)
    for kandidat, forventet in (
            (bedste, 'win-why--god'),
            (_plan(I_MORGEN, red_hours=3), 'win-why--pris'),
            (_plan(I_MORGEN, worst_wind_kn=27.0), 'win-why--pris'),
            (_plan(I_MORGEN + timedelta(hours=5), hours=9), 'win-why--pris')):
        linje = p._why_line(kandidat, bedste)
        assert forventet in linje
        assert 'win-why-ico' in linje
        # Der skal stå ord, ikke bare et mærke.
        assert len(linje.split('</span>')[-1].replace('</div>', '').strip()) > 8


def test_maerkaten_forsvinder_naar_den_ikke_siger_noget():
    """"Gode forhold" på alle atten kort er støj, ikke information."""
    p = Planner.__new__(Planner)
    ens = [_plan(I_MORGEN + timedelta(hours=i)) for i in range(4)]
    p.s = type('S', (), {'windows': ens})()
    assert not p._verdict_varies()

    blandet = ens + [_plan(I_MORGEN, red_hours=2)]
    p.s = type('S', (), {'windows': blandet})()
    assert p._verdict_varies()


# ── Rækkefølgen i sejlplanen ──────────────────────────────────────────────────
def test_skippervurderingen_staar_foer_noegletallene():
    """Det, man kom efter, skal møde én først — ikke nederst bag en harmonika."""
    kilde = _kode(Planner.plan_view)
    for tidlig, sen in (('_ai_tab', '_plan_overview'),
                        ('_ai_tab', '_key_figures'),
                        ('_ai_tab', '_weather_tab'),
                        ('_weather_tab', '_next_actions')):
        assert kilde.index(f'self.{tidlig}(') < kilde.index(f'self.{sen}('), \
            f'{tidlig} skal stå før {sen}'


def test_vurderingens_tom_tilstand_ligger_i_den_del_der_tegnes_om():
    """Ellers bliver "Få en skippervurdering" stående oven på den færdige.

    Fejlen var, at kun `ai_output` var opdaterbar, mens tom-tilstanden og
    knapteksten blev tegnet i `_ai_tab`, som aldrig blev tegnet om.
    """
    ud = _kode(Planner.ai_output)
    assert 'Få en skippervurdering' in ud, 'tom-tilstanden tegnes ikke om'
    assert 'Lav vurderingen om' in ud, 'knapteksten tegnes ikke om'
    assert 'ai-wait' in ud, 'ingen ventetilstand, hvor svaret kommer'

    tab = _kode(Planner._ai_tab)
    assert 'Få en skippervurdering' not in tab
    assert 'ui.button' not in tab


def test_vurderingen_hentes_af_sig_selv_naar_planen_staar():
    assert '_maybe_run_ai' in _kode(Planner._go_to_step)
    assert '_maybe_run_ai' in _kode(Planner._select_window)
    # Og den må ikke hentes to gange for den samme afgang.
    assert '_ai_done_for' in _kode(Planner._maybe_run_ai)


# ── Hvad nu ───────────────────────────────────────────────────────────────────
def test_planen_slutter_med_noget_at_gaa_videre_med():
    kilde = _kode(Planner._next_actions)
    for handler in ('_save_route', '_open_watch', '_copy_link'):
        assert f'self.{handler}' in kilde, f'{handler} mangler under "Hvad nu"'


@pytest.mark.parametrize('navn', ['_save_route', '_open_watch', '_copy_link'])
def test_handlingerne_findes_faktisk(navn):
    """En knap, der peger på en metode, der ikke findes, fejler først ved klik."""
    assert callable(getattr(Planner, navn))
