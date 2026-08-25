"""De tre dokumenter skal kunne skrives ud — på hvert sprog, der findes.

Den her fil findes, fordi den offline sejlplan var brudt i stilhed. `warnings()`
gav Note-objekter, ikke tekst, og `esc()` kalder `.replace` direkte — så hver
eneste plan med en advarsel rejste AttributeError. Planlæggeren sluger den fejl
med vilje (en plan, der ikke kunne gemmes til senere, må ikke forhindre, at man
ser den nu), og derfor opdagede ingen det: knappen virkede, dokumentet blev bare
aldrig lagt i telefonen.

Der er ingen påstand her om, at teksten er rigtig. Der er kun den påstand, at
den kan skrives — og det er præcis dét, der manglede.
"""
from __future__ import annotations

from datetime import datetime, timedelta

import pytest

from app import i18n, narrative, offline
from app.boats import BOATS, DEFAULT_BOAT
from app.sailing import Limits, Route, Waypoint, sail

# Alle sprog i vælgeren. Et nyt sprog er dækket, fra det står i
# `i18n.LANGUAGES` — ellers ville svensk kunne vælte den offline plan,
# uden at en eneste prøve sagde noget.
SPROG = list(i18n.LANGUAGES)


def _vejr(timer: int = 60) -> list[list[dict]]:
    """En prognose, der er hård nok til at udløse advarsler.

    Rigtige tal ville kræve netværk. Det her er en time-for-time række, der
    ligner den, Open-Meteo giver, med vind nok til at komme over grænserne.
    """
    start = datetime.now().replace(minute=0, second=0, microsecond=0)
    række = []
    for i in range(timer):
        række.append({
            'time': start + timedelta(hours=i),
            'wind_kn': 8 + (i % 20),          # topper over 20 knob
            'gust_kn': 12 + (i % 24),
            'wind_dir': (i * 17) % 360,
            'wave_m': 0.3 + (i % 7) * 0.3,    # topper over 1,5 meter
            'wave_dir': (i * 23) % 360,
            'cur_kn': 0.2,
            'cur_dir': (i * 11) % 360,
        })
    return [række, række, række]


@pytest.fixture
def plan():
    boat = BOATS[DEFAULT_BOAT]
    route = Route([Waypoint(55.456, 12.194, 'Køge'),
                   Waypoint(56.036, 12.614, 'Helsingør')])
    limits = Limits()
    start = datetime.now().replace(hour=limits.day_start, minute=0,
                                   second=0, microsecond=0)
    return boat, route, limits, sail(boat, route, start, _vejr(), limits)


@pytest.mark.parametrize('sprog', SPROG)
def test_offline_dokument_kan_skrives(plan, sprog):
    """Den her fangede fejlen: advarsler er Note, ikke tekst."""
    boat, route, limits, p = plan
    assert narrative.warnings(p, limits, boat), 'prøven skal have advarsler'
    with i18n.using(sprog):
        doc = offline.document(boat, route, p, limits)
    assert doc.startswith('<!doctype html>')
    assert len(doc) > 2000


@pytest.mark.parametrize('sprog', SPROG)
def test_ren_tekst_kan_skrives(plan, sprog):
    boat, route, limits, p = plan
    with i18n.using(sprog):
        tekst = narrative.as_text(boat, route, p, limits)
    assert len(tekst) > 1000


@pytest.mark.parametrize('sprog', SPROG)
def test_manualen_kan_skrives(sprog):
    from app.ui import help as helpui
    with i18n.using(sprog):
        doc = helpui.document()
    assert doc.startswith('<!doctype html>')
    assert len(doc) > 10000


def test_dansk_kommer_uaendret_igennem():
    """Nøglen er den danske sætning. Kommer den ikke uændret ud på dansk, er
    en dansk tekst blevet rettet uden at nøglen fulgte med."""
    from app.lang import de, de_manual, de_plan, de_ui
    alle = {**de.WORDS, **de_ui.WORDS, **de_manual.WORDS, **de_plan.WORDS}
    with i18n.using('da'):
        fejl = [k for k in alle
                if not k.endswith((i18n.PLURAL_MARK, i18n.SENTENCE_MARK))
                and i18n.t(k) != k]
    assert not fejl, fejl[:3]


def test_pladsholdere_er_de_samme_paa_begge_sprog():
    """En oversættelse, der mangler en pladsholder, falder tilbage til dansk
    uden at nogen opdager det. Tallene bliver rigtige, sproget forkert."""
    import re
    from app.lang import de, de_manual, de_plan, de_ui
    alle = {**de.WORDS, **de_ui.WORDS, **de_manual.WORDS, **de_plan.WORDS}
    felt = lambda s: set(re.findall(r'\{(\w+)\}', s))
    fejl = [k for k, v in alle.items()
            if not k.endswith((i18n.PLURAL_MARK, i18n.SENTENCE_MARK))
            and felt(k) != felt(v)]
    assert not fejl, fejl[:3]
