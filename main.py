"""Opstart af Sejlplan.

Kør appen med:  python main.py
"""
from __future__ import annotations

from nicegui import ui

from app import pwa
from app.config import settings
from app.ui import page  # noqa: F401  – registrerer siden ved import

pwa.register_routes()

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
