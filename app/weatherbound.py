"""Bliver du blæst inde, når du er fremme?

Det klassiske danske sommerproblem: man sejler til Marstal i det pæneste vejr,
og så blæser det femogtyve knob i tre døgn, og man kommer ikke hjem. Prognosen
rækker ti døgn, og turen selv tager sjældent mere end fire — så de sidste dage
ligger der og siger noget, ingen kigger på.

Her kigger vi. Fra det øjeblik man er fremme, og til prognosen slipper op,
tælles det efter, om der overhovedet er et sejlbart døgn tilbage. Er der ikke,
skal det stå i planen, før man kaster los — ikke opdages i havnen.

Vi lover ingenting om, hvad der sker bagefter. Vi siger, hvad prognosen viser,
og hvor langt den rækker. Resten er skipperens.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta

from .sailing import GO, Limits, Plan, status_of

# Så mange timer i træk skal der være brugbart vejr, før dagen tæller som en,
# man kan komme afsted på. Under det er det et hul, ikke et vindue — man
# kaster ikke los på halvanden time.
MIN_WINDOW_H = 4


@dataclass
class Outlook:
    """Hvad prognosen siger om dagene, efter man er fremme."""
    place: str
    stuck_days: int          # hele sejldøgn i træk uden et brugbart vindue
    next_window: datetime | None   # første dag man kan komme afsted igen
    worst_wind_kn: float
    worst_wave_m: float
    runs_out: bool           # blæser det stadig, når prognosen holder op?
    checked_to: datetime | None

    @property
    def matters(self) -> bool:
        """Er det værd at sige noget om?

        Ét døgn er ikke en nyhed — man ligger over en dag, og det gør man
        alligevel. To i træk er en ændret ferie.
        """
        return self.stuck_days >= 2


def _hours(series: list[dict], start: datetime, end: datetime) -> list[dict]:
    return [row for row in series
            if row.get('time') and start <= row['time'] <= end]


def _day_ok(rows: list[dict], limits: Limits) -> bool:
    """Er der et brugbart vindue i dagens timer?"""
    run = 0
    for row in rows:
        # Søen vejes ikke efter retning her. Vi ved ikke, hvilken vej man vil
        # sejle hjem, og så er den rå bølgehøjde det ærligste mål.
        if status_of(row.get('wind_kn') or 0.0, row.get('wave_m') or 0.0,
                     limits.max_wind, limits.max_wave) == GO:
            run += 1
            if run >= MIN_WINDOW_H:
                return True
        else:
            run = 0
    return False


def look_ahead(plan: Plan, series: list[dict], limits: Limits,
               place: str) -> Outlook | None:
    """Tæl de sejldøgn efter ankomsten, hvor man ikke kan komme afsted.

    `series` er vejret på destinationen. Vi begynder dagen efter ankomsten:
    ankomstdagen er der ingen, der forventer at sejle videre på.
    """
    if not series or plan.incomplete:
        return None

    horizon = max((r['time'] for r in series if r.get('time')), default=None)
    if horizon is None:
        return None

    stuck, next_window = 0, None
    worst_wind, worst_wave = 0.0, 0.0
    day = (plan.arrival + timedelta(days=1)).date()

    while True:
        start = datetime.combine(day, datetime.min.time()).replace(
            hour=limits.day_start)
        end = datetime.combine(day, datetime.min.time()).replace(
            hour=limits.day_end)
        if end > horizon:
            break

        rows = _hours(series, start, end)
        if not rows:
            break
        if _day_ok(rows, limits):
            next_window = start
            break

        stuck += 1
        worst_wind = max(worst_wind, max(r.get('wind_kn') or 0.0 for r in rows))
        worst_wave = max(worst_wave, max(r.get('wave_m') or 0.0 for r in rows))
        day += timedelta(days=1)

    return Outlook(
        place=place,
        stuck_days=stuck,
        next_window=next_window,
        worst_wind_kn=round(worst_wind, 1),
        worst_wave_m=round(worst_wave, 1),
        # Slipper prognosen op, mens det stadig blæser, ved vi ikke hvornår
        # det holder — og dét er en anden besked end "på onsdag".
        runs_out=stuck > 0 and next_window is None,
        checked_to=horizon,
    )
