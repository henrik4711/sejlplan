"""Ruter der holder sig i vandet.

En sejlrute mellem to havne er sjældent en ret linje. Modulet her lægger vejen
udenom land i tre trin, fordi ét ikke rækker:

1. **Grovsøgning.** A* på et gitter, der er groft nok til at en tur over
   Kattegat kan regnes på et øjeblik. Ingen celle er spærret med mindre den er
   land tvært igennem — til gengæld er land dyrt. Så finder søgningen det
   rigtige farvand uden at et smalt løb som Snævringen lukker sig, blot fordi
   gitteret blev groft.
2. **Udglatning.** Punkter fjernes, så længe der kan trækkes en fri linje
   udenom dem. Trappemønsteret fra gitteret bliver til de få lange stræk, en
   skipper faktisk ville sejle — og de stykker, der ikke kunne glattes ud, er
   præcis dem, hvor grovsøgningen skar et hjørne.
3. **Reparation.** De stykker efterprøves mod kystlinjens egen opløsning og
   lægges om med en finsøgning i et lille vindue. Vinduet kan være lille, netop
   fordi udglatningen har indsnævret problemet til ét knæk ad gangen. Det er
   her Snævringen og Svendborgsund bliver fundet.

Viser et stykke sig at være helt ulasteligt — grovsøgningen troede der var et
løb, men det er lukket — spærres det i grovgitteret, og der søges forfra. Så
finder ruten det næstbedste farvand i stedet for at sy en omvej sammen om et
sted, den aldrig skulle have været.

Enderne er altid brugerens egne punkter. En havn ligger bag moler, som
kystlinjen regner for land, så det første og sidste stykke går ind til kajen —
præcis som man selv sejler det.
"""
from __future__ import annotations

import heapq
import math
from collections.abc import Iterable
from dataclasses import dataclass

import numpy as np

from . import landmask
from .landmask import NM_PER_DEGREE

Point = tuple[float, float]

# Afstand til land, ruten forsøger at holde. Nok til at man ikke ligger og
# skraber en pynt, lidt nok til at den stadig kan gå gennem et snævert løb.
CLEARANCE_NM = 0.25

# ── Grovsøgning ──────────────────────────────────────────────────────────────
COARSE_CELLS = 320          # kantlængde på grovgitteret
COARSE_MIN_STEP = 0.004
COARSE_MAX_STEP = 0.02

# Land spærrer først, når cellen ikke har vand i sig overhovedet. I stedet gør
# landandelen cellen dyr, og prisen stiger i tredje potens: en halvt tør celle
# er til at betale, en næsten tør er det ikke. Det holder de smalle løb åbne
# uden at ruten begynder at skyde genvej over et næs.
SOLID = 0.995
LAND_COST = 40.0

# ── Finsøgning ───────────────────────────────────────────────────────────────
FINE_STEP = 0.002            # kystlinjegitterets egen opløsning
FINE_MAX_CELLS = 300_000     # loft over hvor stort et reparationsvindue bliver
FINE_MARGINS = (0.05, 0.15, 0.45)   # grader luft omkring stykket der lægges om

# En omlægning må gerne bugte sig gennem et løb, men ikke sejle hele vejen
# rundt om en ø. Bliver den længere end det her, var det ikke et løb.
PATCH_LIMIT_NM = 6.0
PATCH_LIMIT_FACTOR = 8.0
RETRIES = 4         # hvor mange gange et lukket løb må spærres og ruten lægges om

# Hvor mange punkter frem udglatningen leder efter en genvej, efter den sidste
# der virkede. Uden loftet ville hvert punkt blive prøvet mod alle de andre.
LOOKAHEAD = 14

STRAIGHT = ((-1, 0), (1, 0), (0, -1), (0, 1))
DIAGONAL = ((-1, -1), (-1, 1), (1, -1), (1, 1))


class NoRoute(RuntimeError):
    """Der blev ikke fundet en vej gennem vandet."""


@dataclass(frozen=True)
class Leg:
    """Ét ben af ruten: den streg man faktisk sejler."""

    points: list[Point]
    exact: bool = True      # False = vi måtte give op og lægge den lige

    @property
    def detour(self) -> bool:
        """Går benet udenom noget, eller er det bare en ret linje?"""
        return len(self.points) > 2


# ── Søgevinduet ──────────────────────────────────────────────────────────────
class Window:
    """Et udsnit af kortet, klar til A*.

    `blocked` siger hvor man ikke må sejle, `penalty` hvor man helst ikke vil.
    Bræmmen langs kysten er ikke spærret — bare dyrere, så ruten af sig selv
    søger ud på det åbne vand, når der er plads til det.
    """

    def __init__(self, lat0: float, lon0: float, step: float,
                 share: np.ndarray) -> None:
        self.lat0, self.lon0, self.step = lat0, lon0, step
        self.rows, self.cols = share.shape
        self.blocked = share > SOLID
        self.penalty = shore_penalty(self.blocked) + (share ** 3) * np.float32(LAND_COST)

        mid = math.radians(lat0 + self.rows * step / 2)
        self.dy_nm = step * NM_PER_DEGREE
        self.dx_nm = step * NM_PER_DEGREE * max(0.2, math.cos(mid))

    def cell(self, lat: float, lon: float) -> tuple[int, int]:
        r = min(self.rows - 1, max(0, int((lat - self.lat0) / self.step)))
        c = min(self.cols - 1, max(0, int((lon - self.lon0) / self.step)))
        return r, c

    def point(self, r: int, c: int) -> Point:
        return (self.lat0 + (r + 0.5) * self.step,
                self.lon0 + (c + 0.5) * self.step)


def shore_penalty(blocked: np.ndarray) -> np.ndarray:
    """Ekstra pris for at ligge tæt på land: én ring dyr, næste ring lidt dyr."""
    near = np.zeros(blocked.shape, dtype=np.float32)
    ring = blocked
    for weight in (0.9, 0.35):
        grown = ring.copy()
        grown[1:, :] |= ring[:-1, :]
        grown[:-1, :] |= ring[1:, :]
        grown[:, 1:] |= ring[:, :-1]
        grown[:, :-1] |= ring[:, 1:]
        near += (grown & ~ring) * np.float32(weight)
        ring = grown
    return near


def window(lat_lo: float, lat_hi: float, lon_lo: float, lon_hi: float,
           step: float) -> Window:
    """Klip kystlinjegitteret ned til søgeopløsning inden for et udsnit."""
    g = landmask.grid()
    if g is None:
        raise NoRoute('intet kystlinjegitter')

    lat_lo, lon_lo = max(g.lat0, lat_lo), max(g.lon0, lon_lo)
    lat_hi = min(g.lat0 + g.rows * g.res, lat_hi)
    lon_hi = min(g.lon0 + g.cols * g.res, lon_hi)

    # Hver søgecelle dækker et helt antal celler i kystlinjegitteret, så
    # landandelen kan tælles med ét reshape i stedet for et opslag pr. celle.
    per = max(1, int(round(step / g.res)))
    r0, c0 = int((lat_lo - g.lat0) / g.res), int((lon_lo - g.lon0) / g.res)
    rows = min(int((lat_hi - lat_lo) / g.res), g.rows - r0) // per
    cols = min(int((lon_hi - lon_lo) / g.res), g.cols - c0) // per
    if rows < 2 or cols < 2:
        raise NoRoute('udsnittet er for lille')

    block = g.land[r0:r0 + rows * per, c0:c0 + cols * per]
    share = block.reshape(rows, per, cols, per).mean(axis=(1, 3), dtype=np.float32)
    return Window(g.lat0 + r0 * g.res, g.lon0 + c0 * g.res, per * g.res, share)


def free_cell(w: Window, lat: float, lon: float) -> tuple[int, int]:
    """Nærmeste celle man kan sejle i. Havne ligger tit i en spærret celle."""
    r, c = w.cell(lat, lon)
    if not w.blocked[r, c]:
        return r, c
    for radius in (4, 16, 64, 256, 1024):
        r_lo, r_hi = max(0, r - radius), min(w.rows, r + radius + 1)
        c_lo, c_hi = max(0, c - radius), min(w.cols, c + radius + 1)
        free = np.argwhere(~w.blocked[r_lo:r_hi, c_lo:c_hi])
        if len(free):
            d = (free[:, 0] + r_lo - r) ** 2 + (free[:, 1] + c_lo - c) ** 2
            i = int(np.argmin(d))
            return int(free[i, 0]) + r_lo, int(free[i, 1]) + c_lo
    raise NoRoute('intet farbart vand i nærheden')


# ── A* ───────────────────────────────────────────────────────────────────────
def astar(w: Window, start: tuple[int, int], goal: tuple[int, int]) -> list[Point]:
    """Billigste vej gennem vandet. Diagonaler kun hvor der er plads til dem."""
    rows, cols = w.rows, w.cols
    blocked, penalty = w.blocked, w.penalty
    dy, dx = w.dy_nm, w.dx_nm
    diag = math.hypot(dy, dx)
    gr, gc = goal
    s_idx, g_idx = start[0] * cols + start[1], goal[0] * cols + goal[1]

    best = np.full(rows * cols, np.inf, dtype=np.float32)
    came = np.full(rows * cols, -1, dtype=np.int32)
    done = np.zeros(rows * cols, dtype=bool)
    best[s_idx] = 0.0

    heap = [(math.hypot((start[0] - gr) * dy, (start[1] - gc) * dx), s_idx)]
    while heap:
        _, idx = heapq.heappop(heap)
        if idx == g_idx:
            break
        if done[idx]:
            continue
        done[idx] = True
        r, c = divmod(idx, cols)
        here = best[idx]

        for dr, dc in STRAIGHT:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < rows and 0 <= nc < cols) or blocked[nr, nc] or done[nr * cols + nc]:
                continue
            n = nr * cols + nc
            cost = here + (dy if dr else dx) * (1.0 + penalty[nr, nc])
            if cost < best[n]:
                best[n] = cost
                came[n] = idx
                heapq.heappush(heap, (cost + math.hypot((nr - gr) * dy, (nc - gc) * dx), n))

        for dr, dc in DIAGONAL:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < rows and 0 <= nc < cols) or blocked[nr, nc]:
                continue
            # Skær ikke hjørner: begge nabofelter skal være frie, ellers ville
            # ruten smutte diagonalt gennem en landtange.
            if blocked[nr, c] or blocked[r, nc]:
                continue
            n = nr * cols + nc
            if done[n]:
                continue
            cost = here + diag * (1.0 + penalty[nr, nc])
            if cost < best[n]:
                best[n] = cost
                came[n] = idx
                heapq.heappush(heap, (cost + math.hypot((nr - gr) * dy, (nc - gc) * dx), n))

    if g_idx != s_idx and came[g_idx] < 0:
        raise NoRoute('ingen vej fundet')

    path, idx = [], g_idx
    while idx >= 0:
        r, c = divmod(idx, cols)
        path.append(w.point(r, c))
        if idx == s_idx:
            break
        idx = int(came[idx])
    path.reverse()
    return path


# ── De tre trin ──────────────────────────────────────────────────────────────
def coarse_window(a: Point, b: Point, margin: float) -> Window:
    """Læg gitteret ud til grovsøgningen med `margin` graders luft omkring."""
    span = max(abs(a[0] - b[0]), abs(a[1] - b[1]))
    step = min(COARSE_MAX_STEP, max(COARSE_MIN_STEP, span / COARSE_CELLS))
    lat_lo, lat_hi = min(a[0], b[0]) - margin, max(a[0], b[0]) + margin
    lon_lo, lon_hi = min(a[1], b[1]) - margin, max(a[1], b[1]) + margin
    wide = max(lat_hi - lat_lo, lon_hi - lon_lo)
    return window(lat_lo, lat_hi, lon_lo, lon_hi, max(step, wide / COARSE_CELLS))


def start_search(a: Point, b: Point) -> tuple[Window, list[Point], tuple[int, int], tuple[int, int]]:
    """Første grovrute. Findes der ingen vej, får søgningen mere plads at gå ud i."""
    margin = max(0.15, max(abs(a[0] - b[0]), abs(a[1] - b[1])) * 0.35)
    for _ in range(3):
        try:
            w = coarse_window(a, b, margin)
            first, last = free_cell(w, *a), free_cell(w, *b)
            return w, astar(w, first, last), first, last
        except NoRoute:
            margin *= 2.2
    raise NoRoute('intet farvand mellem punkterne')


def repair(path: list[Point]) -> tuple[list[Point], list[tuple[Point, Point]]]:
    """Læg de stykker om, der ikke holder mod kystlinjens egen opløsning.

    Efter udglatningen er et dårligt stykke altid kort — det er ét knæk, hvor
    grovsøgningen skar et hjørne — så vinduet kan være lille og søgningen
    hurtig. Returnerer ruten og de stykker, der ikke lod sig lægge om.
    """
    out: list[Point] = [path[0]]
    closed: list[tuple[Point, Point]] = []

    for target in path[1:]:
        here = out[-1]
        if landmask.clear(here[0], here[1], target[0], target[1]):
            out.append(target)
            continue

        budget = max(PATCH_LIMIT_NM, nm(here, target) * PATCH_LIMIT_FACTOR)
        patch = None
        for margin in FINE_MARGINS:
            try:
                found = local_route(here, target, margin)
            except NoRoute:
                continue
            if length(found) <= budget:
                patch = found
                break
            # Omvejen er så lang, at løbet må være lukket. Det er ikke et
            # hjørne der skal skæres pænere — det er et forkert farvand.
            break

        if patch is None:
            closed.append((here, target))
            out.append(target)
        else:
            out.extend(patch[1:])
    return out, closed


def nm(a: Point, b: Point) -> float:
    """Afstand i sømil. Fladt regnet – strækningerne her er korte."""
    return math.hypot(a[0] - b[0], (a[1] - b[1]) * math.cos(math.radians(a[0]))) * NM_PER_DEGREE


def length(path: list[Point]) -> float:
    return sum(nm(a, b) for a, b in zip(path, path[1:]))


def local_route(a: Point, b: Point, margin: float) -> list[Point]:
    """Finsøgning i et lille vindue, hvor land er land og intet andet."""
    lat_lo, lat_hi = min(a[0], b[0]) - margin, max(a[0], b[0]) + margin
    lon_lo, lon_hi = min(a[1], b[1]) - margin * 1.7, max(a[1], b[1]) + margin * 1.7

    step = FINE_STEP
    cells = ((lat_hi - lat_lo) / step) * ((lon_hi - lon_lo) / step)
    if cells > FINE_MAX_CELLS:
        step *= math.sqrt(cells / FINE_MAX_CELLS)

    w = window(lat_lo, lat_hi, lon_lo, lon_hi, step)
    inner = astar(w, free_cell(w, *a), free_cell(w, *b))
    # Enderne skal være de punkter, der blev bedt om — ellers ville stykket
    # blive hæftet på ruten et par hundrede meter ved siden af, og netop dét
    # spring kunne gå over land.
    return [a, *inner[1:-1], b]


def smooth(path: list[Point], clearance: float) -> list[Point]:
    """Fjern punkter, så længe der kan trækkes en fri linje henover dem."""
    if len(path) < 3:
        return path

    out, i, last = [path[0]], 0, len(path) - 1
    while i < last:
        best = i + 1
        j = i + 1
        while j <= last and j - best <= LOOKAHEAD:
            a, b = path[i], path[j]
            if landmask.clear(a[0], a[1], b[0], b[1], clearance):
                best = j
            j += 1
        out.append(path[best])
        i = best
    return out


def plan(a: Point, b: Point) -> Leg:
    """Læg ét ben fra a til b."""
    if not landmask.available():
        return Leg([a, b])

    start, end = landmask.nearest_water(*a), landmask.nearest_water(*b)
    if landmask.clear(start[0], start[1], end[0], end[1], CLEARANCE_NM):
        return Leg([a, b])

    try:
        w, guide, first, last = start_search(start, end)
    except NoRoute:
        return Leg([a, b], exact=False)

    path: list[Point] = [start, end]
    closed: list[tuple[Point, Point]] = []

    for attempt in range(RETRIES):
        if attempt:
            try:
                guide = astar(w, first, last)
            except NoRoute:
                break
        # Grovcellernes midtpunkter kan ligge på land — cellen spærres jo først,
        # når den er tør tvært igennem. Træk dem ud i vandet, før der måles på dem.
        guide = [landmask.nearest_water(*p) for p in guide]
        guide[0], guide[-1] = start, end
        path, closed = repair(smooth(guide, 0.0))
        if not closed:
            break
        if not block(w, closed, first, last):
            break

    path = smooth(smooth(path, CLEARANCE_NM), 0.0)
    return Leg([a, *path[1:-1], b], exact=not closed)


def block(w: Window, closed: list[tuple[Point, Point]],
          first: tuple[int, int], last: tuple[int, int]) -> bool:
    """Spær de grovceller, hvor løbet viste sig at være lukket."""
    marked = False
    for a, b in closed:
        r1, c1 = w.cell(*a)
        r2, c2 = w.cell(*b)
        steps = max(abs(r2 - r1), abs(c2 - c1), 1)
        for i in range(steps + 1):
            cell = (r1 + (r2 - r1) * i // steps, c1 + (c2 - c1) * i // steps)
            if cell in (first, last) or w.blocked[cell]:
                continue
            w.blocked[cell] = True
            marked = True
    return marked


def plan_route(points: Iterable[Point]) -> list[Leg]:
    """Læg hele ruten, ét ben ad gangen."""
    pts = list(points)
    return [plan(a, b) for a, b in zip(pts, pts[1:])]
