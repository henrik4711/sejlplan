"""Bådvælgeren i indstillingerne.

Kortene bygges i en løkke over `SAILBOATS` og `MOTORBOATS`, så en ny båd i
`boats.py` skulle stå der af sig selv. »Skulle« er ikke godt nok, når det er
dét, brugeren vælger sin plan med: prøven her åbner dialogen og ser efter, at
hver eneste båd står på skærmen.
"""
from __future__ import annotations

import pytest
from nicegui import ui
from nicegui.testing import User

from app.boats import BOATS

pytestmark = pytest.mark.module_under_test('main')

RUTE = '/proeve-baadvalg'


def _siden_med_dialogen() -> None:
    """Forsiden med indstillingerne slået op med det samme.

    Dialogen åbnes ellers af et tryk på tandhjulet, og den knap kan prøven
    ikke ramme uden en browser. Den kaldes derfor direkte — det er samme
    funktion, knappen kalder.
    """
    from app.ui.planner import Planner
    from app.ui.settings import settings_dialog
    from app import theme
    theme.apply()
    planner = Planner()
    planner.build()
    settings_dialog(planner)


async def test_alle_baade_staar_i_vaelgeren(user: User):
    # Ruten lægges på her og ikke ved import: prøvefiksturet indlæser `main`
    # forfra og fejer siderne af bordet undervejs.
    ui.page(RUTE)(_siden_med_dialogen)
    await user.open(RUTE)
    for båd in BOATS.values():
        await user.should_see(båd.name)
