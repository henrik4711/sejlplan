"""Sidedefinitionen.

`@ui.page` kører én gang pr. besøgende, så alt der oprettes herinde — også
`Planner` — tilhører netop den ene bruger.

Registreringen sker i `register()` og ikke som en bivirkning af at importere
modulet. Det er ikke pedanteri: da den lå i importen, kunne den ikke køres
igen. Prøverne genindlæser `main` for at bygge siden forfra, men `from app.ui
import page` var da en tom handling, ruten blev aldrig registreret på ny, og
`user.open('/')` faldt med "not found" — nogle gange, alt efter hvilken prøve
der havde importeret modulet først. Den slags fejl ser ud, som om prøven er
dårlig. Den var ikke; opsætningen var.
"""
from __future__ import annotations

from nicegui import context, ui

from .. import pwa, share, theme
from .. import i18n
from ..i18n import t
from ..boats import BOATS
from .planner import Planner


async def index(rute: str = '') -> None:
    """Forsiden. `?rute=…` åbner en rute, nogen har delt."""
    # Sproget skal stå fast, før der bliver tegnet noget — ellers bygges
    # fladen på ét sprog og skal skiftes ud for øjnene af brugeren. Det står i
    # en cookie, som følger med anmodningen, så der er ingenting at vente på.
    # Første udgave spurgte browseren med JavaScript, og det er præcis den
    # slags, der giver en blank side, når svaret udebliver.
    forespørgsel = getattr(context.client, 'request', None)
    i18n.adopt(getattr(forespørgsel, 'cookies', None) or {},
               (forespørgsel.headers.get('accept-language', '')
                if forespørgsel else ''))

    ui.page_title(t('Sejlplan – find den bedste afgang'))
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
            ui.notify(t('Delelinket kunne ikke læses'), type='warning',
                      position='bottom')

    planner.build()

    if rute and planner.s.waypoints:
        ui.notify(t('Rute åbnet: {fra} → {til}',
                    fra=planner.s.waypoints[0].name,
                    til=planner.s.waypoints[-1].name), position='bottom')

    # Først nu spørger vi browseren, om den har en rute liggende, som serveren
    # har glemt. Det stod før `build`, og så ventede hele siden på svaret —
    # kom det ikke, sad brugeren og kiggede på ingenting. Fandt vi noget,
    # tegnes fladen om; det er et blink, og det er kun, når der faktisk er
    # noget at redde.
    if not rute and await planner.s.adopt_browser_copy():
        planner.refresh(fit=True)


def register() -> None:
    """Læg forsiden på. Kaldes én gang ved opstart — og igen i prøverne."""
    ui.page('/')(index)
