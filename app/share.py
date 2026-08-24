"""Deling og eksport af en rute.

En rute skal kunne forlade appen: som et link man sender til gasten, og som en
GPX-fil kortplotteren kan læse.

GPX-filen indeholder både brugerens egne punkter som waypoints og hele den
sejlbare rute som rutepunkter — også de knæk, ruteberegningen har lagt ind for
at komme udenom land. Det er dem, plotteren skal styre efter; ville man have
luftlinjen, behøvede man ikke appen.
"""
from __future__ import annotations

import base64
import json
import zlib
from datetime import datetime
from xml.sax.saxutils import escape

from .i18n import t
from .sailing import Route, Waypoint


# ── Delelink ──────────────────────────────────────────────────────────────────
def encode_route(waypoints: list[Waypoint], boat_id: str = '') -> str:
    """Pak ruten til en kort, URL-sikker streng.

    Koordinater rundes til 4 decimaler (ca. 10 m) — rigeligt til en ruteplan og
    det halverer linkets længde.
    """
    payload = {
        'b': boat_id,
        'w': [[round(w.lat, 4), round(w.lon, 4), w.name] for w in waypoints],
    }
    raw = json.dumps(payload, separators=(',', ':'), ensure_ascii=False).encode('utf-8')
    return base64.urlsafe_b64encode(zlib.compress(raw, 9)).decode('ascii').rstrip('=')


def decode_route(token: str) -> tuple[list[Waypoint], str]:
    """Læs en rute tilbage fra et delelink. Returnerer ([], '') hvis den er ugyldig."""
    try:
        padded = token + '=' * (-len(token) % 4)
        raw = zlib.decompress(base64.urlsafe_b64decode(padded))
        payload = json.loads(raw)
        waypoints = [Waypoint(float(lat), float(lon), str(name))
                     for lat, lon, name in payload.get('w', [])]
        return waypoints, str(payload.get('b') or '')
    except (ValueError, TypeError, zlib.error, KeyError):
        return [], ''


# ── GPX ───────────────────────────────────────────────────────────────────────
def to_gpx(route: Route, route_name: str = 'Sejlplan') -> str:
    """Byg en GPX 1.1-fil med brugerens punkter og hele den sejlbare rute."""
    stamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    name = escape(route_name)

    points = '\n'.join(
        f'  <wpt lat="{w.lat:.6f}" lon="{w.lon:.6f}">\n'
        f'    <name>{escape(w.name)}</name>\n'
        f'    <sym>Anchor</sym>\n'
        f'  </wpt>'
        for w in route.waypoints)

    # Samme vej lagt to gange. En rute er dét, plotteren navigerer efter, og et
    # spor er dét, mange programmer tegner. Der findes plottere, der kun læser
    # det ene, og filen skal virke i dem alle.
    track = '\n'.join(
        f'      <trkpt lat="{lat:.6f}" lon="{lon:.6f}" />'
        for lat, lon, _label in route_points(route))

    legs = '\n'.join(
        f'    <rtept lat="{lat:.6f}" lon="{lon:.6f}">\n'
        f'      <name>{escape(label)}</name>\n'
        f'    </rtept>'
        for lat, lon, label in route_points(route))

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<gpx version="1.1" creator="Sejlplan" xmlns="http://www.topografix.com/GPX/1/1"
     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
     xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">
  <metadata>
    <name>{name}</name>
    <time>{stamp}</time>
  </metadata>
{points}
  <rte>
    <name>{name}</name>
{legs}
  </rte>
  <trk>
    <name>{name}</name>
    <trkseg>
{track}
    </trkseg>
  </trk>
</gpx>
"""


def route_points(route: Route) -> list[tuple[float, float, str]]:
    """Rutepunkterne i rækkefølge. Brugerens egne beholder deres navne."""
    out: list[tuple[float, float, str]] = []
    knee = 0
    for leg, track in enumerate(route.tracks):
        for i, (lat, lon) in enumerate(track):
            if i == 0:
                out.append((lat, lon, route.waypoints[leg].name))
            elif i < len(track) - 1:
                knee += 1
                out.append((lat, lon, t('Knæk {nr}', nr=knee)))
            # Sidste punkt i et ben er første punkt i det næste – tages dér.
    last = route.waypoints[-1]
    out.append((last.lat, last.lon, last.name))
    return out


def filename(waypoints: list[Waypoint]) -> str:
    """Et filnavn der siger hvad ruten er, uden specialtegn."""
    if not waypoints:
        return 'sejlplan.gpx'
    ends = f'{waypoints[0].name}-{waypoints[-1].name}' if len(waypoints) > 1 else waypoints[0].name
    safe = ''.join(c if c.isalnum() or c in '-_' else '-' for c in ends.lower()
                   .replace('æ', 'ae').replace('ø', 'oe').replace('å', 'aa'))
    while '--' in safe:
        safe = safe.replace('--', '-')
    return f'sejlplan-{safe.strip("-")}.gpx'
