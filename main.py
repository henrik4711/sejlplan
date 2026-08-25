"""Opstart af Sejlplan.

Kør appen med:  python main.py
"""
from __future__ import annotations

from nicegui import app, ui

from app import api, lookout, mishap, pwa
from app.config import settings
from app.ui import page
from app.ui import watchpages

mishap.install()
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
