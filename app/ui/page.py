"""Sidedefinitionen.

`@ui.page` kører én gang pr. besøgende, så alt der oprettes herinde — også
`Planner` — tilhører netop den ene bruger.
"""
from __future__ import annotations

from nicegui import ui

from .. import pwa, share, theme
from ..boats import BOATS
from .planner import Planner


@ui.page('/')
async def index(rute: str = '') -> None:
    """Forsiden. `?rute=…` åbner en rute, nogen har delt."""
    ui.page_title('Sejlplan – find den bedste afgang')
    theme.apply()
    pwa.head()

    planner = Planner()

    # Et delelink er altid stærkest: det er dét, brugeren står med i hånden.
    # Ellers spørger vi browseren, om den har en rute liggende, som serveren har
    # glemt. Begge dele skal ske før `build`, så fladen bygges rigtigt fra
    # starten i stedet for at blive skiftet ud for øjnene af brugeren.
    if rute:
        waypoints, boat_id = share.decode_route(rute)
        if waypoints:
            planner.s.waypoints = waypoints
            if boat_id in BOATS:
                planner.s.boat_id = boat_id
            planner.s.invalidate()
            planner.s.persist()
        else:
            ui.notify('Delelinket kunne ikke læses', type='warning', position='bottom')

    await planner.s.adopt_browser_copy()

    planner.build()

    if rute and planner.s.waypoints:
        ui.notify(f'Rute åbnet: {planner.s.waypoints[0].name} → '
                  f'{planner.s.waypoints[-1].name}', position='bottom')
