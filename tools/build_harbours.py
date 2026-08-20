"""Byg havneregisteret, appen søger og planlægger i.

Køres når registeret skal opdateres. Resultatet lægges i
`app/data/harbours.json.gz` og følger med i repoet — appen henter aldrig
havnedata over nettet.

    python tools/build_harbours.py marinas.json countries.geojson

`marinas.json` er svaret fra Overpass på

    [out:json][timeout:240];
    ( nwr["leisure"="marina"]({{bbox}}); );
    out center tags;

kørt i tern hen over Nordeuropa (Overpass klarer ikke hele området i ét hug).
`countries.geojson` er Natural Earths `ne_10m_admin_0_countries` og bruges kun
til at sætte det rigtige land på en havn.

Hver havn gemmes som `[navn, farvand, land, bredde, længde, pladser]`. Farvandet
er det, en sejler ville sige — ikke postnummeret.
"""
from __future__ import annotations

import gzip
import json
import math
import sys
import unicodedata
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'app' / 'data' / 'harbours.json.gz'

# Udsnittet appen dækker – samme som kystlinjegitteret.
LAT0, LAT1 = 53.0, 62.0
LON0, LON1 = 4.0, 20.0

# Farvande, som danske sejlere navigerer efter. Havnen får navnet på det
# nærmeste af dem — bokse ville skulle overlappe, punkter behøver ikke.
WATERS: list[tuple[str, float, float]] = [
    ('Øresund', 55.85, 12.65),
    ('Øresund', 55.60, 12.75),
    ('Køge Bugt', 55.45, 12.35),
    ('Østersøen', 54.85, 12.40),
    ('Østersøen', 54.60, 11.30),
    ('Østersøen', 55.38, 13.30),      # Skånes sydkyst
    ('Østersøen', 55.95, 14.60),      # Hanöbukten
    ('Østersøen', 56.15, 15.60),      # Blekinge
    ('Bornholm', 55.15, 14.90),
    ('Smålandsfarvandet', 55.05, 11.60),
    ('Storebælt', 55.45, 11.00),
    ('Langelandsbælt', 54.90, 10.85),
    ('Det Sydfynske Øhav', 54.92, 10.30),
    ('Lillebælt', 55.30, 9.85),
    ('Flensborg Fjord', 54.85, 9.60),
    ('Als Fjord', 55.00, 9.75),
    ('Vejle Fjord', 55.68, 9.75),
    ('Horsens Fjord', 55.85, 10.05),
    ('Aarhus Bugt', 56.05, 10.45),
    ('Samsø Bælt', 55.85, 10.85),
    ('Sejerø Bugt', 55.85, 11.35),
    ('Isefjord', 55.75, 11.85),
    ('Roskilde Fjord', 55.80, 12.05),
    ('Kattegat', 56.60, 11.60),
    ('Kattegat', 57.20, 11.20),
    ('Mariager Fjord', 56.68, 10.15),
    ('Randers Fjord', 56.55, 10.35),
    ('Limfjorden', 56.85, 9.30),
    ('Limfjorden', 56.60, 8.60),
    ('Skagerrak', 57.80, 9.80),
    ('Jammerbugt', 57.30, 9.30),
    ('Nordsøen', 56.20, 8.00),
    ('Ringkøbing Fjord', 55.95, 8.20),
    ('Vadehavet', 55.25, 8.45),
    ('Kielerbugten', 54.45, 10.30),
    ('Femern Bælt', 54.55, 11.20),
]

MAX_WATER_NM = 42.0     # længere væk end det siger farvandsnavnet ikke noget

# Landenavne på dansk. Resten står som Natural Earth skriver dem.
COUNTRY_DA = {
    'Denmark': 'Danmark', 'Sweden': 'Sverige', 'Norway': 'Norge',
    'Germany': 'Tyskland', 'Poland': 'Polen', 'Netherlands': 'Holland',
    'Finland': 'Finland', 'Estonia': 'Estland', 'Latvia': 'Letland',
    'Lithuania': 'Litauen', 'United Kingdom': 'Storbritannien',
    'Russia': 'Rusland', 'Belgium': 'Belgien',
}

NM_PER_DEGREE = 60.0


def clean(name: str) -> str:
    """Ryd navnet op, så listen ikke fyldes med afdelingsnavne og forkortelser."""
    name = ' '.join(unicodedata.normalize('NFC', name).split())
    for prefix in ('Marina ', 'Yachthafen ', 'Jachthafen '):
        if name.startswith(prefix) and len(name) > len(prefix) + 3:
            name = name[len(prefix):]
    return name.strip(' -–·,')


def water_name(lat: float, lon: float) -> str:
    best, best_d = '', math.inf
    scale = math.cos(math.radians(lat))
    for name, wlat, wlon in WATERS:
        d = math.hypot(lat - wlat, (lon - wlon) * scale) * NM_PER_DEGREE
        if d < best_d:
            best, best_d = name, d
    return best if best_d <= MAX_WATER_NM else ''


def load_countries(path: Path) -> list[tuple[str, list]]:
    """Landegrænser klippet ned til vores udsnit, som simple ringe."""
    data = json.loads(path.read_text(encoding='utf-8'))
    out = []
    for feat in data.get('features', []):
        props = feat.get('properties') or {}
        name = props.get('NAME_EN') or props.get('NAME') or ''
        geom = feat.get('geometry') or {}
        polys = (geom.get('coordinates') or []) if geom.get('type') == 'MultiPolygon' \
            else [geom.get('coordinates') or []]
        rings = []
        for poly in polys:
            if not poly:
                continue
            ring = poly[0]
            lons = [p[0] for p in ring]
            lats = [p[1] for p in ring]
            if max(lons) < LON0 - 1 or min(lons) > LON1 + 1:
                continue
            if max(lats) < LAT0 - 1 or min(lats) > LAT1 + 1:
                continue
            rings.append(ring)
        if rings:
            out.append((COUNTRY_DA.get(name, name), rings))
    return out


def inside(ring: list, lat: float, lon: float) -> bool:
    """Stråleskydning: tæl hvor mange kanter en vandret linje skærer."""
    hit = False
    n = len(ring)
    for i in range(n):
        x1, y1 = ring[i]
        x2, y2 = ring[(i + 1) % n]
        if (y1 > lat) != (y2 > lat):
            if lon < x1 + (lat - y1) / (y2 - y1) * (x2 - x1):
                hit = not hit
    return hit


def country_of(countries, lat: float, lon: float) -> str:
    """Hvilket land havnen hører til.

    En havn ligger på vandet, og vandet hører ikke til noget land i Natural
    Earths polygoner. Rammer punktet forbi, prøver vi et par hundrede meter
    inde i alle retninger — der ligger kysten.
    """
    for radius in (0.0, 0.008, 0.02, 0.05):
        spots = [(lat, lon)] if radius == 0 else [
            (lat + dy * radius, lon + dx * radius * 1.7)
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1),
                           (0.7, 0.7), (0.7, -0.7), (-0.7, 0.7), (-0.7, -0.7))]
        for name, rings in countries:
            for ring in rings:
                if any(inside(ring, y, x) for y, x in spots):
                    return name
    return ''


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2

    raw = json.loads(Path(sys.argv[1]).expanduser().read_text(encoding='utf-8'))
    elements = raw.get('elements', raw) if isinstance(raw, dict) else raw
    countries = load_countries(Path(sys.argv[2]).expanduser()) if len(sys.argv) > 2 else []
    print(f'{len(elements)} elementer, {len(countries)} lande')

    seen: dict[tuple, list] = {}
    for el in elements:
        tags = el.get('tags') or {}
        name = clean(tags.get('name') or tags.get('seamark:name') or '')
        if len(name) < 2:
            continue

        lat = el.get('lat') or (el.get('center') or {}).get('lat')
        lon = el.get('lon') or (el.get('center') or {}).get('lon')
        if lat is None or lon is None:
            continue
        lat, lon = float(lat), float(lon)
        if not (LAT0 <= lat <= LAT1 and LON0 <= lon <= LON1):
            continue

        try:
            berths = int(''.join(c for c in str(tags.get('capacity', '')) if c.isdigit()) or 0)
        except ValueError:
            berths = 0

        # Samme havn optræder tit som både flade og punkt. Rund positionen af
        # til ~100 m og behold den med flest oplysninger.
        key = (round(lat, 3), round(lon, 3))
        row = [name, '', '', round(lat, 5), round(lon, 5), min(berths, 5000)]
        if key not in seen or berths > seen[key][5]:
            seen[key] = row

    harbours = list(seen.values())
    print(f'{len(harbours)} havne med navn')

    for row in harbours:
        row[1] = water_name(row[3], row[4])
        row[2] = country_of(countries, row[3], row[4])

    harbours.sort(key=lambda r: (r[2], r[1], r[0]))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(OUT, 'wt', encoding='utf-8') as f:
        json.dump(harbours, f, ensure_ascii=False, separators=(',', ':'))

    print(f'\n{OUT.relative_to(ROOT)}  {OUT.stat().st_size / 1000:.0f} kB')
    for land, n in Counter(r[2] or '(ukendt)' for r in harbours).most_common():
        print(f'  {n:5d}  {land}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
