"""App på hjemmeskærmen, og en plan der bliver, når dækningen går.

To ting, som hænger sammen, men ikke er det samme.

**Appen** er et manifest og et sæt ikoner. Så kan Sejlplan lægges på
hjemmeskærmen og åbne i sit eget vindue uden browserlinje. Det koster ingenting
og ændrer alt ved, hvordan den føles.

**Uden dækning** er sværere, og det skal siges rent: Sejlplan tegner fladen på
serveren og sender den ned over en websocket. Uden forbindelse er der ingen
flade — og en service worker kan ikke tegne den, for den findes kun på serveren.
Man kan altså ikke *lægge* en rute uden dækning.

Men det er heller ikke dét, man har brug for på vandet. Dér skal man kunne
*læse* den plan, man lagde i havn i morges. Så hver gang en plan bliver regnet,
lægger vi den ned som ét selvstændigt dokument i browserens cache. Går siden
ikke igennem, serverer service workeren dokumentet i stedet — og så står hele
sejlplanen der, midt i Kattegat.

Kortfliserne, man har set på, bliver liggende i deres egen cache med et loft, så
kortet også kan vise sig selv i det farvand, man lige har kigget på.
"""
from __future__ import annotations

import json
from pathlib import Path

from fastapi import Response
from nicegui import app, ui

STATIC = Path(__file__).resolve().parent / 'static'

# Versionen står i cachenavnene. Ændrer man service workeren, skal de gamle
# caches ryddes — ellers ligger en forældet app og holder ved.
VERSION = 'v1'

MANIFEST = {
    'id': '/',
    'name': 'Sejlplan',
    'short_name': 'Sejlplan',
    'description': 'Find den bedste afgang, og tag sejlplanen med til søs.',
    # Appen paa hjemmeskaermen skal aabne i planlaeggeren, ikke paa
    # forsiden. Den, der har lagt Sejlplan paa skaermen, er ikke i gang med
    # at laese om, hvad den kan. `scope` bliver paa roden, saa forsiden og
    # de andre sprog stadig hoerer med til appen.
    'start_url': '/planlaeg',
    'scope': '/',
    'display': 'standalone',
    'orientation': 'any',
    'background_color': '#0D1B2A',
    'theme_color': '#0D1B2A',
    'lang': 'da',
    'dir': 'ltr',
    'categories': ['navigation', 'travel', 'weather'],
    'icons': [
        {'src': '/static/icon-192.png', 'sizes': '192x192', 'type': 'image/png'},
        {'src': '/static/icon-512.png', 'sizes': '512x512', 'type': 'image/png'},
        {'src': '/static/icon-maskable-512.png', 'sizes': '512x512',
         'type': 'image/png', 'purpose': 'maskable'},
    ],
}

# ── Service worker ────────────────────────────────────────────────────────────
# Den bor på roden, fordi en service worker kun må styre det, der ligger under
# dens egen sti. Skal den svare for hele appen, skal den ligge øverst.
SERVICE_WORKER = """
const V = '%(version)s';
const SHELL = 'sejlplan-shell-' + V;   // appens egne filer
const TILES = 'sejlplan-tiles-' + V;   // kortfliser man har set paa
const PLAN  = 'sejlplan-plan';         // den gemte sejlplan (overlever versioner)
const PLAN_URL = '/offline-plan';
const TILE_LIMIT = 600;                // ~15 MB. Nok til et farvand, ikke til et hav.

self.addEventListener('install', (e) => {
  self.skipWaiting();
});

self.addEventListener('activate', (e) => {
  e.waitUntil((async () => {
    // Ryd gamle udgaver, men lad planen ligge — den er brugerens, ikke vores.
    const keys = await caches.keys();
    await Promise.all(keys.map((k) =>
      (k.startsWith('sejlplan-shell-') || k.startsWith('sejlplan-tiles-'))
        && !k.endsWith(V) ? caches.delete(k) : null));
    await self.clients.claim();
  })());
});

// Siden sender planen herned, saa snart den er regnet.
self.addEventListener('message', (e) => {
  const d = e.data || {};
  if (d.type !== 'gem-plan' || !d.html) return;
  e.waitUntil(caches.open(PLAN).then((c) => c.put(PLAN_URL, new Response(
    d.html, {headers: {'Content-Type': 'text/html; charset=utf-8'}}))));
});

function erFlise(url) {
  return /\\.(png|jpg|jpeg|webp)($|\\?)/i.test(url.pathname)
      && /(tile|arcgis|basemaps|openstreetmap|cartocdn|openseamap)/i.test(url.host + url.pathname);
}

async function beskaerFliser() {
  const c = await caches.open(TILES);
  const alle = await c.keys();
  // De aeldste ryger foerst. Cache API holder raekkefoelgen fra de blev lagt.
  for (let i = 0; i < alle.length - TILE_LIMIT; i++) await c.delete(alle[i]);
}

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);

  // 1. Selve siden. Naettet foerst — planen er kun en redningsline.
  if (req.mode === 'navigate') {
    e.respondWith((async () => {
      try {
        return await fetch(req);
      } catch (err) {
        const gemt = await caches.match(PLAN_URL);
        if (gemt) return gemt;
        return new Response(INGEN_PLAN, {
          status: 200, headers: {'Content-Type': 'text/html; charset=utf-8'}});
      }
    })());
    return;
  }

  // 2. Kortfliser. Cachen foerst — de aendrer sig ikke, og de er tunge.
  if (erFlise(url)) {
    e.respondWith((async () => {
      const c = await caches.open(TILES);
      const hit = await c.match(req);
      if (hit) return hit;
      const svar = await fetch(req);
      if (svar.ok || svar.type === 'opaque') {
        c.put(req, svar.clone()).then(beskaerFliser).catch(() => {});
      }
      return svar;
    })());
    return;
  }

  // 3. Appens egne filer. Vis det gemte med det samme, og hent en frisk
  //    udgave i baggrunden — saa starter appen hurtigt paa en daarlig linje.
  if (url.origin === location.origin
      && /^\\/(_nicegui|static)\\//.test(url.pathname)) {
    e.respondWith((async () => {
      const c = await caches.open(SHELL);
      const hit = await c.match(req);
      const frisk = fetch(req).then((svar) => {
        if (svar.ok) c.put(req, svar.clone());
        return svar;
      }).catch(() => hit);
      return hit || frisk;
    })());
  }
});

const INGEN_PLAN = `<!doctype html><html lang="da"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="light dark"><title>Sejlplan uden dækning</title>
<style>
:root{--bg:#F4F1EC;--ink:#12212F;--ink2:rgba(18,33,47,.66);--gold:#A8752A}
@media(prefers-color-scheme:dark){:root{--bg:#0D1B2A;--ink:#F0EDE8;
--ink2:rgba(240,237,232,.66);--gold:#E8B96A}}
body{margin:0;min-height:100vh;display:flex;align-items:center;justify-content:center;
background:var(--bg);color:var(--ink);text-align:center;padding:32px;
font:16px/1.6 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif}
h1{font-size:20px;margin:18px 0 8px}p{color:var(--ink2);max-width:34ch;margin:0 auto}
svg{width:56px;height:56px}
</style></head><body><div>
<svg viewBox="0 0 24 24" fill="var(--gold)"><path d="M12 2 L20 15 H13 V2 Z"/>
<path d="M11 5 L11 15 H4 Z" opacity=".72"/>
<path d="M3 17 h18 l-3 4 H6 Z"/></svg>
<h1>Ingen dækning — og ingen gemt plan</h1>
<p>Sejlplan lægger selv den nyeste sejlplan i telefonen, så du kan læse den uden
forbindelse. Der er bare ikke lavet en endnu. Åbn appen med dækning, find en
afgang, og så ligger planen her næste gang.</p>
</div></body></html>`;
"""

# ── Registrering i siden ──────────────────────────────────────────────────────
REGISTER = """
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js', {scope: '/'}).catch(() => {});
  });
}
// Chrome spoerger ikke selv paa skrivebordet. Vi gemmer tilbuddet, saa appen
// kan tilbyde installation dér, hvor det giver mening.
window.sejlplanInstall = null;
window.addEventListener('beforeinstallprompt', (e) => {
  e.preventDefault();
  window.sejlplanInstall = e;
  document.body.classList.add('kan-installeres');
});
window.addEventListener('appinstalled', () => {
  window.sejlplanInstall = null;
  document.body.classList.remove('kan-installeres');
});
"""

# Læg planen ned i service workerens cache. Den kan komme, før workeren er
# klar — derfor ventes der på `ready` i stedet for at antage noget.
SAVE_PLAN = """
(async (html) => {
  try {
    const reg = await navigator.serviceWorker.ready;
    (reg.active || navigator.serviceWorker.controller)
      .postMessage({type: 'gem-plan', html});
  } catch (e) {
    // Ingen service worker (fx en gammel browser). Så er der ingen offline-
    // plan, og det er den eneste ting, der går tabt.
  }
})(%(html)s);
"""


def register_routes() -> None:
    """Manifest, service worker og ikoner. Kaldes én gang ved opstart."""

    @app.get('/manifest.webmanifest')
    def _manifest() -> Response:
        return Response(json.dumps(MANIFEST, ensure_ascii=False),
                        media_type='application/manifest+json')

    @app.get('/sw.js')
    def _sw() -> Response:
        return Response(
            SERVICE_WORKER % {'version': VERSION},
            media_type='application/javascript',
            # Browseren skal opdage en ny service worker med det samme.
            headers={'Cache-Control': 'no-cache',
                     'Service-Worker-Allowed': '/'})

    if STATIC.is_dir():
        app.add_static_files('/static', STATIC)


def head() -> None:
    """De mærker i sidens hoved, der gør den til en app."""
    ui.add_head_html(
        '<link rel="manifest" href="/manifest.webmanifest">'
        '<meta name="theme-color" content="#0D1B2A">'
        '<meta name="mobile-web-app-capable" content="yes">'
        # iOS har sine egne mærker og læser ikke manifestet.
        '<meta name="apple-mobile-web-app-capable" content="yes">'
        '<meta name="apple-mobile-web-app-title" content="Sejlplan">'
        '<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">'
        '<link rel="apple-touch-icon" href="/static/apple-touch-icon.png">'
        '<link rel="icon" type="image/png" sizes="32x32" href="/static/favicon-32.png">'
    )
    ui.add_body_html(f'<script>{REGISTER}</script>')


def save_plan_js(html: str) -> str:
    """JavaScript, der lægger et plandokument i telefonen."""
    return SAVE_PLAN % {'html': json.dumps(html)}
