"""Tilstand pr. bruger.

NiceGUI kører sidefunktionen én gang pr. klient, så en `Session` hører til
præcis én browserfane — ingen deling mellem brugere. Det holdbare (rute, båd,
grænser) spejles i `app.storage.user`, så det overlever en genindlæsning.

Ruten findes i to udgaver: brugerens punkter, og den streg der faktisk sejles
mellem dem. Den sidste regnes ud af `searoute` og kan tage et øjeblik, så den
lever i et felt for sig og bliver lagt på plads, når den er klar.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta

from nicegui import app

from .boats import BOATS, DEFAULT_BOAT, Boat
from .sailing import Limits, Plan, Route, Waypoint

STORAGE_KEY = 'sejlplan'
PLANNING_DAYS = 3          # standard: i dag og tre dage frem
MAX_FORECAST_DAYS = 7      # så langt rækker prognosen


def default_limits() -> Limits:
    today = date.today()
    boat = BOATS[DEFAULT_BOAT]
    return Limits(
        max_wind=boat.max_wind_kn,
        max_wave=boat.max_wave_m,
        date_from=today.isoformat(),
        date_to=(today + timedelta(days=PLANNING_DAYS)).isoformat(),
    )


def signature(waypoints: list[Waypoint]) -> tuple:
    """Nøgle der ændrer sig, præcis når ruten skal regnes om."""
    return tuple((round(w.lat, 5), round(w.lon, 5)) for w in waypoints)


@dataclass
class Session:
    """Alt hvad én bruger har gang i lige nu."""

    waypoints: list[Waypoint] = field(default_factory=list)
    boat_id: str = DEFAULT_BOAT
    limits: Limits = field(default_factory=default_limits)

    # Ruten gennem vandet – regnet i baggrunden, tom indtil den er klar.
    tracks: list[list[tuple[float, float]]] = field(default_factory=list)
    exact: list[bool] = field(default_factory=list)
    tracks_for: tuple = ()
    routing: bool = False

    # Beregnet – ryddes så snart ruten eller grænserne ændrer sig.
    weather: list = field(default_factory=list)
    windows: list[Plan] = field(default_factory=list)
    selected: int = 0
    has_waves: bool = True
    ai_text: str = ''

    step: int = 1  # 1 = rute, 2 = afgang, 3 = sejlplan

    # ── Afledt ──────────────────────────────────────────────────────
    @property
    def boat(self) -> Boat:
        return BOATS.get(self.boat_id) or BOATS[DEFAULT_BOAT]

    @property
    def route(self) -> Route:
        """Ruten som den ser ud lige nu — med havvejen, hvis den er regnet."""
        fresh = self.tracks_for == signature(self.waypoints)
        return Route(list(self.waypoints),
                     [list(t) for t in self.tracks] if fresh else [],
                     list(self.exact) if fresh else [])

    @property
    def route_ready(self) -> bool:
        return bool(self.waypoints) and self.tracks_for == signature(self.waypoints)

    @property
    def plan(self) -> Plan | None:
        if not self.windows:
            return None
        return self.windows[min(self.selected, len(self.windows) - 1)]

    @property
    def can_analyse(self) -> bool:
        return len(self.waypoints) >= 2

    @property
    def total_nm(self) -> float:
        return self.route.total_nm

    # ── Ruten gennem vandet ─────────────────────────────────────────
    def set_tracks(self, key: tuple, legs) -> bool:
        """Læg en færdigregnet rute på plads. Falsk hvis den er forældet."""
        if key != signature(self.waypoints):
            return False
        self.tracks = [list(leg.points) for leg in legs]
        self.exact = [leg.exact for leg in legs]
        self.tracks_for = key
        self.routing = False
        return True

    # ── Ændringer ───────────────────────────────────────────────────
    def invalidate(self) -> None:
        """Kaldes når ruten eller grænserne ændres: gamle resultater gælder ikke."""
        self.weather = []
        self.windows.clear()
        self.selected = 0
        self.ai_text = ''
        if self.step > 1:
            self.step = 1

    def add(self, wp: Waypoint) -> None:
        self.waypoints.append(wp)
        self.invalidate()
        self.persist()

    def remove(self, index: int) -> None:
        if 0 <= index < len(self.waypoints):
            self.waypoints.pop(index)
            self.invalidate()
            self.persist()

    def move(self, index: int, delta: int) -> None:
        """Flyt et waypoint op eller ned i rækkefølgen."""
        target = index + delta
        if 0 <= index < len(self.waypoints) and 0 <= target < len(self.waypoints):
            wps = self.waypoints
            wps[index], wps[target] = wps[target], wps[index]
            self.invalidate()
            self.persist()

    def insert(self, index: int, wp: Waypoint) -> None:
        self.waypoints.insert(max(0, min(index, len(self.waypoints))), wp)
        self.invalidate()
        self.persist()

    def reverse(self) -> None:
        self.waypoints.reverse()
        self.invalidate()
        self.persist()

    def clear(self) -> None:
        self.waypoints.clear()
        self.tracks, self.exact, self.tracks_for = [], [], ()
        self.invalidate()
        self.persist()

    def set_boat(self, boat_id: str) -> None:
        """Bådskiftet trækker komfortgrænserne med sig — de hører til båden."""
        if boat_id not in BOATS:
            return
        self.boat_id = boat_id
        self.limits.max_wind = BOATS[boat_id].max_wind_kn
        self.limits.max_wave = BOATS[boat_id].max_wave_m
        self.invalidate()
        self.persist()

    # ── Lagring ─────────────────────────────────────────────────────
    def persist(self) -> None:
        lim = self.limits
        try:
            app.storage.user[STORAGE_KEY] = {
                'boat_id': self.boat_id,
                'waypoints': [w.as_dict() for w in self.waypoints],
                'limits': {
                    'max_wind': lim.max_wind,
                    'max_wave': lim.max_wave,
                    'date_from': lim.date_from,
                    'date_to': lim.date_to,
                    'day_start': lim.day_start,
                    'day_end': lim.day_end,
                    'night_ok': lim.night_ok,
                    'use_motor': lim.use_motor,
                },
            }
        except (RuntimeError, KeyError):
            # Ingen sessionslager (fx under test) – så kører vi bare uden.
            pass

    @staticmethod
    def restore() -> 'Session':
        """Læs sidste session tilbage. Datoer i fortiden rykkes frem til i dag."""
        s = Session()
        try:
            saved = app.storage.user.get(STORAGE_KEY) or {}
        except (RuntimeError, KeyError):
            return s

        s.boat_id = saved.get('boat_id') or DEFAULT_BOAT
        if s.boat_id not in BOATS:
            s.boat_id = DEFAULT_BOAT

        try:
            s.waypoints = [Waypoint.from_dict(d) for d in saved.get('waypoints') or []]
        except (KeyError, TypeError, ValueError):
            s.waypoints = []

        lim = saved.get('limits') or {}
        d = s.limits
        d.max_wind = float(lim.get('max_wind', d.max_wind))
        d.max_wave = float(lim.get('max_wave', d.max_wave))
        # `early_hour`/`late_hour` er de gamle navne, fra dengang tallene kun
        # afgrænsede afgangen. Nu afgrænser de hele sejldøgnet.
        d.day_start = int(lim.get('day_start', lim.get('early_hour', d.day_start)))
        d.day_end = int(lim.get('day_end', lim.get('late_hour', d.day_end)))
        if d.day_end <= d.day_start:
            d.day_start, d.day_end = 7, 20
        d.night_ok = bool(lim.get('night_ok', not lim.get('avoid_night', True)))
        d.use_motor = bool(lim.get('use_motor', d.use_motor))
        s.normalise_dates()
        return s

    def normalise_dates(self) -> None:
        """Hold datovinduet inden for det prognosen faktisk dækker."""
        today = date.today()
        horizon = today + timedelta(days=MAX_FORECAST_DAYS - 1)

        try:
            start = date.fromisoformat(self.limits.date_from)
        except (TypeError, ValueError):
            start = today
        try:
            end = date.fromisoformat(self.limits.date_to)
        except (TypeError, ValueError):
            end = today + timedelta(days=PLANNING_DAYS)

        start = min(max(start, today), horizon)
        end = min(max(end, start), horizon)
        self.limits.date_from = start.isoformat()
        self.limits.date_to = end.isoformat()
