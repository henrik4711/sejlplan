"""Kobl vores havne til havnelods.dk, så man kan læse mere om dem.

Sejlplan siger, hvornår du kan sejle, og hvilken havn du kan nå. Den siger
ingenting om, hvor mange pladser der er, hvad det koster, om der er vand på
broen, eller hvordan indsejlingen ser ud. Det står i en havneguide, og så skal
man kunne komme derhen med ét tryk.

Ingen af de danske guider har et opslag på navn, man kan regne med.
`danskehavnelods.dk` er en JavaScript-app, hvor adressen ikke rammer noget
serverside, og `havnelods.dk` har pæne sider — `/havne/marstal` — men slugs, man
ikke kan gætte: `aabenraa-lystbaadehavn-fh` ved siden af `assens`. Gætter man,
får man døde links, og et dødt link er værre end intet link.

Så vi finder dem alle selv. Guidens liste giver alle sider, hver side bærer sin
egen position i schema.org-data, og så kobles havnene på **position** — ikke på
navn. Det er den eneste nøgle, der holder: der findes to Ballen Havn, én på Fyn
og én på Samsø, og guiden har dem begge. Navnet kan ikke skelne dem. Det kan
positionen.

Siderne gemmes lokalt undervejs, så et nyt kørsel ikke henter det hele igen.

Vi tager kun navn, position og adresse — dét, der skal til for at pege rigtigt.
Formålet er at sende brugeren over til guiden.

Kør:  python tools/build_harbour_links.py
      python tools/build_harbour_links.py --frisk    (hent alt forfra)
"""
from __future__ import annotations

import json
import math
import re
import sys
import time
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app import harbours  # noqa: E402

LIST_URL = 'https://havnelods.dk/havne'
BASE = 'https://havnelods.dk/havne/'
CACHE = Path(__file__).resolve().parent / 'cache' / 'havnelods.json'
OUT = ROOT / 'app' / 'data' / 'harbour_links.json'

AGENT = 'Sejlplan/1.0 (havnekobling; kontakt via sejlplan)'

# Så tæt skal de ligge, før det er den samme havn. Under et kvart sømil er de
# oven i hinanden, og så er navnet ligegyldigt. Derudover — helt ud til en halv
# sømil, som er afstanden mellem to bassiner i den samme havn — skal navnene
# også dele et ord. Rønne Nørrekås og Rønne Sdr. Bådhavn er den samme havn;
# to havne på hver sin side af en bugt er ikke.
SURE_NM = 0.25
MAX_NM = 0.50

NM_PER_RADIAN = 3440.065


def words(text: str) -> set:
    """Navnets ord, foldet ned så æøå og store bogstaver ikke spænder ben."""
    text = text.lower().replace('ø', 'oe').replace('æ', 'ae').replace('å', 'aa')
    return {w for w in re.split(r'[^a-z0-9]+', text) if len(w) > 2}


def distance_nm(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = math.radians
    a = (math.sin(r(lat2 - lat1) / 2) ** 2
         + math.cos(r(lat1)) * math.cos(r(lat2)) * math.sin(r(lon2 - lon1) / 2) ** 2)
    return 2 * NM_PER_RADIAN * math.asin(math.sqrt(min(1.0, a)))


def slugs(client: httpx.Client) -> list[str]:
    """Alle guidens havnesider, taget fra dens egen liste."""
    r = client.get(LIST_URL, timeout=90)
    r.raise_for_status()
    seen, out = set(), []
    for chunk in r.text.split('href="/havne/')[1:]:
        slug = chunk.split('"')[0]
        if slug and slug not in seen:
            seen.add(slug)
            out.append(slug)
    return out


def read_page(text: str) -> dict | None:
    """Havnens navn og position, som siden selv opgiver dem.

    Siderne bærer schema.org-data af typen `Marina`. Det er guidens egne tal,
    ikke noget vi har regnet os frem til, og derfor det bedste vi kan få.
    """
    for blob in re.findall(
            r'<script type="application/ld\+json">(.*?)</script>', text, re.S):
        try:
            data = json.loads(blob)
        except ValueError:
            continue
        for node in (data if isinstance(data, list) else [data]):
            if not isinstance(node, dict) or node.get('@type') != 'Marina':
                continue
            geo = node.get('geo') or {}
            addr = node.get('address') or {}
            try:
                return {
                    'name': str(node.get('name') or ''),
                    'lat': float(geo['latitude']),
                    'lon': float(geo['longitude']),
                    'region': str(addr.get('addressRegion') or ''),
                    'country': str(addr.get('addressCountry') or ''),
                }
            except (KeyError, TypeError, ValueError):
                continue
    return None


def harvest(fresh: bool = False) -> dict[str, dict]:
    """Hent guidens havne. Det gemte genbruges, medmindre der bedes om nyt."""
    cache: dict[str, dict] = {}
    if CACHE.exists() and not fresh:
        try:
            cache = json.loads(CACHE.read_text(encoding='utf-8'))
        except ValueError:
            cache = {}

    with httpx.Client(headers={'User-Agent': AGENT}, follow_redirects=True,
                      timeout=40) as client:
        todo = [s for s in slugs(client) if s not in cache]
        print(f'{len(cache) + len(todo)} havne i guiden, '
              f'{len(todo)} skal hentes')

        for i, slug in enumerate(todo, 1):
            try:
                r = client.get(BASE + slug)
                row = read_page(r.text) if r.status_code == 200 else None
            except httpx.HTTPError:
                row = None
            if row:
                cache[slug] = row
            if i % 25 == 0 or i == len(todo):
                print(f'  {i}/{len(todo)} …')
                CACHE.parent.mkdir(parents=True, exist_ok=True)
                CACHE.write_text(json.dumps(cache, ensure_ascii=False),
                                 encoding='utf-8')
            # Vi henter fem hundrede sider fra en gratis guide. Så tager vi den
            # med ro.
            time.sleep(0.35)

    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(cache, ensure_ascii=False), encoding='utf-8')
    return cache


def match(guide: dict[str, dict], ours: list) -> dict[str, str]:
    """Kobl på position. Nærmeste havn inden for MAX_NM vinder."""
    rows = [(s, g) for s, g in guide.items()
            if isinstance(g, dict) and 'lat' in g]
    links: dict[str, str] = {}

    for h in ours:
        mine_words = words(h.name)
        best, best_d = None, MAX_NM
        for slug, g in rows:
            d = distance_nm(h.lat, h.lon, g['lat'], g['lon'])
            if d >= best_d:
                continue
            if d > SURE_NM and not (mine_words & words(g.get('name') or '')):
                continue
            best, best_d = slug, d
        if best:
            links[f'{h.lat:.4f},{h.lon:.4f}'] = best
    return links


def main() -> None:
    fresh = '--frisk' in sys.argv
    guide = harvest(fresh)
    with_geo = sum(1 for g in guide.values() if 'lat' in g)
    ours = harbours.all_harbours()
    links = match(guide, ours)

    OUT.write_text(json.dumps({
        '_om': ('Kobling fra havnens position til havnelods.dk. Noeglen er '
                'lat,lon med fire decimaler — ikke navnet, for der findes to '
                'Ballen Havn. Bygget af tools/build_harbour_links.py. '
                'Vaerdien saettes efter ' + BASE),
        'base': BASE,
        'links': dict(sorted(links.items())),
    }, ensure_ascii=False, indent=1), encoding='utf-8')

    print(f'\n{with_geo} af guidens {len(guide)} sider har position')
    print(f'{len(links)} af vores {len(ours)} havne fik et link '
          f'({len(set(links.values()))} af guidens sider ramt)')
    print(f'skrevet til {OUT.relative_to(ROOT)} '
          f'({OUT.stat().st_size / 1024:.1f} kB)')


if __name__ == '__main__':
    main()
