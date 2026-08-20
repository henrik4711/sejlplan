"""Hvor er der vand?

Et enkelt gitter over skandinaviske farvande, én bit pr. celle på ca. 200 × 125
meter, bygget af GSHHG's kystlinjer i fuld opløsning. Filen ligger i
`app/data/landmask.bin` og laves med `tools/build_landmask.py`.

Grunden til at det er en bitmap og ikke polygoner: ruteberegningen skal kunne
spørge hundredtusindvis af gange i træk om der er vand i et punkt, og det skal
koste ét opslag i et array. Polygoner ville koste et gennemløb hver gang.

Uden for gitteret svarer vi "vand". Så virker appen stadig i farvande vi ikke
har data for — den lægger bare ruten lige, som den altid har gjort.
"""
from __future__ import annotations

import json
import math
import struct
import zlib
from dataclasses import dataclass
from pathlib import Path

import numpy as np

DATA = Path(__file__).resolve().parent / 'data' / 'landmask.bin'
MAGIC = b'SJPMASK1'

NM_PER_DEGREE = 60.0


@dataclass(frozen=True)
class Grid:
    lat0: float
    lon0: float
    res: float
    rows: int
    cols: int
    land: np.ndarray          # (rows, cols) bool – True = land

    def row(self, lat: float) -> int:
        return int((lat - self.lat0) / self.res)

    def col(self, lon: float) -> int:
        return int((lon - self.lon0) / self.res)

    def lat_of(self, row: int) -> float:
        return self.lat0 + (row + 0.5) * self.res

    def lon_of(self, col: int) -> float:
        return self.lon0 + (col + 0.5) * self.res

    def inside(self, lat: float, lon: float) -> bool:
        r, c = self.row(lat), self.col(lon)
        return 0 <= r < self.rows and 0 <= c < self.cols


_grid: Grid | None = None
_loaded = False


def grid() -> Grid | None:
    """Læs gitteret første gang det bruges. Mangler filen, kører appen uden."""
    global _grid, _loaded
    if _loaded:
        return _grid
    _loaded = True
    try:
        raw = DATA.read_bytes()
        if raw[:8] != MAGIC:
            return None
        size = struct.unpack('<I', raw[8:12])[0]
        head = json.loads(raw[12:12 + size])
        rows, cols = int(head['rows']), int(head['cols'])
        bits = np.unpackbits(np.frombuffer(zlib.decompress(raw[12 + size:]), dtype=np.uint8))
        _grid = Grid(
            lat0=float(head['lat0']), lon0=float(head['lon0']), res=float(head['res']),
            rows=rows, cols=cols,
            land=bits[:rows * cols].reshape(rows, cols).astype(bool),
        )
    except (OSError, ValueError, KeyError, zlib.error):
        _grid = None
    return _grid


def available() -> bool:
    return grid() is not None


# ── Opslag ───────────────────────────────────────────────────────────────────
def is_water(lat: float, lon: float) -> bool:
    """Er der vand i punktet? Uden for gitteret: ja, vi ved det ikke bedre."""
    g = grid()
    if g is None or not g.inside(lat, lon):
        return True
    return not bool(g.land[g.row(lat), g.col(lon)])


def _samples(lat1: float, lon1: float, lat2: float, lon2: float,
             g: Grid) -> tuple[np.ndarray, np.ndarray]:
    """Punkter langs en linje, tættere end gitterets celler er store."""
    span = max(abs(lat2 - lat1), abs(lon2 - lon1))
    n = int(min(20000, max(2, span / g.res * 2)))
    t = np.linspace(0.0, 1.0, n)
    return lat1 + (lat2 - lat1) * t, lon1 + (lon2 - lon1) * t


def _all_water(lats: np.ndarray, lons: np.ndarray, g: Grid) -> bool:
    r = ((lats - g.lat0) / g.res).astype(np.int64)
    c = ((lons - g.lon0) / g.res).astype(np.int64)
    inside = (r >= 0) & (r < g.rows) & (c >= 0) & (c < g.cols)
    if not inside.any():
        return True
    return not bool(g.land[r[inside], c[inside]].any())


def clear(lat1: float, lon1: float, lat2: float, lon2: float,
          clearance_nm: float = 0.0) -> bool:
    """Kan man sejle lige fra det ene punkt til det andet uden at ramme land?

    `clearance_nm` lægger en bræmme ud til hver side, så ruten ikke skraber
    en pynt. Bræmmen tjekkes som to parallelle linjer — nok til formålet og
    langt billigere end at afsøge et helt bånd.
    """
    g = grid()
    if g is None:
        return True

    lats, lons = _samples(lat1, lon1, lat2, lon2, g)
    if not _all_water(lats, lons, g):
        return False
    if clearance_nm <= 0:
        return True

    mid_lat = math.radians((lat1 + lat2) / 2)
    scale = max(0.2, math.cos(mid_lat))
    dy, dx = lat2 - lat1, (lon2 - lon1) * scale
    length = math.hypot(dy, dx)
    if length < 1e-9:
        return True

    off = clearance_nm / NM_PER_DEGREE
    n_lat, n_lon = -dx / length * off, dy / length * off / scale
    for sign in (1, -1):
        if not _all_water(lats + sign * n_lat, lons + sign * n_lon, g):
            return False
    return True


def nearest_water(lat: float, lon: float, max_nm: float = 6.0) -> tuple[float, float]:
    """Nærmeste vandcelle. Ligger punktet allerede i vand, returneres det uændret.

    Bruges når en havn eller et klik lander på land — havnebassiner er for små
    til at figurere i kystlinjedataene, så en havnemole tæller som land.
    """
    g = grid()
    if g is None or is_water(lat, lon):
        return lat, lon

    r0, c0 = g.row(lat), g.col(lon)
    limit = int(max_nm / NM_PER_DEGREE / g.res)
    best: tuple[float, float] | None = None
    best_d = float('inf')

    for radius in range(1, limit + 1):
        r_lo, r_hi = max(0, r0 - radius), min(g.rows, r0 + radius + 1)
        c_lo, c_hi = max(0, c0 - radius), min(g.cols, c0 + radius + 1)
        window = g.land[r_lo:r_hi, c_lo:c_hi]
        free = np.argwhere(~window)
        if not len(free):
            continue
        rr = free[:, 0] + r_lo
        cc = free[:, 1] + c_lo
        d = (rr - r0) ** 2 + ((cc - c0) * 0.55) ** 2
        i = int(np.argmin(d))
        if d[i] < best_d:
            best_d = float(d[i])
            best = (g.lat_of(int(rr[i])), g.lon_of(int(cc[i])))
        if best is not None:
            break
    return best or (lat, lon)
