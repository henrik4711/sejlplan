"""Byg det land/vand-gitter, ruteberegningen bruger.

Køres én gang, når kystlinjedataene skal opdateres. Resultatet lægges i
`app/data/landmask.bin` og følger med i repoet — appen henter aldrig
kystlinjer over nettet.

    python tools/build_landmask.py ~/Downloads/gshhs_f.b

Værktøjet bruger numpy og scipy. Appen selv nøjes med numpy.

Kilden er GSHHG i fuld opløsning (gshhs_f.b) fra
<https://www.soest.hawaii.edu/pwessel/gshhg/>, udgivet under LGPL. Filen fylder
knap 100 MB og hører derfor ikke hjemme i repoet — kun det færdige gitter gør.

Formatet er så enkelt som det kan blive: en JSON-header med gitterets
udstrækning, efterfulgt af én bit pr. celle, zlib-pakket. Bit sat = land.
"""
from __future__ import annotations

import json
import struct
import sys
import time
import zlib
from pathlib import Path

import numpy as np
from scipy import ndimage

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'app' / 'data' / 'landmask.bin'

# Skandinaviske farvande med god margen: Nordsøen i vest, Ålands hav i øst,
# Vadehavet i syd og Trondheimsfjorden i nord.
LAT0, LAT1 = 53.0, 62.0
LON0, LON1 = 4.0, 20.0
RES = 0.002          # ~220 m i nord/syd, ~125 m i øst/vest på disse breddegrader

MAGIC = b'SJPMASK1'

# GSHHG-niveauer: 1 = kyst, 2 = sø, 3 = ø i sø, 4 = dam på ø i sø.
# Kun niveau 1 tegnes. Søer bliver dermed land, og det er det rigtige her: en
# sø er ikke farvand man kan sejle til fra havet, og lod vi den stå som vand,
# kunne ruteberegningen finde på at bruge den som smutvej henover et næs.


def read_polygons(path: Path):
    """Læs GSHHG's binære format. Returnerer (niveau, lon[], lat[]) pr. polygon."""
    raw = np.fromfile(path, dtype='>i4')
    i, out = 0, []
    while i < len(raw):
        n, flag = int(raw[i + 1]), int(raw[i + 2])
        west, east = int(raw[i + 3]) / 1e6, int(raw[i + 4]) / 1e6
        south, north = int(raw[i + 5]) / 1e6, int(raw[i + 6]) / 1e6
        level = flag & 0xFF
        head = i + 11
        i = head + 2 * n

        if level != 1 or north < LAT0 or south > LAT1:
            continue
        # Polygoner om Greenwich gemmes i 0-360. Skub dem til -180..180, så de
        # ligger i samme talrum som vores udsnit.
        if west > 180:
            west, east = west - 360, east - 360
        if east < LON0 or west > LON1:
            continue

        pts = raw[head:i].reshape(n, 2).astype(np.float64) / 1e6
        lon = pts[:, 0]
        lon = np.where(lon > 180, lon - 360, lon)
        out.append((level, lon, pts[:, 1]))
    return out


def fill(mask: np.ndarray, lon: np.ndarray, lat: np.ndarray, value: bool) -> None:
    """Scanline-udfyldning af én polygon med lige/ulige-reglen.

    Kanterne lægges i bunker efter hvilke rækker de skærer, så en polygon på
    en million punkter kun koster arbejde på de rækker den faktisk rører.
    """
    nrows, ncols = mask.shape

    y1, y2 = lat, np.roll(lat, -1)
    x1, x2 = lon, np.roll(lon, -1)

    lo, hi = np.minimum(y1, y2), np.maximum(y1, y2)
    r_from = np.ceil((lo - LAT0) / RES - 0.5)
    r_to = np.ceil((hi - LAT0) / RES - 0.5)
    np.clip(r_from, 0, nrows, out=r_from)
    np.clip(r_to, 0, nrows, out=r_to)
    r_from, r_to = r_from.astype(np.int32), r_to.astype(np.int32)

    live = (y1 != y2) & (r_to > r_from)
    if not live.any():
        return
    idx = np.flatnonzero(live)
    x1, x2, y1, y2 = x1[idx], x2[idx], y1[idx], y2[idx]
    r_from, r_to = r_from[idx], r_to[idx]

    order = np.argsort(r_from, kind='stable')
    starts = r_from[order]
    slope = (x2 - x1) / (y2 - y1)

    active = np.empty(0, dtype=np.int64)
    p = 0
    first, last = int(starts[0]), int(r_to.max())

    for r in range(first, last):
        step = np.searchsorted(starts, r, side='right')
        if step > p:
            active = np.concatenate((active, order[p:step]))
            p = int(step)
        if active.size:
            active = active[r_to[active] > r]
        if not active.size:
            continue

        yc = LAT0 + (r + 0.5) * RES
        xs = np.sort(x1[active] + (yc - y1[active]) * slope[active])

        cols = np.ceil((xs - LON0) / RES - 0.5)
        np.clip(cols, 0, ncols, out=cols)
        cols = cols.astype(np.int32)
        row = mask[r]
        for a, b in zip(cols[0::2], cols[1::2]):
            if b > a:
                row[a:b] = value


def open_sea(mask: np.ndarray) -> None:
    """Luk alt vand, der ikke hænger sammen med havet.

    Havnebassiner ligger bag moler, og moler er land i kystlinjedataene. Et
    bassin bliver derfor en lille sø af vand, man ikke kan sejle ind i — og
    lagde ruteberegningen sit endepunkt dér, kunne den aldrig nå frem. Vi
    beholder den store sammenhængende vandflade og det vand, der løber ud over
    udsnittets kant, og gør resten til land. Det vand var alligevel ikke til
    at sejle til.
    """
    labels, count = ndimage.label(~mask)
    if count < 2:
        return

    keep = set(np.unique(np.concatenate([
        labels[0], labels[-1], labels[:, 0], labels[:, -1]])).tolist())
    sizes = np.bincount(labels.ravel())
    sizes[0] = 0
    keep.add(int(np.argmax(sizes)))
    keep.discard(0)

    closed = ~np.isin(labels, sorted(keep)) & ~mask
    print(f'  lukker {int(closed.sum())} celler indelukket vand')
    mask |= closed


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    source = Path(sys.argv[1]).expanduser()
    if not source.exists():
        print(f'Findes ikke: {source}')
        return 2

    t0 = time.time()
    print(f'Læser {source.name} …')
    polygons = read_polygons(source)
    print(f'  {len(polygons)} polygoner i udsnittet   ({time.time() - t0:.1f}s)')

    nrows = int(round((LAT1 - LAT0) / RES))
    ncols = int(round((LON1 - LON0) / RES))
    mask = np.zeros((nrows, ncols), dtype=bool)
    print(f'Tegner {nrows} × {ncols} celler …')

    batch = [p for p in polygons if p[0] == 1]
    for _lvl, lon, lat in batch:
        fill(mask, lon, lat, True)
    print(f'  {len(batch)} kystpolygoner   ({time.time() - t0:.1f}s)')

    open_sea(mask)

    header = json.dumps({
        'lat0': LAT0, 'lat1': LAT1, 'lon0': LON0, 'lon1': LON1,
        'res': RES, 'rows': nrows, 'cols': ncols,
        'source': 'GSHHG 2.3.7 full resolution (LGPL)',
    }, separators=(',', ':')).encode()

    packed = np.packbits(mask, axis=None).tobytes()
    body = zlib.compress(packed, 9)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open('wb') as f:
        f.write(MAGIC)
        f.write(struct.pack('<I', len(header)))
        f.write(header)
        f.write(body)

    land = int(mask.sum())
    print(f'\n{OUT.relative_to(ROOT)}  {OUT.stat().st_size / 1e6:.1f} MB')
    print(f'{land / mask.size:.1%} land · {time.time() - t0:.1f}s')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
