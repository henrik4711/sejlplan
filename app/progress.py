"""Hvor er jeg i forhold til planen?

Planen er lagt i havnen. Undervejs er spørgsmålet et andet: er jeg foran eller
bagud, og hvornår er jeg så fremme i virkeligheden?

Det kræver kun ét stykke information, som telefonen selv har: hvor båden er.
Ikke hvem der sejler den, ikke hvor den var i går, og ikke hvor andre er.
Positionen bliver på telefonen og hos den ene beregning her — den gemmes ikke,
og den sendes ikke videre til nogen.

Regnestykket er simpelt og robust: find det punkt på ruten, man er tættest på,
læs hvor langt inde det ligger, og slå op i planens eget spor, hvor langt man
skulle have været på det klokkeslæt. Forskellen er forspringet.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import datetime, timedelta

NM_PER_DEGREE = 60.0

# Længere væk end det er man ikke på ruten længere, og så siger et forspring
# ingenting. Tre sømil er rundhåndet nok til at runde en pynt vidt, men ikke
# nok til at være i en anden bugt.
OFF_ROUTE_NM = 3.0


@dataclass
class Progress:
    """Bådens plads i planen lige nu."""
    along_nm: float          # hvor langt inde i ruten
    remaining_nm: float
    off_route_nm: float      # hvor langt fra stregen
    planned_nm: float        # hvor langt man skulle have været
    ahead_nm: float          # foran (+) eller bagud (−) i sømil
    ahead_min: float         # det samme i minutter
    eta: datetime | None     # ny ankomst med den fart, der faktisk holdes
    made_good_kn: float      # fart over grunden siden afgang
    arrived: bool
    started: bool            # er afgangstidspunktet overhovedet passeret?

    @property
    def on_route(self) -> bool:
        return self.off_route_nm <= OFF_ROUTE_NM

    @property
    def verdict(self) -> str:
        """Kort dom. Et kvarter er ikke noget at sige om."""
        if not self.started:
            return 'ikke begyndt'
        if self.arrived:
            return 'fremme'
        if abs(self.ahead_min) < 15:
            return 'som planlagt'
        return 'foran' if self.ahead_min > 0 else 'bagud'


def _project(route, lat: float, lon: float) -> tuple[float, float]:
    """Nærmeste punkt på ruten: hvor langt inde, og hvor langt væk.

    Samme projektion som havnene bruger — vinkelret ned på hvert lige stykke.
    """
    steps = getattr(route, 'steps', None)
    if not steps:
        return 0.0, float('inf')

    scale = math.cos(math.radians(lat))
    px, py = lon * scale, lat
    best_along, best_d = 0.0, float('inf')

    for s in steps:
        ay, ax = s.lat, s.lon * scale
        by, bx = s.to_lat, s.to_lon * scale
        dy, dx = by - ay, bx - ax
        span = dy * dy + dx * dx
        if span <= 0:
            continue
        t = max(0.0, min(1.0, ((py - ay) * dy + (px - ax) * dx) / span))
        d = math.hypot(py - (ay + t * dy), px - (ax + t * dx)) * NM_PER_DEGREE
        if d < best_d:
            best_d = d
            best_along = s.start_nm + t * s.distance_nm
    return best_along, best_d


def _planned_at(plan, when: datetime) -> float:
    """Hvor langt inde i ruten planen siger, man skulle være nu.

    Planens spor er sejltimerne. Ligger man i havn mellem to døgn, står tallet
    stille — og det er rigtigt: man skulle heller ikke være kommet længere.
    """
    rows = [(s.along_nm, s.time) for s in plan.segments]
    rows.append((plan.total_nm, plan.arrival))
    if not rows:
        return 0.0
    if when <= rows[0][1]:
        return 0.0
    for (a1, t1), (a2, t2) in zip(rows, rows[1:]):
        if t1 <= when <= t2:
            span = (t2 - t1).total_seconds()
            if span <= 0:
                return a2
            return a1 + (a2 - a1) * ((when - t1).total_seconds() / span)
    return plan.total_nm


def where(route, plan, lat: float, lon: float,
          now: datetime | None = None) -> Progress | None:
    """Sammenlign, hvor båden er, med hvor planen sagde den ville være."""
    if plan is None or not plan.segments or route.total_nm <= 0:
        return None
    now = now or datetime.now()

    along, off = _project(route, lat, lon)
    planned = _planned_at(plan, now)
    remaining = max(0.0, route.total_nm - along)

    # Er afgangen ikke passeret endnu, er der ingen fart at regne og intet
    # forspring at have. Første udgave dividerede med et tidsrum, der ikke var
    # gået, og skrev "291,6 knob i snit" på en sejlbåd.
    sailed_h = (now - plan.depart).total_seconds() / 3600
    started = sailed_h > 0.05
    if not started:
        return Progress(
            along_nm=round(along, 1), remaining_nm=round(remaining, 1),
            off_route_nm=round(off, 2), planned_nm=0.0, ahead_nm=0.0,
            ahead_min=0, eta=None, made_good_kn=0.0,
            arrived=False, started=False)

    made_good = along / sailed_h
    # Minutter foran regnes med den fart, planen selv holder — ikke bådens.
    # Ellers ville et øjebliks vindstille se ud som en times forsinkelse.
    pace = plan.avg_speed_kn or made_good or 1.0
    ahead_min = (along - planned) / pace * 60
    arrived = remaining < 0.3

    eta = None
    if not arrived and 0.5 < made_good < 40:
        # Den fart, man faktisk har holdt, er det ærligste bud på resten.
        eta = now + timedelta(hours=remaining / made_good)

    return Progress(
        along_nm=round(along, 1), remaining_nm=round(remaining, 1),
        off_route_nm=round(off, 2), planned_nm=round(planned, 1),
        ahead_nm=round(along - planned, 1), ahead_min=round(ahead_min),
        eta=eta, made_good_kn=round(made_good, 1), arrived=arrived,
        started=True)
