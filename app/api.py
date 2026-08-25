"""Et lille HTTP-vindue ind til beskedtjenesten.

**Hvad der ikke er her, og hvorfor.** Der er ingen rute, der giver positioner
eller beskeder ud. En båds position er den mest følsomme oplysning, appen
håndterer — den siger også "her står et hjem tomt" og "her ligger nogen alene
på en øde ankerplads". Hele konstruktionen bygger på, at man kun kan se andre,
mens man selv er synlig, og at man skal have en session for at have et mærke.
En HTTP-rute, der leverede positioner mod et mærke i en URL, ville lægge det
mærke i serverlogs, i browserhistorik og i Referer-headere hos alle, man
klikkede videre til. Det er ikke en lille risiko, det er hele beskyttelsen.

Beskederne bliver leveret over den forbindelse, browseren har i forvejen —
NiceGUI's egen, som allerede er knyttet til sessionen. Postbuddet er den
asynkrone tjeneste; det her er kun vinduet, man kan kigge ind ad.

Skal der en dag være en rigtig klient udefra — en app, en plotter — er vejen
et token, brugeren selv laver og kan trække tilbage, sendt i en
Authorization-header. Ikke et mærke i en URL.
"""
from __future__ import annotations

import json
from datetime import datetime

from fastapi import Response
from nicegui import app

from . import chat, fleetmap, postbud
from .config import settings

_startet = datetime.now()


def _svar(data: dict) -> Response:
    return Response(json.dumps(data, ensure_ascii=False, indent=1),
                    media_type='application/json; charset=utf-8')


def register_routes() -> None:
    """Kaldes én gang ved opstart."""

    @app.get('/api/status')
    def _status() -> Response:
        """Kører tjenesten, og er der nogen på vandet?

        Tal, ikke navne: hvor mange både der er synlige, hvor mange browsere
        der lytter, og hvor længe serveren har kørt. Ingenting herinde kan
        pege på en enkelt båd.
        """
        oppe = (datetime.now() - _startet).total_seconds()
        data = {
            'oppe_sekunder': round(oppe),
            'lager': bool(settings.storage_dir),
            'postbud': {
                'lyttere': postbud.lyttere(),
                'levering': 'øjeblikkelig',
            },
        }
        if fleetmap.available():
            try:
                data['både_synlige'] = fleetmap.count()
            except Exception:
                data['både_synlige'] = None
        return _svar(data)

    @app.get('/api/sundhed')
    def _sundhed() -> Response:
        """Til overvågning: svarer serveren, og kan den nå sit lager?"""
        ok = True
        if fleetmap.available():
            try:
                fleetmap.count()
            except Exception:
                ok = False
        return _svar({'ok': ok, 'chat': chat.available()})
