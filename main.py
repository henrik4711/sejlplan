"""Opstart af Sejlplan.

Kør appen med:  python main.py
"""
from __future__ import annotations

from nicegui import ui

from app.config import settings
from app.ui import page  # noqa: F401  – registrerer siden ved import

if __name__ in {'__main__', '__mp_main__'}:
    ui.run(
        title='Sejlplan',
        host=settings.host,
        port=settings.port,
        storage_secret=settings.storage_secret,
        favicon='⛵',
        dark=True,
        reload=False,
        show=False,
    )
