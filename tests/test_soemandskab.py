"""Sømærker og sejltrim.

Det her er den eneste del af Sejlplan, hvor teksten kan gøre fysisk skade.
Står der "sæt bomholder" på læns, er det ikke pynt — det er dét, der afgør, om
bommen kommer over hovedet på nogen. Så prøven siger, at rådet findes, hvor det
skal, og at det aldrig er tomt.
"""
from __future__ import annotations

import pytest

from app import i18n, seamanship as sm, trim

VINKLER = list(range(0, 181, 5))
STYRKER = [0, 3, 7, 9, 13, 15, 19, 21, 25, 27, 35, 50]


@pytest.mark.parametrize('twa', VINKLER)
@pytest.mark.parametrize('kn', STYRKER)
def test_der_er_altid_et_raad(twa, kn):
    """Ingen kombination må give ingenting eller en tom sætning."""
    r = trim.advise(twa, kn)
    assert r is not None
    assert r.sail and r.watch and r.reef
    for navn, tekst in r.rows:
        assert navn and tekst, f'{navn!r} er tom ved {twa}° / {kn} kn'


@pytest.mark.parametrize('twa', [t for t in VINKLER if t >= 100])
@pytest.mark.parametrize('kn', [5, 12, 20, 30])
def test_bomholder_paa_alt_fra_rumskoeds_og_ned(twa, kn):
    """Fra rumskøds og ned mod læns er bomvendingen risikoen.

    Det er dét, der slår folk ned. Nævnes det ikke, er rådet ikke færdigt.
    """
    r = trim.advise(twa, kn)
    assert 'bomholder' in r.warning.lower(), f'ingen advarsel ved {twa}°'


@pytest.mark.parametrize('twa', [t for t in VINKLER if t < 100])
def test_ingen_bomholder_paa_kryds(twa):
    """En advarsel, der står alle steder, bliver ikke læst nogen steder."""
    assert not trim.advise(twa, 15).warning


@pytest.mark.parametrize('kn', [30, 40, 60])
def test_haard_vind_giver_reb(kn):
    for twa in (40, 90, 150):
        assert 'reb' in trim.advise(twa, kn).reef.lower()


def test_motorbaad_faar_ingen_trim():
    from app.boats import MOTORBOATS
    motor = (MOTORBOATS[0] if isinstance(MOTORBOATS, (list, tuple))
             else next(iter(MOTORBOATS.values())))
    assert motor.is_motor
    assert trim.advise(90, 12, motor) is None


def test_sejlstillingen_passer_med_planen():
    """Trimmet og timetabellen skal aldrig kunne blive uenige om, hvad man
    sejler for — de skal bruge de samme grænser."""
    from app.sailing import point_of_sail
    for twa in VINKLER:
        assert trim.advise(twa, 12).sail == point_of_sail(twa)


# ── Sømærkerne ───────────────────────────────────────────────────────────────
def test_alle_maerker_er_hele():
    for m in sm.MARKS:
        assert m.name and m.meaning and m.action and m.light
        assert m.svg.startswith('<svg') and m.svg.endswith('</svg>')


def test_kardinalmaerkerne_siger_hvilken_side():
    """Et kardinalmærke, der ikke siger hvilken vej man skal gå, er ubrugeligt."""
    for id_, side in (('nord', 'nord'), ('syd', 'syd'),
                      ('øst', 'øst'), ('vest', 'vest')):
        m = next(x for x in sm.MARKS if x.id == id_)
        assert side in m.action.lower()


@pytest.mark.parametrize('sprog', ['da', 'de'])
def test_alt_kan_skrives_ud_paa_begge_sprog(sprog):
    with i18n.using(sprog):
        for m in sm.MARKS:
            for felt in (m.name, m.meaning, m.action, m.light):
                assert i18n.t(felt).strip()
        for gruppe in (sm.LANTERNS, sm.DAY_SHAPES, sm.SOUND_MANOEUVRE,
                       sm.SOUND_FOG, sm.DISTRESS):
            for s in gruppe:
                assert i18n.t(s.what).strip() and i18n.t(s.means).strip()


def test_tysk_bruger_de_tyske_soemandsord():
    """Ikke oversættelser af de danske ord — de ord, der står i den tyske
    lærebog. Går de tabt ved en omskrivning, skal det opdages her."""
    with i18n.using('de'):
        assert 'Bullenstander' in i18n.t(trim.advise(170, 15).warning)
        assert 'Patenthalse' in i18n.t(trim.advise(170, 15).warning)
        fare = next(m for m in sm.MARKS if m.id == 'fare')
        assert i18n.t(fare.name) == 'Einzelgefahrenzeichen'


# ── Tegningen ────────────────────────────────────────────────────────────────
# En tegning, der viser sejlene i den forkerte side, er værre end ingen
# tegning: den, der er i tvivl, er præcis den, der ikke opdager fejlen.
def _bom_punkt(svg: str) -> tuple[float, float]:
    """Bommens yderste punkt ud af tegningen."""
    import re
    m = re.search(r'<line x1="([\d.]+)" y1="([\d.]+)" x2="([\d.-]+)" '
                  r'y2="([\d.-]+)" stroke="#3A4252"', svg)
    assert m, 'ingen bom i tegningen'
    return float(m.group(3)), float(m.group(4))


@pytest.mark.parametrize('twa', [40, 60, 90, 120, 150, 180])
def test_bommen_staar_i_lae(twa):
    """Vinden fra styrbord betyder bommen i bagbord — altså til venstre i
    tegningen, hvor stævnen vender opad."""
    x, _y = _bom_punkt(trim.diagram(twa, 'styrbords halse'))
    assert x < trim._MIDTE_X, f'bommen står i luv ved {twa}°'
    x, _y = _bom_punkt(trim.diagram(twa, 'bagbords halse'))
    assert x > trim._MIDTE_X, f'bommen står i luv ved {twa}°'


@pytest.mark.parametrize('twa', [40, 60, 90, 120, 150, 180])
def test_bommen_staar_agter_for_masten(twa):
    _x, y = _bom_punkt(trim.diagram(twa))
    assert y > trim._MAST_Y, 'bommen peger fremad'


def test_bomvinklen_vokser_med_vindvinklen():
    """Jo længere agterind vinden kommer, jo længere ude står bommen. Er den
    ikke monoton, er der en fejl i opslagstabellen."""
    vinkler = [trim.boom_angle(t) for t in range(0, 181, 5)]
    assert vinkler == sorted(vinkler)
    assert vinkler[0] == 0 and vinkler[-1] > 70


def test_i_vindoejet_tegnes_uden_bom():
    """Der er ingen sejlføring at vise — der er en beslutning at træffe."""
    svg = trim.diagram(20)
    assert 'stroke="#3A4252"' not in svg


@pytest.mark.parametrize('twa', [0, 20, 45, 90, 135, 180])
def test_tegningen_holder_sig_inden_for_rammen(twa):
    """Et element uden for viewBox bliver klippet væk, og så mangler der
    noget uden at nogen kan se hvad."""
    import re
    svg = trim.diagram(twa)
    tal = [float(x) for x in re.findall(r'[xy][12]?="(-?[\d.]+)"', svg)]
    assert tal, 'ingen koordinater'
    assert min(tal) >= -1, f'noget stikker ud til venstre eller op: {min(tal)}'
    assert max(tal) <= max(trim.BÅD_BREDDE, trim.BÅD_HØJDE) + 1
