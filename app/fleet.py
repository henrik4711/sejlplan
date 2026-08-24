"""Bådregistret — søg din båd i stedet for at gætte dens fart.

Det svageste led i hele systemet var spørgsmålet "hvor hurtigt sejler din båd
for halvvind i ti knobs vind?". De færreste kender tallet, og gætter man
forkert, er hele planen forkert. Men næsten alle kender deres båds navn.

Så her ligger de både, man møder i danske og nordiske havne, med de mål,
fabrikanten opgiver: længde, vandlinje, deplacement, sejlareal og dybgang. Ud
af de mål kan farten anslås langt bedre, end nogen kan gætte den.

Anslås. Ikke måles. Et rigtigt polardiagram kommer fra en måling af netop den
båd med netop de sejl, og det har vi ikke. Derfor er tallet et skøn, det bliver
sagt at det er et skøn, og brugeren kan altid rette det.

Registret er håndholdt. Tallene er fabrikanternes nominelle mål, og en rettelse
er én linje i `data/sailboats.json`.
"""
from __future__ import annotations

import json
import math
import unicodedata
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

DATA = Path(__file__).resolve().parent / 'data' / 'sailboats.json'

# Omregning til de enheder, de klassiske forholdstal er defineret i.
M_TO_FT = 3.28084
KG_TO_LB = 2.20462
LB_PER_LONG_TON = 2240.0

# Referencen er en almindelig nutidig krydser. Konstanten er sat, så netop den
# rammer den fart, `boats.reference_speed()` giver — så registret og det tal,
# man selv kan taste, taler samme sprog.
BASE_FRACTION = 0.74
TYPICAL_SA_D = 17.0      # sejlareal/deplacement for en almindelig krydser
TYPICAL_D_L = 250.0      # deplacement/længde, samme båd


@dataclass(frozen=True)
class Sailboat:
    """En båd fra registret, med de mål der skal til for at anslå farten."""
    name: str
    loa_m: float
    lwl_m: float
    disp_kg: float
    sail_m2: float
    draft_m: float
    year: int

    # ── Klassiske forholdstal ───────────────────────────────────────
    @property
    def hull_speed_kn(self) -> float:
        """Skrogfarten. Den mur, et fortrængende skrog ikke kommer forbi."""
        return 1.34 * math.sqrt(max(1.0, self.lwl_m * M_TO_FT))

    @property
    def sail_area_disp(self) -> float:
        """Sejlareal mod deplacement — bådens kræfter i forhold til sin vægt.

        Under 16 er den tung at få i gang, over 20 er den letbenet.
        """
        vol = (self.disp_kg * KG_TO_LB) / 64.0        # kubikfod fortrængning
        return (self.sail_m2 * M_TO_FT ** 2) / (vol ** (2 / 3))

    @property
    def disp_length(self) -> float:
        """Deplacement mod vandlinje — hvor tungt skroget er for sin længde.

        Over 300 er en tung langturssejler, under 200 en let båd.
        """
        tons = (self.disp_kg * KG_TO_LB) / LB_PER_LONG_TON
        return tons / (0.01 * self.lwl_m * M_TO_FT) ** 3

    @property
    def reach_kn(self) -> float:
        """Anslået fart for halvvind i 10 knobs vind.

        Skrogfarten sætter loftet, og de to forholdstal siger, hvor stor en del
        af det loft båden når i en jævn brise: kræfterne trækker op, vægten
        trækker ned. Eksponenterne er små, fordi fart i den vind mest handler om
        vandlinjen — forholdstallene flytter den, de afgør den ikke.
        """
        power = self.sail_area_disp / TYPICAL_SA_D
        heft = self.disp_length / TYPICAL_D_L
        frac = BASE_FRACTION * power ** 0.45 / max(0.35, heft) ** 0.15
        return round(self.hull_speed_kn * min(0.95, max(0.40, frac)), 1)

    @property
    def character(self) -> str:
        """Bådens væsen i to ord — dét man ville sige om den på broen."""
        from .i18n import t
        sd, dl = self.sail_area_disp, self.disp_length
        if dl > 300:
            weight = 'tung'
        elif dl > 215:
            weight = 'solid'
        elif dl > 160:
            weight = 'moderat'
        else:
            weight = 'let'
        if sd > 21:
            rig = 'rigeligt sejl'
        elif sd > 17.5:
            rig = 'godt sejlført'
        elif sd > 15:
            rig = 'almindeligt sejlført'
        else:
            rig = 'beskedent sejlført'
        return f'{t(weight)}, {t(rig)}'

    @property
    def summary(self) -> str:
        from .i18n import t
        return (f'{_da(self.loa_m, 2)} m · {_da(self.disp_kg / 1000, 1)} t · '
                f'{_da(self.sail_m2, 0)} m² {t("sejl")} · '
                f'{_da(self.draft_m, 2)} m {t("dybgang")}')

    @property
    def reach_text(self) -> str:
        return f'{_da(self.reach_kn, 1)} kn'

    def as_spec(self) -> dict:
        """Bådens mål lagt over i den form, `boats.custom_boat` forstår."""
        return {
            'name': self.name,
            'kind': 'sail',
            'length_m': self.loa_m,
            'reach_kn': self.reach_kn,
            'draft_m': self.draft_m,
            'from_register': self.name,
        }


def _da(value: float, decimals: int = 1) -> str:
    """Dansk talformat. Et sejlareal med amerikansk punktum ser lånt ud."""
    return f'{value:.{decimals}f}'.replace('.', ',')


def _fold(text: str) -> str:
    """Slå ned til noget, man kan sammenligne: små bogstaver uden accenter."""
    text = text.lower().replace('ø', 'o').replace('æ', 'ae').replace('å', 'aa')
    text = unicodedata.normalize('NFKD', text)
    return ''.join(c for c in text if not unicodedata.combining(c))


@lru_cache(maxsize=1)
def all_boats() -> list[Sailboat]:
    """Hele registret, sorteret efter navn."""
    try:
        raw = json.loads(DATA.read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return []
    out = []
    for row in raw.get('baade') or []:
        try:
            out.append(Sailboat(
                name=str(row['n']), loa_m=float(row['loa']),
                lwl_m=float(row['lwl']), disp_kg=float(row['disp']),
                sail_m2=float(row['sa']), draft_m=float(row['draft']),
                year=int(row.get('y') or 0)))
        except (KeyError, TypeError, ValueError):
            continue
    out.sort(key=lambda b: _fold(b.name))
    return out


def search(query: str, limit: int = 12) -> list[Sailboat]:
    """Find bådene, der passer på det, der er tastet.

    Ordene må komme i hvilken som helst rækkefølge: "34 bavaria" skal finde
    Bavaria 34, for det er sådan folk husker deres båd. De, der begynder med
    det tastede, står øverst — dét er som regel den, man ledte efter.
    """
    q = _fold(query).strip()
    if len(q) < 2:
        return []
    words = q.split()

    hits = []
    for boat in all_boats():
        name = _fold(boat.name)
        if not all(w in name for w in words):
            continue
        # Rangering: hele det tastede forrest i navnet slår spredte ord.
        rank = 0 if name.startswith(q) else 1 if q in name else 2
        hits.append((rank, len(name), boat))

    hits.sort(key=lambda row: (row[0], row[1]))
    return [boat for _rank, _len, boat in hits[:limit]]


def by_name(name: str) -> Sailboat | None:
    folded = _fold(name)
    return next((b for b in all_boats() if _fold(b.name) == folded), None)
