"""Opsætning til prøverne.

`nicegui.testing` kan køre en side uden en browser: den bygger fladen i samme
proces og lader os læse, hvad der står på den. Det er dét, der skal til for at
fange en fejl som den, der væltede hele siden — modulerne importerede fint, det
var først, da siden blev bygget, at navnet manglede.
"""
from __future__ import annotations

import os
import pathlib
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


@pytest.fixture(autouse=True)
def ryd_sessionslager():
    """Tøm NiceGUI's sessionslager efter hver prøve.

    NiceGUI's prøvefikstur laver en midlertidig mappe og fjerner den bagefter
    med rmdir — som kræver, at den er tom. Skriver en prøve i
    `app.storage.user`, bliver der en fil tilbage, og så falder oprydningen
    med "mappen er ikke tom". Fejlen står på en prøve, der intet har gjort
    galt, og den kommer og går. Det er den slags, der gør, at folk holder op
    med at stole på prøverne.
    """
    yield
    from nicegui import app
    try:
        app.storage.user.clear()
    except Exception:
        pass
    # `clear()` tømmer ordbogen, men filen bliver liggende — og det er filen,
    # rmdir falder over. Så den skal væk.
    try:
        mappe = pathlib.Path(app.storage.path)
    except Exception:
        return
    if not mappe.is_dir() or 'nicegui-test-storage' not in mappe.name:
        return
    for fil in mappe.iterdir():
        try:
            if fil.is_file():
                fil.unlink()
        except OSError:
            pass
