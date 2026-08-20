"""Havneregisteret.

Godt 3.000 lystbådehavne i danske og skandinaviske farvande, hentet fra
OpenStreetMap og lagt ned i én pakket fil med `tools/build_harbours.py`. Appen
slår op i den lokalt: ingen netværkskald, intet at vente på, og den virker
også når man planlægger fra kajen med dårligt signal.

Registeret bruges tre steder:

* **søgningen** i trin 1, når man leder efter en havn ved navn
* **kortet**, der viser havnene omkring dét, man kigger på
* **overnatningerne**, når en tur ikke kan nås inden for ét sejldøgn og
  planlæggeren skal finde et sted at ligge undervejs
"""
from __future__ import annotations

import gzip
import json
import math
import unicodedata
from dataclasses import dataclass
from pathlib import Path

import numpy as np

DATA = Path(__file__).resolve().parent / 'data' / 'harbours.json.gz'

NM_PER_DEGREE = 60.0

# Hvor langt en havn må ligge fra ruten, før den ikke længere er et rimeligt
# sted at søge ind. Seks sømil er godt en time for en sejlbåd — nok til at
# Køge og Rødvig kommer med, når man ligger i Drogden og skal have en havn.
MAX_DETOUR_NM = 6.0


HOME = 'Danmark'


@dataclass(frozen=True)
class Harbour:
    name: str
    water: str
    country: str
    lat: float
    lon: float
    berths: int = 0

    @property
    def icon(self) -> str:
        return 'anchor'

    @property
    def home(self) -> bool:
        return self.country == HOME

    @property
    def detail(self) -> str:
        """Stedet, som en sejler ville sige det: farvandet, og landet hvis det er ude."""
        if self.home:
            return self.water or 'Lystbådehavn'
        if self.water and self.country:
            return f'{self.water} · {self.country}'
        return self.country or self.water or 'Lystbådehavn'


_all: list[Harbour] | None = None
_coords: np.ndarray | None = None


def all_harbours() -> list[Harbour]:
    """Læs registeret første gang det bruges."""
    global _all, _coords
    if _all is not None:
        return _all
    try:
        with gzip.open(DATA, 'rt', encoding='utf-8') as f:
            rows = json.load(f)
        _all = [Harbour(r[0], r[1], r[2], r[3], r[4], r[5]) for r in rows]
    except (OSError, ValueError, IndexError):
        _all = []
    _coords = (np.array([[h.lat, h.lon] for h in _all], dtype=np.float64)
               if _all else np.zeros((0, 2)))
    return _all


def coords() -> np.ndarray:
    all_harbours()
    return _coords if _coords is not None else np.zeros((0, 2))


# ── Søgning ──────────────────────────────────────────────────────────────────
def fold(s: str) -> str:
    """Sammenlign uden hensyn til store bogstaver og æøå/accenter."""
    s = s.lower().replace('æ', 'ae').replace('ø', 'oe').replace('å', 'aa')
    return ''.join(c for c in unicodedata.normalize('NFD', s) if not unicodedata.combining(c))


_index: list[tuple[str, str, Harbour]] | None = None


def _search_index() -> list[tuple[str, str, Harbour]]:
    global _index
    if _index is None:
        _index = [(fold(h.name), fold(h.detail), h) for h in all_harbours()]
    return _index


def _rank(h: Harbour) -> tuple:
    """Danske havne først, så de store. Det er dem, folk oftest mener."""
    return (not h.home, -h.berths, len(h.name))


def search(query: str, limit: int = 8) -> list[Harbour]:
    """Havne der matcher. Dem der begynder med søgeordet kommer først."""
    q = fold(query.strip())
    if not q:
        return []
    starts = [h for name, _, h in _search_index() if name.startswith(q)]
    inside = [h for name, detail, h in _search_index()
              if not name.startswith(q) and (q in name or q in detail)]
    starts.sort(key=_rank)
    inside.sort(key=_rank)
    return (starts + inside)[:limit]


def in_bounds(south: float, west: float, north: float, east: float,
              limit: int = 400) -> list[Harbour]:
    """Havnene inden for et kortudsnit. Er der for mange, vises de største."""
    pts = coords()
    if not len(pts):
        return []
    hit = ((pts[:, 0] >= south) & (pts[:, 0] <= north)
           & (pts[:, 1] >= west) & (pts[:, 1] <= east))
    found = [h for h, ok in zip(all_harbours(), hit) if ok]
    if len(found) > limit:
        found.sort(key=lambda h: (-h.berths, h.name))
        found = found[:limit]
    return found


def nearest(lat: float, lon: float, count: int = 5) -> list[Harbour]:
    pts = coords()
    if not len(pts):
        return []
    scale = math.cos(math.radians(lat))
    d = (pts[:, 0] - lat) ** 2 + ((pts[:, 1] - lon) * scale) ** 2
    order = np.argsort(d)[:count]
    return [all_harbours()[int(i)] for i in order]


# ── Havne langs en rute ──────────────────────────────────────────────────────
def along_route(route, max_detour_nm: float = MAX_DETOUR_NM) -> list[tuple]:
    """Havne tæt nok på ruten til at kunne bruges som overnatning.

    Returnerer (havn, sømil inde i ruten, afstikker i sømil), sorteret efter
    hvor langt inde i ruten de ligger. Afstanden måles vinkelret ned på hvert
    lige stykke af ruten — det er dét, en afstikker faktisk koster.
    """
    pts = coords()
    steps = getattr(route, 'steps', None)
    if not len(pts) or not steps:
        return []

    scale = math.cos(math.radians(float(np.mean(pts[:, 0]))))
    hl = pts[:, 0]
    hx = pts[:, 1] * scale

    best_d = np.full(len(pts), np.inf)
    best_along = np.zeros(len(pts))

    for s in steps:
        ay, ax = s.lat, s.lon * scale
        by, bx = s.to_lat, s.to_lon * scale
        dy, dx = by - ay, bx - ax
        span = dy * dy + dx * dx
        if span <= 0:
            continue
        t = np.clip(((hl - ay) * dy + (hx - ax) * dx) / span, 0.0, 1.0)
        d = np.hypot(hl - (ay + t * dy), hx - (ax + t * dx)) * NM_PER_DEGREE
        better = d < best_d
        best_d = np.where(better, d, best_d)
        best_along = np.where(better, s.start_nm + t * s.distance_nm, best_along)

    hits = np.flatnonzero(best_d <= max_detour_nm)
    out = [(all_harbours()[int(i)], float(best_along[i]), float(best_d[i])) for i in hits]
    out.sort(key=lambda row: row[1])
    return out


def reachable(route, candidates: list[tuple]) -> list[tuple]:
    """Frasortér de havne, man ikke kan sejle lige ind til fra ruten.

    En havn kan ligge to sømil fra ruten og alligevel ligge på den anden side
    af en ø. Vi tjekker linjen fra ruten ind mod havnen, så et forslag om at
    overnatte aldrig kræver, at man sejler over land.
    """
    from . import landmask
    if not landmask.available():
        return candidates

    out = []
    for h, along, detour in candidates:
        lat, lon, _course, _leg = route.at(along)
        entry = landmask.nearest_water(h.lat, h.lon)
        if landmask.clear(lat, lon, entry[0], entry[1]):
            out.append((h, along, detour))
    return out


def stopovers(route, max_detour_nm: float = MAX_DETOUR_NM) -> list[tuple]:
    """Havnene man reelt kan overnatte i undervejs på ruten."""
    return reachable(route, along_route(route, max_detour_nm))
