"""Opsætning til prøverne.

`nicegui.testing` kan køre en side uden en browser: den bygger fladen i samme
proces og lader os læse, hvad der står på den. Det er dét, der skal til for at
fange en fejl som den, der væltede hele siden — modulerne importerede fint, det
var først, da siden blev bygget, at navnet manglede.
"""
from __future__ import annotations

import os
import tempfile

import pytest

# Skal stå før app importeres: databasen skal lægges et sted, prøverne må rode.
os.environ.setdefault('SEJLPLAN_DATA_DIR',
                      os.path.join(tempfile.gettempdir(), 'sejlplan-proever'))

pytest_plugins = ['nicegui.testing.plugin']


@pytest.fixture
def sprog():
    """Ryd sprogvalget mellem prøverne, så de ikke smitter af på hinanden."""
    from app import i18n
    i18n._TABLES.clear()
    yield
    i18n._TABLES.clear()
