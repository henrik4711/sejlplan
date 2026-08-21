"""Kortet: ruten, havnene og interaktionen med dem.

NiceGUI's Leaflet-komponent videresender kun kortets egne begivenheder, ikke
lagenes. Markørernes ikoner og deres træk-håndtering sættes derfor med et enkelt
stykke JavaScript, som melder tilbage via `emitEvent`.

Havnelaget er bygget på samme måde, men af en anden grund: der er over tre
tusind havne. At lave dem som Python-lag ville sende tre tusind beskeder over
websocket'en hver gang kortet flyttede sig. I stedet får browseren hele listen
én gang og tegner selv dem, der er i billedet.
"""
from __future__ import annotations

import json
from collections.abc import Callable

from nicegui import ui

from .. import harbours
from ..sailing import GO, STATUS_COLOR, Plan, Route

# ── Grundkort ────────────────────────────────────────────────────────────────
# "Søkort" viser dybdeforhold og er det, man planlægger en sejlads efter.
# "Landkort" er det almindelige gadekort, når man skal finde havnen i land.
OCEAN_TILES = ('https://services.arcgisonline.com/ArcGIS/rest/services/Ocean/'
               'World_Ocean_Base/MapServer/tile/{z}/{y}/{x}')
OCEAN_LABELS = ('https://services.arcgisonline.com/ArcGIS/rest/services/Ocean/'
                'World_Ocean_Reference/MapServer/tile/{z}/{y}/{x}')
OCEAN_ATTRIBUTION = 'Esri, GEBCO, NOAA, National Geographic'
# Esri har kun fliser til zoom 10 i vores farvande. Uden `maxNativeZoom` beder
# Leaflet om fliser, der ikke findes, og så står der "Map data not yet
# available" hen over hele kortet — præcis dér, hvor man zoomer ind for at
# finde havneindløbet. Med den sat strækker Leaflet flisen fra niveau 10 i
# stedet. Lidt uskarpt, men et kort.
OCEAN_NATIVE_ZOOM = 10
# Over det her niveau er den strakte flise ikke længere et kort at navigere
# efter, og det skarpe landkort nedenunder tager over. Sat lig med Esris egen
# grænse: så snart der ikke er rigtige fliser mere, er der ingen grund til at
# vise en forstørrelse af dem.
CHART_FADE_ZOOM = 10

STREET_LIGHT = 'https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}.png'
STREET_DARK = 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png'
STREET_ATTRIBUTION = ('&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> '
                      '&copy; <a href="https://carto.com/attributions">CARTO</a>')

# OpenSeaMap lægger bøjer, fyr, sejlløb og havnesymboler oven på grundkortet.
SEAMARK_TILES = 'https://tiles.openseamap.org/seamark/{z}/{x}/{y}.png'
SEAMARK_ATTRIBUTION = '&copy; <a href="https://www.openseamap.org/">OpenSeaMap</a>'

CHART, STREET = 'chart', 'street'

HOME = (56.2, 11.4)   # Kattegat – midt i det danske sejlområde
HOME_ZOOM = 7

# Under dette zoomniveau ville havnene ligge oven i hinanden som konfetti.
HARBOUR_ZOOM = 8
# Og herfra er der plads til at skrive, hvad de hedder.
HARBOUR_LABEL_ZOOM = 10
HARBOUR_MAX = 300

# Kortet bygges på serveren, før Vue har monteret komponenten i browseren.
# Kører vores JavaScript for tidligt, findes `c.map` ikke endnu — og så fik en
# gemt rute grå standardnåle i stedet for de nummererede. Derfor venter alle
# stykker på, at kortet dukker op, i stedet for at antage at det er der.
_WHEN_READY = """
(function run(tries) {
  const c = getElement(%(map_id)d);
  if (!c || !c.map) {
    if (tries < 60) setTimeout(() => run(tries + 1), 100);
    return;
  }
  %(body)s
})(0);
"""

# Kortets egen lys/mørk-tilstand. Den følger grundkortet, ikke appens tema:
# havkortet er lyst, også når resten af fladen er mørk.
_BASE_MODE_BODY = """
  c.map.getContainer().classList.toggle('map-dark', %(dark)s);
"""

# Zoom til ruten. Leaflet regner sit udsnit ud fra beholderens størrelse, og
# ved sideindlæsning er den endnu ikke lagt færdigt — så et `fitBounds` sendt
# derfra landede på hele Skandinavien i stedet for på de to havne, man lige
# havde valgt. Derfor måler vi op igen først og venter på næste tegning.
_FIT_BODY = """
  const pts = %(points)s;
  c.map.invalidateSize();
  requestAnimationFrame(() => {
    if (pts.length === 1) c.map.setView(pts[0], %(zoom)d);
    else c.map.fitBounds(pts, {padding: [70, 70], maxZoom: %(zoom)d});
  });
"""

# Kobling mellem panel og kort. Peger man på et sted i listen, skal kortet vise
# hvilket. Det sker helt i browseren: rækkerne bærer deres position i et
# data-attribut, og én lytter oversætter det til en ring på kortet. Havde vi
# sendt hver mus-bevægelse til serveren og svaret tilbage, ville ringen komme
# et halvt sekund efter fingeren — og så er den værre end ingenting.
_LINK_BODY = """
  if (c.__sejlplanLink) return;
  c.__sejlplanLink = true;

  const ring = L.circleMarker([0, 0], {
    radius: 15, weight: 3, color: '#C8933B', opacity: 0,
    fillColor: '#C8933B', fillOpacity: 0, interactive: false,
    className: 'spot-ring',
  }).addTo(c.map);

  const show = (lat, lon) => {
    ring.setLatLng([lat, lon]);
    ring.setStyle({opacity: .95, fillOpacity: .18});
  };
  const hide = () => ring.setStyle({opacity: 0, fillOpacity: 0});

  const spot = (e) => e.target.closest && e.target.closest('[data-spot]');
  document.addEventListener('mouseover', (e) => {
    const el = spot(e);
    if (!el) return;
    const [lat, lon] = el.dataset.spot.split(',').map(Number);
    show(lat, lon);
  });
  document.addEventListener('mouseout', (e) => { if (spot(e)) hide(); });
  // Ruller listen væk under fingeren, skal ringen ikke blive hængende.
  document.addEventListener('scroll', hide, true);
"""

_RESIZE_BODY = """
  if (c.__sejlplanResize) return;
  c.__sejlplanResize = true;
  const fix = () => c.map.invalidateSize();
  new ResizeObserver(fix).observe(c.$el);
  window.addEventListener('resize', fix);
  requestAnimationFrame(fix);
"""

# Markørerne skabes af Vue, og der går et øjeblik fra serveren har sendt dem,
# til de er i kortet. Vi bliver ved med at prøve, indtil hver eneste af dem har
# fået sit nummer på — ellers ville en rute kunne ende med grå standardnåle.
_MARKERS_BODY = """
  const specs = %(specs)s;
  const wanted = Object.keys(specs).length;
  (function paint(tries) {
    let done = 0;
    c.map.eachLayer((l) => {
      const s = specs[l.id];
      if (!s || !l.setIcon) return;
      done += 1;
      l.setIcon(L.divIcon({
        html: '<div class="wp-marker wp-marker--' + s.kind + '">' + s.label + '</div>',
        className: '', iconSize: [30, 30], iconAnchor: [15, 15],
      }));
      if (l.bindTooltip) l.bindTooltip(s.name, {direction: 'top', offset: [0, -16]});
      if (!l.__sejlplanWired && l.dragging) {
        l.__sejlplanWired = true;
        l.on('dragend', (ev) => {
          const p = ev.target.getLatLng();
          emitEvent('wp_moved', {id: l.id, lat: p.lat, lng: p.lng});
        });
      }
    });
    if (done < wanted && tries < 40) setTimeout(() => paint(tries + 1), 90);
  })(0);
"""

# Havnene tegnes i browseren ud fra én liste, der kun sendes én gang. Ved hvert
# kortryk vises de, der er i billedet — resten koster ingenting at have med.
#
# Fra zoomniveau 10 skrives navnene på. Uden dem er en havn bare en blå prik, og
# så kan man ikke se om den ene er Mosede og den anden Greve. Navnene sættes med
# en simpel kollisionstest: den største havn får pladsen, og en etiket, der ville
# lægge sig oven i en anden, springes over. Det er sådan et rigtigt kort gør det,
# og det er dét, der gør forskellen på et kort og en samling prikker.
_HARBOURS_BODY = """
  if (!c.__harbourData) {
    c.__harbourData = %(data)s;
    c.__harbourLayer = L.layerGroup();

    c.__harbourDraw = () => {
      const layer = c.__harbourLayer;
      layer.clearLayers();
      if (!c.__harboursOn) return;
      const zoom = c.map.getZoom();
      if (zoom < %(min_zoom)d) return;

      const bounds = c.map.getBounds();
      const named = zoom >= %(label_zoom)d;
      const big = zoom >= 11;

      const seen = [];
      for (const h of c.__harbourData) {
        if (bounds.contains([h[0], h[1]])) seen.push(h);
        if (seen.length > 1500) break;
      }
      // Størst først: har to etiketter ikke plads, er det den lille, der viger.
      seen.sort((a, b) => (b[4] || 0) - (a[4] || 0));

      // Rutens egne markører har fortrinsret. Uden det kunne en havneetiket
      // lægge sig hen over destinationen, så det så ud som om ruten gik til
      // et helt andet sted.
      const taken = [];
      c.map.eachLayer((l) => {
        if (!l.setIcon || !l.getLatLng) return;
        const p = c.map.latLngToContainerPoint(l.getLatLng());
        taken.push([p.x - 20, p.y - 20, p.x + 20, p.y + 20]);
      });

      let shown = 0;
      for (const h of seen) {
        if (++shown > %(max)d) break;

        let label = '';
        if (named) {
          const p = c.map.latLngToContainerPoint([h[0], h[1]]);
          const w = 10 + h[2].length * 5.8;
          const box = [p.x - 6, p.y - 9, p.x + 11 + w, p.y + 9];
          const clash = taken.some((t) => !(box[2] < t[0] || box[0] > t[2]
                                         || box[3] < t[1] || box[1] > t[3]));
          if (!clash) {
            taken.push(box);
            label = '<b>' + h[2] + '</b>';
          }
        }

        const marker = L.marker([h[0], h[1]], {
          icon: L.divIcon({
            className: 'hb-icon',
            html: '<span class="hb' + (big ? ' hb--big' : '') + '"><i></i>'
                  + label + '</span>',
            iconSize: [0, 0], iconAnchor: [0, 0],
          }),
          keyboard: false, riseOnHover: true, zIndexOffset: -500,
        });
        marker.bindTooltip(h[2] + (h[3] ? ' · ' + h[3] : ''),
                           {direction: 'top', offset: [0, -10], className: 'hb-tip'});
        marker.on('click', (ev) => {
          L.DomEvent.stopPropagation(ev);
          emitEvent('harbour_pick', {lat: h[0], lng: h[1], name: h[2]});
        });
        layer.addLayer(marker);
      }
    };
    c.map.on('moveend zoomend', c.__harbourDraw);
  }
  c.__harboursOn = %(on)s;
  if (c.__harboursOn) c.__harbourLayer.addTo(c.map); else c.map.removeLayer(c.__harbourLayer);
  c.__harbourDraw();
"""


class RouteMap:
    """Indkapsler Leaflet-kortet og holder det i sync med ruten."""

    def __init__(self, on_click: Callable[[float, float], None],
                 on_drag: Callable[[int, float, float], None],
                 on_harbour: Callable[[float, float, str], None],
                 dark: bool = True, style: str = CHART) -> None:
        self._on_drag = on_drag
        self._on_harbour = on_harbour
        self._markers: list = []
        self._lines: list = []
        self._marker_index: dict[str, int] = {}
        self._dark = dark
        self._style = style
        self._base: list = []
        self._seamarks = None
        # Havnene er tændt fra start. Det er dem, man planlægger efter, og de
        # koster kun én liste over websocket'en — resten sker i browseren.
        self._harbours_on = True
        self._harbours_sent = False
        # Kortets JavaScript sendes også fra baggrundsopgaver, hvor NiceGUI's
        # underforståede klient ikke længere er den rigtige. Vi holder fast i
        # vores egen, så beskederne altid lander i den browser de hører til.
        self._client = ui.context.client

        self.map = ui.leaflet(center=HOME, zoom=HOME_ZOOM, options={
            'zoomControl': True,
            'attributionControl': True,
            'worldCopyJump': True,
        }).classes('absolute inset-0')  # forankret, så højden aldrig kan blive nul
        self.map.clear_layers()
        self._add_base()

        self.map.on('map-click', lambda e: on_click(e.args['latlng']['lat'],
                                                    e.args['latlng']['lng']))
        ui.on('wp_moved', self._handle_drag)
        ui.on('harbour_pick', self._handle_harbour)

        # Leaflet måler sin beholder én gang ved opstart. På det tidspunkt er
        # flex-layoutet ikke lagt færdigt, så kortet husker en for lille højde
        # og tegner kun en stribe fliser. Observatøren nedenfor får det til at
        # måle op igen — helt i browseren, så intet kan fyre efter at siden
        # er lukket.
        self._run(_RESIZE_BODY)
        self._run(_LINK_BODY)
        self._paint_mode()
        self._push_harbours()

    def _run(self, body: str) -> None:
        self._client.run_javascript(_WHEN_READY % {'map_id': self.map.id, 'body': body})

    # ── Kortlag ─────────────────────────────────────────────────────
    def _street_layer(self, z_index: int = 1):
        return self.map.tile_layer(
            url_template=STREET_DARK if self._dark else STREET_LIGHT,
            options={'attribution': STREET_ATTRIBUTION, 'maxZoom': 19,
                     'subdomains': 'abcd', 'zIndex': z_index})

    def _add_base(self) -> None:
        """Læg grundkortet på.

        Søkortet er tre lag. Nederst det almindelige kort, øverst Esris havkort
        med dybdeforhold — men kun så længe Esri har fliser. Over zoom 12 er der
        ikke flere, og et strakt billede af niveau 10 er ikke et kort at finde
        et havneindløb efter. Der forsvinder havkortet, og det skarpe kort
        nedenunder kommer frem. Man planlægger efter dybderne og lægger til
        efter detaljerne.
        """
        if self._style == CHART:
            self._base = [
                self._street_layer(0),
                self.map.tile_layer(url_template=OCEAN_TILES, options={
                    'attribution': OCEAN_ATTRIBUTION,
                    'maxZoom': CHART_FADE_ZOOM, 'maxNativeZoom': OCEAN_NATIVE_ZOOM,
                    'className': 'chart-tiles', 'zIndex': 1}),
                self.map.tile_layer(url_template=OCEAN_LABELS, options={
                    'maxZoom': CHART_FADE_ZOOM, 'maxNativeZoom': OCEAN_NATIVE_ZOOM,
                    'className': 'chart-tiles', 'zIndex': 2}),
            ]
        else:
            self._base = [self._street_layer(1)]

    def _replace_base(self) -> None:
        for layer in self._base or []:
            self.map.remove_layer(layer)
        self._add_base()
        self._paint_mode()

    def _paint_mode(self) -> None:
        """Fortæl kortet om dets eget grundkort er mørkt."""
        dark = self._style == STREET and self._dark
        self._run(_BASE_MODE_BODY % {'dark': 'true' if dark else 'false'})

    def set_dark(self, dark: bool) -> None:
        """Skift grundkort, når brugeren skifter tema."""
        if dark == self._dark:
            return
        self._dark = dark
        if self._style == STREET:
            self._replace_base()

    @property
    def style(self) -> str:
        return self._style

    def set_style(self, style: str) -> None:
        if style == self._style:
            return
        self._style = style
        self._replace_base()

    @property
    def seamarks_on(self) -> bool:
        return self._seamarks is not None

    def toggle_seamarks(self) -> bool:
        """Slå søkortsymbolerne til og fra. Returnerer den nye tilstand."""
        if self._seamarks is not None:
            self.map.remove_layer(self._seamarks)
            self._seamarks = None
        else:
            self._seamarks = self.map.tile_layer(
                url_template=SEAMARK_TILES,
                options={'attribution': SEAMARK_ATTRIBUTION, 'maxZoom': 18,
                         'className': 'seamark-tiles', 'zIndex': 2})
        return self.seamarks_on

    # ── Havnelaget ──────────────────────────────────────────────────
    @property
    def harbours_on(self) -> bool:
        return self._harbours_on

    def toggle_harbours(self) -> bool:
        self._harbours_on = not self._harbours_on
        self._push_harbours()
        return self._harbours_on

    def _push_harbours(self) -> None:
        """Send havnelisten til browseren — kun første gang, den er stor."""
        data = 'null'
        if not self._harbours_sent:
            # Navnene skrives ind i HTML af browseren, så vinkelparenteser skal
            # ikke med. Ingen havn hedder noget med < eller >.
            rows = [[round(h.lat, 5), round(h.lon, 5),
                     h.name.replace('<', '').replace('>', ''),
                     h.detail.replace('<', '').replace('>', ''), h.berths]
                    for h in harbours.all_harbours()]
            data = json.dumps(rows, ensure_ascii=False, separators=(',', ':'))
            self._harbours_sent = bool(rows)
        self._run(_HARBOURS_BODY % {
            'data': data, 'min_zoom': HARBOUR_ZOOM,
            'label_zoom': HARBOUR_LABEL_ZOOM, 'max': HARBOUR_MAX,
            'on': 'true' if self._harbours_on else 'false'})

    # ── Begivenheder ────────────────────────────────────────────────
    def _handle_drag(self, e) -> None:
        index = self._marker_index.get(str(e.args.get('id')))
        if index is not None:
            self._on_drag(index, float(e.args['lat']), float(e.args['lng']))

    def _handle_harbour(self, e) -> None:
        self._on_harbour(float(e.args['lat']), float(e.args['lng']),
                         str(e.args.get('name') or 'Havn'))

    # ── Tegning ─────────────────────────────────────────────────────
    def draw(self, route: Route, plan: Plan | None = None) -> None:
        """Tegn ruten forfra. Er en afgang valgt, farves hvert ben efter vejret."""
        for layer in self._markers + self._lines:
            self.map.remove_layer(layer)
        self._markers.clear()
        self._lines.clear()
        self._marker_index.clear()

        if not route.waypoints:
            return

        self._draw_legs(route, plan)
        self._draw_stops(plan)
        self._draw_markers(route)

    def _draw_legs(self, route: Route, plan: Plan | None) -> None:
        worst = self._worst_status_per_leg(plan)
        for leg, track in enumerate(route.tracks):
            colour = STATUS_COLOR[worst.get(leg + 1, GO)] if worst else '#C8933B'
            path = [[lat, lon] for lat, lon in track]
            # Et bredt, gennemsigtigt lag under stregen gør ruten synlig
            # mod både lyse og mørke kortflader.
            self._lines.append(self.map.generic_layer(name='polyline', args=[
                path, {'color': '#000', 'weight': 7, 'opacity': .16, 'interactive': False},
            ]))
            self._lines.append(self.map.generic_layer(name='polyline', args=[
                path, {'color': colour, 'weight': 3, 'opacity': .95,
                       'dashArray': '9 7', 'lineCap': 'round', 'interactive': False},
            ]))

    def _draw_stops(self, plan: Plan | None) -> None:
        """Overnatningerne. Afstikkeren ind til kajen tegnes tyndt og prikket."""
        if not plan:
            return
        for stop in plan.stops:
            self._lines.append(self.map.generic_layer(name='circleMarker', args=[
                [stop.lat, stop.lon],
                {'radius': 9, 'weight': 3, 'color': '#ffffff',
                 'fillColor': '#6C5CE7', 'fillOpacity': .95, 'interactive': False},
            ]))

    @staticmethod
    def _worst_status_per_leg(plan: Plan | None) -> dict[int, str]:
        if not plan:
            return {}
        rank = {'go': 0, 'warn': 1, 'stop': 2}
        worst: dict[int, str] = {}
        for s in plan.segments:
            current = worst.get(s.leg)
            if current is None or rank[s.status] > rank[current]:
                worst[s.leg] = s.status
        return worst

    def _draw_markers(self, route: Route) -> None:
        specs: dict[str, dict] = {}
        waypoints = route.waypoints
        last = len(waypoints) - 1
        for i, wp in enumerate(waypoints):
            marker = self.map.marker(latlng=(wp.lat, wp.lon)).draggable()
            self._markers.append(marker)
            self._marker_index[str(marker.id)] = i
            kind = 'start' if i == 0 else 'end' if i == last and last > 0 else 'via'
            specs[str(marker.id)] = {
                'kind': kind,
                'label': str(i + 1),
                'name': wp.name.replace('<', '').replace('>', ''),
            }

        self._run(_MARKERS_BODY % {'specs': json.dumps(specs, ensure_ascii=False)})

    # ── Navigation ──────────────────────────────────────────────────
    def fit(self, route: Route) -> None:
        """Zoom så hele ruten er i billedet."""
        points = [p for track in route.tracks for p in track] or \
                 [(w.lat, w.lon) for w in route.waypoints]
        if not points:
            self._run(_FIT_BODY % {'points': json.dumps([list(HOME)]),
                                   'zoom': HOME_ZOOM})
        elif len(route.waypoints) == 1:
            self._run(_FIT_BODY % {'points': json.dumps([list(points[0])]), 'zoom': 11})
        else:
            self._run(_FIT_BODY % {
                'points': json.dumps([[lat, lon] for lat, lon in points]), 'zoom': 12})

    def focus(self, lat: float, lon: float, zoom: int = 12) -> None:
        self.map.run_map_method('flyTo', [lat, lon], zoom, {'duration': .8})
