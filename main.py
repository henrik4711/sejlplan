"""Opstart af Sejlplan.

Kør appen med:  python main.py
"""
from __future__ import annotations

from nicegui import app, ui

from app import api, config, landing, lookout, mishap, pwa
from app.config import settings
from app.ui import page
from app.ui import watchpages


def _sig_hvad_der_er_aabent() -> None:
    """Skriv i loggen, hvad der er åbent, og hvad der er lukket.

    En funktion, der er lukket med vilje, må ikke ligne en, der er i stykker.
    Står det i opstartslinjen, kan man se det uden at gætte — og uden at
    lede efter en knap, der ikke er tegnet.
    """
    navne = {config.FLÅDE: 'SEJLPLAN_FLAADE',
             config.PLADSMELDING: 'SEJLPLAN_PLADSMELDING',
             config.BESKEDER: 'SEJLPLAN_BESKEDER'}
    for hvad, er_åben in config.fællesskab().items():
        tilstand = 'åben' if er_åben else f'lukket (åbn med {navne[hvad]}=til)'
        print(f'Sejlplan · {hvad}: {tilstand}')


mishap.install()
_sig_hvad_der_er_aabent()
# Forsiden skal ligge paa plads foer planlaeggeren: den ejer `/`,
# og planlaeggeren ejer `/planlaeg`.
landing.register()
page.register()
pwa.register_routes()
api.register_routes()
watchpages.register()
app.on_startup(lookout.start)

if __name__ in {'__main__', '__mp_main__'}:
    ui.run(
        title='Sejlplan',
        host=settings.host,
        port=settings.port,
        storage_secret=settings.storage_secret,
        # `viewport-fit=cover` lader siden gaa helt ud i kanterne paa en
        # iPhone. Uden den er env(safe-area-*) altid nul, og saa kan vi
        # ikke holde headeren fri af statuslinjen og urskiven.
        viewport='width=device-width, initial-scale=1, viewport-fit=cover',
        favicon='⛵',
        dark=True,
        reload=False,
        show=False,
    )
