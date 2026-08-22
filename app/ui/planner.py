"""Brugerfladen: trinnene Rute → Afgangstid → Sejlplan.

Flowet er bygget som tre trin, fordi det er den rækkefølge man rent faktisk
planlægger i. Man kan altid gå tilbage, men aldrig frem til noget, der ikke er
beregnet endnu — så er der ingen blindgyder at falde i.

Ruten gennem vandet regnes i en baggrundstråd. Den tager sjældent mere end et
øjeblik, men den skal aldrig kunne fryse fladen, så panelet viser at der bliver
regnet, og kortet retter sig, når svaret er der.
"""
from __future__ import annotations

import asyncio
import html
import json
import time
from datetime import date

from nicegui import ui

from .. import (ai, geocode, harbours, landmask, narrative, offline, pwa,
                searoute, share, theme, weather, weatherbound)
from ..config import settings
from ..dates import clock, day, day_time, full, month, spell
from ..sailing import (GO, STATUS_COLOR, STATUS_LABEL, STOP, WARN, Waypoint,
                       beaufort, compass, find_windows, haversine,
                       point_of_sail)
from ..state import Session, signature
from . import help as helpui
from . import myroutes
from .mapview import RouteMap

# "Afgang" er også en havns rolle i ruten. Trinnet hedder derfor
# "Afgangstid" — det er dét, man vælger dér.
STEPS = [(1, 'Rute'), (2, 'Afgangstid'), (3, 'Sejlplan')]

# To pladser i ruten er lige gode, hvis de ligger inden for det her af
# hinanden i ekstra sømil. Så spørger vi i stedet for at gætte — det er
# skipperens rute.
AMBIGUOUS_NM = 3.0

QUICK_START = ['København', 'Helsingør', 'Aarhus', 'Svendborg',
               'Bornholm', 'Skagen', 'Samsø', 'Marstal']

# Bundskuffen på telefonen. Tre stop: et kig, halvdelen, og næsten hele skærmen.
# Det er de tre, man har brug for — se kortet med ruten nedenunder, arbejde med
# begge dele, eller læse en lang liste.
SHEET_JS = """
(function () {
  const shell = document.querySelector('.app-shell');
  const grip = document.querySelector('.sheet-grip');
  if (!shell || !grip || grip.dataset.wired) return;
  grip.dataset.wired = '1';

  const STOPS = [0.26, 0.58, 0.94];
  // Mindst 1, så en skjult fane ikke kan dividere med nul og slå skuffen i.
  // Headeren er hoejere paa en iPhone, hvor statuslinjen ligger oven i den.
  // Derfor maales den i stedet for at antage seksoghalvtreds.
  const top = () => (document.querySelector('.app-header')
                     || {offsetHeight: 56}).offsetHeight;
  const height = () => Math.max(1, shell.getBoundingClientRect().height - top());
  const now = () => parseFloat(getComputedStyle(shell).getPropertyValue('--sheet')) || 0.58;
  const set = (f) => {
    shell.style.setProperty('--sheet', String(f));
    // Er skuffen naesten helt oppe, er kortet alligevel daekket. Saa skal
    // kortknapperne ikke stikke halvt op bag skuffekanten og se knaekkede ud
    // - de skal traede af.
    shell.classList.toggle('sheet-tall', f > 0.72);
  };

  let from = 0, at = 0, dragging = false;

  grip.addEventListener('pointerdown', (e) => {
    dragging = true; from = e.clientY; at = now();
    shell.classList.add('sheet-dragging');
    grip.setPointerCapture(e.pointerId);
  });
  grip.addEventListener('pointermove', (e) => {
    if (!dragging) return;
    set(Math.min(0.95, Math.max(0.10, at + (from - e.clientY) / height())));
  });
  const settle = () => {
    if (!dragging) return;
    dragging = false;
    shell.classList.remove('sheet-dragging');
    const here = now();
    // Nærmeste stop vinder. Et lille ryk skal ikke kunne smide skuffen helt væk.
    set(STOPS.reduce((a, b) => Math.abs(b - here) < Math.abs(a - here) ? b : a));
  };
  grip.addEventListener('pointerup', settle);
  grip.addEventListener('pointercancel', settle);
  // Et tryk på håndtaget skifter mellem halv og fuld — hurtigere end at trække.
  grip.addEventListener('dblclick', () => set(now() > 0.7 ? STOPS[1] : STOPS[2]));
})();
"""


def esc(text: str) -> str:
    return html.escape(str(text), quote=True)


def dk(value: float, decimals: int = 1, sign: bool = False) -> str:
    """Tal med komma som decimaltegn. Det er sådan de skrives på dansk."""
    text = f'{value:{"+" if sign else ""}.{decimals}f}'
    return text.replace('.', ',')


def _cur_tone(seg) -> str:
    """Strøm med er grøn, strøm imod er rød. Tværs er hverken eller."""
    if seg.cur_along_kn > 0.15:
        return 'var(--go)'
    if seg.cur_along_kn < -0.15:
        return 'var(--stop)'
    return 'var(--txt-3)'


def nm(value: float) -> str:
    return dk(value, 1)


def _guide_link(h) -> None:
    """Knappen ud til havneguiden, hvis vi ved, hvor havnen står omtalt.

    Sejlplan siger, hvornår du kan sejle derhen. Guiden siger, hvad der venter:
    pladser, priser, vand på broen, hvordan indsejlingen ser ud. To tryk skal
    der ikke til, og en havn uden sikker kobling får ingen knap — et link, der
    fører til den forkerte havn, er værre end intet.
    """
    if not getattr(h, 'guide_url', ''):
        return
    # Et gråt ikon klemt inde mellem to andre ikoner kan ingen se — og det gør
    # ingen forskel, at det virker. Der skal stå, hvad det er.
    link = ui.link('Havneguide ↗', h.guide_url) \
        .props('target="_blank" rel="noopener"') \
        .classes('text-[11px] text-[var(--accent)] no-underline '
                 'hover:underline mt-0.5 inline-block')
    # Rækken under lægger havnen ind som mellemstop. Det skal linket ikke også.
    link.on('click.stop', lambda _: None)


def chip(icon: str, text: str, kind: str = '') -> str:
    """En lille mærkat med ikon og tal.

    Der stod emoji her før — 💨 🌊 ⛽. De tegnes af styresystemet, ikke af os,
    så de så forskellige ud på Windows og på en iPhone og passede ingen af
    stederne til resten af skriften. Material-ikonerne er de samme, appen
    bruger alle andre steder.
    """
    css = f'chip chip--{kind}' if kind else 'chip'
    return (f'<span class="{css} tnum">'
            f'<span class="material-icons chip-ico">{icon}</span>{esc(text)}</span>')


class Planner:
    """Hele planlæggeren for én bruger."""

    def __init__(self) -> None:
        self.s = Session.restore()
        self.map: RouteMap | None = None
        self._search_task: asyncio.Task | None = None
        self._route_task: asyncio.Task | None = None
        self._suggestions: list[geocode.Place] = []
        self._searching = False
        self._no_hits = ''
        self._busy = ''
        self._nav = 'none'      # retning for skiftet mellem trin: fwd, back, none
        # Hvilke afsnit i sejlplanen der staar aabne. Tomt = som de
        # starter, og de lange starter lukkede.
        self._sections: dict[str, bool] = {}
        self.search_input: ui.input | None = None
        # Baggrundsopgaver skal opdatere netop den her browser. NiceGUI's
        # underforståede klient er ikke sat, når en opgave vågner op igen, så
        # vi holder fast i vores egen og går ind i den, før vi rører fladen.
        self.client = ui.context.client
        self.s.client = self.client

    # ════════════════════════════════════════════════════════════════
    # Opbygning
    # ════════════════════════════════════════════════════════════════
    def build(self) -> None:
        # Hele appen bor i en skal, der er spændt ud over skærmen. Det er dét,
        # der gør at panelet kan rulle uafhængigt af hvor langt indholdet er.
        with ui.element('div').classes('app-shell'):
            self._header()

            with ui.element('div').classes(
                    'work flex flex-col-reverse md:flex-row w-full flex-1 min-h-0 '
                    'gap-0 overflow-hidden'):

                # ── Arbejdspanel ──
                # På en stor skærm er det en spalte ved siden af kortet. På en
                # telefon er det en skuffe, der ligger oven på kortet og kan
                # trækkes op og ned — dér er der ikke plads til at dele skærmen
                # i to, og kortet er alligevel dét, man peger på.
                #
                # `md:h-full` er ikke pynt. Uden en fast højde bliver en flex-
                # række så høj som sit højeste barn, og så vokser panelet med
                # sit indhold i stedet for at rulle: ti afgangskort blev til
                # 1679 px inde i en række på 722, og resten blev klippet væk.
                with ui.element('aside').classes(
                        'sheet w-full md:w-[430px] md:h-full flex flex-col min-h-0 '
                        'basis-[58%] md:basis-auto md:flex-none '
                        'border-t md:border-t-0 md:border-r '
                        'border-[var(--line)] bg-[var(--sea-2)] z-10'):
                    ui.html('<div class="sheet-grip"><i></i></div>')
                    with ui.element('div').classes('px-4 pt-1 md:pt-3 pb-2 shrink-0'):
                        self.stepbar()
                    with ui.element('div').classes('scroll-y flex-1 min-h-0 px-4 pb-4'):
                        self.panel()
                    # Handlingslinjen ligger uden for rullestrømmen. En rute med
                    # femten ben må ikke kunne skubbe båd, datoer og knappen
                    # ud under skærmkanten.
                    with ui.element('div').classes('shrink-0'):
                        self.action_bar()

                # ── Kort ──
                with ui.element('div').classes(
                        'mapwrap relative min-h-0 basis-[42%] shrink-0 md:h-full '
                        'md:basis-auto md:flex-1 md:shrink'):
                    self.map = RouteMap(on_click=self._map_clicked,
                                        on_drag=self._marker_dragged,
                                        on_harbour=self._harbour_clicked,
                                        dark=bool(self.dark.value))
                    self._map_controls()
                    self._map_overlay()
                    self.plan_view()

        ui.run_javascript(SHEET_JS)
        self._redraw_map(fit=True)
        self._schedule_route()

    def _header(self) -> None:
        with ui.element('header').classes('app-header text-[var(--txt-1)]'):

            ui.icon('sailing').classes('text-[22px] text-[var(--accent)]')
            ui.label('Sejlplan').classes('text-[17px] font-bold tracking-tight')

            self.header_summary()

            ui.element('div').classes('flex-1')

            # Båden stod også her som en knap, der åbnede den samme dialog som
            # tandhjulet. To veje til det samme sted er én for meget — og båden
            # står nu tydeligt i panelets "Turen"-liste.
            ui.button(icon='menu_book', on_click=helpui.manual_dialog) \
                .props('flat round dense').tooltip('Manual og hjælp')
            ui.button(icon='bookmarks', on_click=self._open_routes) \
                .props('flat round dense').tooltip('Mine gemte ruter')
            ui.button(icon='tune', on_click=self._open_settings) \
                .props('flat round dense').tooltip('Båd, grænser og sejldøgn')
            self.share_button()

            self.dark = ui.dark_mode(value=False)
            ui.button(icon='dark_mode', on_click=self._toggle_theme) \
                .props('flat round dense').tooltip('Skift mellem lyst og mørkt')

    @ui.refreshable_method
    def header_summary(self) -> None:
        """Rutens overskrift i toppen — kun når der faktisk er en rute."""
        if len(self.s.waypoints) < 2:
            return
        with ui.element('div').classes('hidden lg:flex items-center gap-2 ml-3 pl-3 '
                                       'border-l border-[var(--line)]'):
            ui.label(f'{self.s.waypoints[0].name} → {self.s.waypoints[-1].name}') \
                .classes('text-[13px] font-semibold truncate max-w-[26ch]')
            ui.html(f'<span class="chip tnum">{self.s.total_nm:.0f} sm</span>')

    def share_button(self) -> None:
        with ui.button(icon='share').props('flat round dense') \
                .tooltip('Del eller eksportér ruten'):
            with ui.menu().classes('min-w-[230px]'):
                ui.menu_item('Kopiér delelink', self._copy_link)
                ui.menu_item('Hent GPX til kortplotter', self._download_gpx)
                ui.separator()
                ui.menu_item('Vend ruten om', self._reverse_route)
                ui.menu_item('Ryd hele ruten', self._clear_route)

    def _map_controls(self) -> None:
        """Kortvælger og genveje i kortets øverste højre hjørne."""
        with ui.element('div').classes(
                'map-tools absolute top-3 right-3 z-[500] flex flex-col items-end gap-2'):

            with ui.element('div').classes('seg'):
                self.style_btns = {}
                for key, label, tip in (
                        ('chart', 'Søkort', 'Havkort med dybdeforhold'),
                        ('street', 'Landkort', 'Almindeligt kort med veje og byer')):
                    item = ui.element('div').classes('seg-item')
                    with item:
                        ui.label(label)
                    item.tooltip(tip)
                    item.on('click', lambda _, k=key: self._set_map_style(k))
                    self.style_btns[key] = item
                self._paint_style_buttons()

            # Knapperne har tekst under ikonet og står i én flade. Et anker og
            # en bølge er ikke tegn, man bare kan regne ud, og på en telefon
            # findes der ingen tooltip at holde musen over. Havnelaget er dét,
            # appen kan — så skal man kunne se, at knappen findes.
            with ui.element('div').classes('map-stack'):
                self.harbour_btn = self._map_button(
                    'anchor', 'Havne', self._toggle_harbours, on=True,
                    tip='Vis alle lystbådehavne — klik på en for at lægge den i ruten')
                self.seamark_btn = self._map_button(
                    'waves', 'Sømærker', self._toggle_seamarks,
                    tip='Bøjer, fyr og sejlløb fra OpenSeaMap')
                self._map_button(
                    'zoom_out_map', 'Hele ruten',
                    lambda: self.map and self.map.fit(self.s.route),
                    tip='Zoom ud, så hele ruten er i billedet')

    @staticmethod
    def _map_button(icon: str, label: str, on_click, on: bool = False,
                    tip: str = ''):
        btn = ui.button(on_click=on_click).props('flat dense no-caps') \
            .classes('map-btn map-btn--tall' + (' map-btn--on' if on else ''))
        with btn:
            with ui.element('div').classes('flex flex-col items-center gap-0.5'):
                ui.icon(icon).classes('text-[19px]')
                ui.label(label).classes('map-btn-label')
        if tip:
            btn.tooltip(tip)
        return btn

    def _paint_style_buttons(self) -> None:
        active = self.map.style if self.map else 'chart'
        for key, item in self.style_btns.items():
            on = key == active
            item.classes(add='seg-item--on' if on else '',
                         remove='' if on else 'seg-item--on')

    def _set_map_style(self, style: str) -> None:
        if not self.map:
            return
        self.map.set_style(style)
        self._paint_style_buttons()

    def _toggle_seamarks(self) -> None:
        if not self.map:
            return
        on = self.map.toggle_seamarks()
        self.seamark_btn.classes(add='map-btn--on' if on else '',
                                 remove='' if on else 'map-btn--on')
        ui.notify('Søkortsymboler ' + ('vist' if on else 'skjult'), position='bottom')

    def _toggle_harbours(self) -> None:
        if not self.map:
            return
        on = self.map.toggle_harbours()
        self.harbour_btn.classes(add='map-btn--on' if on else '',
                                 remove='' if on else 'map-btn--on')
        ui.notify('Havnene vises, når du zoomer ind. Klik på en for at lægge '
                  'den i ruten.' if on else 'Havnene er skjult', position='bottom')

    def _map_overlay(self) -> None:
        """Diskret hjælpetekst nederst på kortet."""
        with ui.element('div').classes(
                'absolute bottom-6 left-1/2 -translate-x-1/2 z-[500] pointer-events-none '
                'w-max max-w-[92%]'):
            self.map_hint()

    @ui.refreshable_method
    def map_hint(self) -> None:
        if self.s.routing:
            ui.html(
                '<div class="float px-4 py-2 text-[12.5px] text-[var(--txt-2)] '
                'flex items-center gap-2.5">'
                '<span class="spinner-dot"></span>Lægger ruten udenom land…</div>')
            return
        if len(self.s.waypoints) >= 2:
            return
        text = ('Klik på kortet, eller søg efter en havn, for at sætte afgangshavnen'
                if not self.s.waypoints else 'Klik igen for at sætte destinationen')
        ui.html(
            f'<div class="float px-4 py-2 text-[12.5px] text-[var(--txt-2)] '
            f'flex items-center gap-2.5">'
            f'<span class="material-icons text-[16px] text-[var(--accent)]">touch_app</span>'
            f'{esc(text)}</div>')

    # ════════════════════════════════════════════════════════════════
    # Trinviser
    # ════════════════════════════════════════════════════════════════
    @ui.refreshable_method
    def stepbar(self) -> None:
        with ui.element('div').classes('stepbar'):
            for i, (num, label) in enumerate(STEPS):
                if i:
                    ui.html('<div class="step-rule"></div>')
                unlocked = self._step_unlocked(num)
                state = ('step--active' if num == self.s.step
                         else 'step--done' if unlocked and num < self.s.step
                         else '' if unlocked else 'step--locked')
                mark = ('check' if unlocked and num < self.s.step else str(num))
                icon = ('<span class="material-icons" style="font-size:13px">check</span>'
                        if mark == 'check' else mark)
                el = ui.html(f'<div class="step {state}">'
                             f'<span class="step-num">{icon}</span>{esc(label)}</div>')
                if unlocked:
                    el.on('click', lambda _, n=num: self._go_to_step(n))
                else:
                    # Et trin, der ikke gør noget, når man trykker, ligner et
                    # ødelagt trin. Sig hvorfor det ikke kan bruges endnu.
                    el.tooltip(self._step_why(num))
                    el.on('click', lambda _, n=num: ui.notify(
                        self._step_why(n), position='bottom'))

    def _step_unlocked(self, num: int) -> bool:
        if num == 1:
            return True
        if num == 2:
            return self.s.can_analyse
        return bool(self.s.windows)

    @staticmethod
    def _step_why(num: int) -> str:
        """Hvorfor trinnet ikke kan bruges endnu."""
        if num == 2:
            return ('Læg først en rute med mindst to punkter — så kan vi '
                    'regne afgangstider ud.')
        return ('Tryk Find bedste afgangstider først, og vælg en afgang. '
                'Så skriver vi sejlplanen.')

    def _go_to_step(self, num: int) -> None:
        if not self._step_unlocked(num):
            return
        # Retningen huskes, så panelet glider den vej, man går. Det er det, der
        # gør at man kan mærke om man er på vej frem eller tilbage, i stedet for
        # at indholdet bare bliver skiftet ud under næsen på én.
        self._nav = 'back' if num < self.s.step else 'fwd'
        self.s.step = num
        self.refresh()

    # ════════════════════════════════════════════════════════════════
    # Panelet
    # ════════════════════════════════════════════════════════════════
    @ui.refreshable_method
    def panel(self) -> None:
        with ui.element('div').classes(f'swap swap--{self._nav}'):
            if self._busy:
                self._busy_panel()
            elif self.s.step == 1:
                self._route_panel()
            elif self.s.step == 2:
                self._windows_panel()
            else:
                self._analysis_panel()

    def _busy_panel(self) -> None:
        with ui.column().classes('w-full items-center justify-center gap-4 pt-24'):
            ui.spinner('dots', size='2.6rem').classes('text-[var(--accent)]')
            ui.label(self._busy).classes('text-[13.5px] text-[var(--txt-2)]')

    # ── Trin 1: rute ────────────────────────────────────────────────
    def _route_panel(self) -> None:
        self._search_box()
        self.suggestion_list()
        self.waypoint_list()

    def _search_box(self) -> None:
        with ui.element('div').classes('relative mb-2'):
            self.search_input = ui.input(placeholder='Søg havn, ø eller position…') \
                .props('outlined dense clearable autocomplete=off '
                       'input-class="text-[14.5px]"') \
                .classes('w-full search') \
                .on('keydown.enter', self._accept_first_suggestion)
            with self.search_input.add_slot('prepend'):
                ui.icon('search').classes('text-[19px] text-[var(--txt-3)]')
            self.search_input.on_value_change(self._search_changed)

    @ui.refreshable_method
    def suggestion_list(self) -> None:
        if self._searching:
            with ui.row().classes('items-center gap-2 px-2 py-2'):
                ui.spinner(size='16px').classes('text-[var(--accent)]')
                ui.label('Søger…').classes('text-[12.5px] text-[var(--txt-3)]')
            return

        if self._no_hits:
            with ui.element('div').classes(
                    'card px-4 py-3 mb-3 text-[12.5px] text-[var(--txt-3)] leading-snug'):
                ui.label(f'Ingen steder hedder "{self._no_hits}". Prøv et andet '
                         f'navn, eller tast en position som 55.69, 12.60.')
            return

        if not self._suggestions:
            return

        with ui.element('div').classes('card overflow-hidden mb-3'):
            for i, place in enumerate(self._suggestions):
                if i:
                    ui.html('<div class="hairline"></div>')
                row = ui.element('div').classes(
                    'flex items-center gap-3 px-3 py-2.5 cursor-pointer '
                    'hover:bg-[var(--sea-3)] transition-colors').props(
                    f'data-spot="{place.lat:.5f},{place.lon:.5f}"')
                with row:
                    ui.icon(place.icon).classes('text-[18px] text-[var(--accent)] shrink-0')
                    with ui.element('div').classes('min-w-0 flex-1'):
                        ui.label(place.name).classes('text-[13.5px] font-semibold truncate')
                        ui.label(place.detail).classes('text-[11.5px] text-[var(--txt-3)] truncate')
                    ui.icon('add').classes('text-[17px] text-[var(--txt-3)] shrink-0')
                row.on('click', lambda _, p=place: self._add_place(p))

    @ui.refreshable_method
    def waypoint_list(self) -> None:
        if not self.s.waypoints:
            self._empty_route()
            return

        with ui.element('div').classes('flex items-center gap-2 mt-3 mb-1.5'):
            ui.html('<span class="section-label">Ruten</span>')
            if self.s.saved_name:
                # Arbejder man i en gemt rute, skal man kunne se hvilken. Navnet
                # er brugerens eget og kan være langt — det må ikke kunne skubbe
                # Gem-knappen ud over kanten på en telefon.
                ui.html('<span class="chip" style="max-width:16ch;overflow:hidden;'
                        'text-overflow:ellipsis;white-space:nowrap">'
                        f'{esc(self.s.saved_name)}</span>')
            ui.element('div').classes('flex-1')
            if self.s.routing:
                ui.html('<span class="text-[11px] text-[var(--txt-3)]">'
                        'beregner havvejen…</span>')
            else:
                ui.button('Gem', icon='bookmark_border', on_click=self._save_route) \
                    .props('flat dense no-caps size=sm') \
                    .classes('text-[var(--accent)] shrink-0')

        with ui.element('div').classes('card px-1.5 py-1.5 mb-3'):
            last = len(self.s.waypoints) - 1
            for i, wp in enumerate(self.s.waypoints):
                self._waypoint_row(i, wp, last)
                if i < last:
                    self._leg_row(i)

        self._route_footer()

    def _waypoint_row(self, i: int, wp: Waypoint, last: int) -> None:
        kind = 'start' if i == 0 else 'end' if i == last and last > 0 else 'via'
        role = {'start': 'Afgang', 'end': 'Destination', 'via': 'Mellemstop'}[kind]

        with ui.element('div').classes('wp group').props(
                f'data-spot="{wp.lat:.5f},{wp.lon:.5f}"'):
            ui.html(f'<div class="wp-pin wp-pin--{kind}">{i + 1}</div>')

            info = ui.element('div').classes('min-w-0 flex-1 cursor-pointer')
            with info:
                ui.label(wp.name).classes('wp-name truncate')
                ui.label(f'{role} · {wp.where}').classes('wp-meta truncate')
            info.on('click', lambda _, w=wp: self.map and self.map.focus(w.lat, w.lon))
            info.tooltip('Vis på kortet')

            # `wp-tools` dæmper kun knapperne på skærme med mus. På en telefon
            # er der ingen hover, og halvgennemsigtige knapper ligner slukkede.
            with ui.element('div').classes('wp-tools flex items-center shrink-0'):
                ui.button(icon='keyboard_arrow_up', on_click=lambda _, k=i: self._move(k, -1)) \
                    .props('flat dense round size=sm').set_enabled(i > 0)
                ui.button(icon='keyboard_arrow_down', on_click=lambda _, k=i: self._move(k, 1)) \
                    .props('flat dense round size=sm').set_enabled(i < last)
                ui.button(icon='close', on_click=lambda _, k=i: self._remove(k)) \
                    .props('flat dense round size=sm').classes('text-[var(--stop)]')

    def _leg_row(self, i: int) -> None:
        """Benets længde og kurs. Tallene er havvejens, ikke luftlinjens."""
        route = self.s.route
        a, b = self.s.waypoints[i], self.s.waypoints[i + 1]
        direct = haversine(a.lat, a.lon, b.lat, b.lon)
        dist = route.leg_nm(i) if self.s.route_ready else direct
        steps = [s for s in route.steps if s.leg == i]
        crs = steps[0].course if steps else 0

        text = f'{nm(dist)} sømil · kurs {crs:.0f}° {compass(crs)}'
        if self.s.route_ready and dist > direct + 0.6:
            text += f' · {nm(dist - direct)} sm udenom land'
        with ui.element('div').classes('leg'):
            ui.html('<div class="leg-rule"></div>')
            ui.label(text).classes('tnum')

    def _empty_route(self) -> None:
        with ui.element('div').classes('empty'):
            ui.icon('explore').classes('text-[42px] text-[var(--accent)] opacity-45 mb-2')
            ui.label('Læg din rute').classes('empty-title')
            ui.label('Søg efter en havn foroven, klik direkte på kortet, eller slå '
                     'havnelaget til og vælg en havn. Du skal bruge mindst to punkter.') \
                .classes('empty-sub')

        if self.s.routes:
            # Har man ruter på hylden, er det her, man vil have fat i dem —
            # ikke bag et ikon oppe i hjørnet.
            with ui.element('div').classes('flex items-center gap-2 mt-1 mb-2'):
                ui.html('<span class="section-label">Mine ruter</span>')
                ui.element('div').classes('flex-1')
                ui.button('Se alle', on_click=self._open_routes) \
                    .props('flat dense no-caps size=sm') \
                    .classes('text-[var(--accent)] shrink-0')
            myroutes.rows(self.s, self._open_saved, lambda: self.refresh(fit=True))

        ui.label('Kom hurtigt i gang').classes('section-label mt-2 mb-2 block')
        with ui.row().classes('gap-1.5 flex-wrap'):
            for name in QUICK_START:
                ui.button(name, on_click=lambda _, n=name: self._add_named(n)) \
                    .props('flat dense no-caps size=sm') \
                    .classes('chip !px-2.5 !py-1 hover:!bg-[var(--accent-soft)] '
                             'hover:!text-[var(--accent)]')

    def _route_footer(self) -> None:
        n_legs = len(self.s.waypoints) - 1
        if n_legs < 1:
            ui.label('Tilføj mindst ét punkt mere for at kunne beregne afgangstider.') \
                .classes('text-[12.5px] text-[var(--txt-3)] px-1')
            return

        route = self.s.route
        if self.s.route_ready and not route.ok:
            ui.html('<div class="chip chip--warn mb-2">Et ben kunne ikke lægges '
                    'sikkert udenom land — kontrollér det selv på søkortet.</div>')
        self._estimate_card(route)
        self._trip_rows()
        self._stopover_preview(route)

    def _estimate_card(self, route) -> None:
        """Hvad turen ser ud til at blive — før man trykker og venter.

        Ruten kender vi med det samme. Det koster ingenting at sige hvor langt
        og hvor længe, og om det overhovedet kan nås inden for ét sejldøgn.
        Uden det trykker man i blinde og opdager først tyve sekunder senere, at
        turen kræver to overnatninger.
        """
        if not self.s.route_ready:
            return
        text, days = narrative.estimate(self.s.boat, route, self.s.limits)
        note = narrative.days_note(days, self.s.limits)

        with ui.element('div').classes('card px-4 py-3 mt-3'):
            with ui.element('div').classes('flex items-baseline gap-2'):
                ui.label(text).classes('text-[14px] font-semibold tnum flex-1')
                if days > 1:
                    ui.html(f'<span class="chip">{days} døgn</span>')
            ui.label(note).classes(
                'text-[11.5px] text-[var(--txt-3)] leading-snug mt-1 block')

    def _trip_rows(self) -> None:
        """Båd, datoer og sejldøgn som navngivne rækker med deres værdi.

        De stod før som én forkortet streng — "20. aug–23. aug · sejldøgn 07–20
        · maks 20 kn". Man kunne læse den, men man kunne ikke se hvad der var
        hvad. En række med navn til venstre og værdi til højre kan man skimme.
        """
        lim, boat = self.s.limits, self.s.boat
        rows = [
            ('directions_boat', 'Båd', boat.name),
            ('event', 'Hvornår', f'{self._short_date(lim.date_from)} – '
                                 f'{self._short_date(lim.date_to)}'),
            ('schedule', 'Sejldøgn', f'{lim.day_start:02d}:00 – {lim.day_end:02d}:00'
                                     + (' · også nat' if lim.night_ok else '')),
            ('air', 'Grænser', f'{lim.max_wind:.0f} kn vind · '
                               f'{dk(lim.max_wave)} m bølger'),
        ]
        ui.label('Turen').classes('section-label mt-4 mb-1.5 block')
        with ui.element('div').classes('card overflow-hidden'):
            for i, (icon, label, value) in enumerate(rows):
                if i:
                    ui.html('<div class="hairline"></div>')
                row = ui.element('div').classes(
                    'flex items-center gap-3 px-3.5 py-2.5 cursor-pointer '
                    'hover:bg-[var(--sea-3)] transition-colors')
                with row:
                    ui.icon(icon).classes('text-[17px] text-[var(--txt-3)] shrink-0')
                    ui.label(label).classes('text-[13px] font-medium shrink-0')
                    ui.label(value).classes(
                        'text-[13px] text-[var(--txt-2)] flex-1 text-right truncate')
                    ui.icon('chevron_right').classes(
                        'text-[18px] text-[var(--txt-3)] shrink-0 -mr-1')
                row.on('click', self._open_settings)

    def _stopover_preview(self, route) -> None:
        """Havnene langs ruten — dem man kan søge ind i, hvis vejret skifter.

        De er regnet ud alligevel, fordi planlæggeren skal bruge dem til
        overnatninger. At vise dem allerede her koster ingenting og svarer på
        det spørgsmål, enhver stiller sig selv inden en længere tur: hvor kan
        jeg gå ind undervejs?
        """
        if not self.s.route_ready:
            return
        # Rutens egne punkter er ikke "undervejs" — de er dér, man skal hen.
        margin = min(2.0, route.total_nm / 6)
        found = [(h, along, detour) for h, along, detour in harbours.stopovers(route)
                 if margin < along < route.total_nm - margin]
        if len(found) < 2:
            return

        # Spred dem ud over ruten i stedet for at vise ti havne i samme bugt.
        step = max(1, len(found) // 6)
        picked = found[::step][:6]

        with ui.element('div').classes('flex items-center gap-1 mt-4 mb-1'):
            ui.label('Havne undervejs').classes('section-label')
            helpui.dot('havne')
        ui.label('Steder du kan søge ind, hvis vejret skifter. Klik for at lægge '
                 'en ind som mellemstop.') \
            .classes('text-[11.5px] text-[var(--txt-3)] mb-2 block leading-snug')

        with ui.element('div').classes('card overflow-hidden'):
            for i, (h, along, detour) in enumerate(picked):
                if i:
                    ui.html('<div class="hairline"></div>')
                row = ui.element('div').classes(
                    'flex items-center gap-3 px-3 py-2 cursor-pointer '
                    'hover:bg-[var(--sea-3)] transition-colors').props(
                    f'data-spot="{h.lat:.5f},{h.lon:.5f}"')
                with row:
                    ui.icon('anchor').classes('text-[15px] text-[var(--txt-3)] shrink-0')
                    with ui.element('div').classes('min-w-0 flex-1'):
                        ui.label(h.name).classes('text-[13px] font-medium truncate block')
                        ui.label(f'efter {nm(along)} sm · {nm(detour)} sm ind fra ruten') \
                            .classes('text-[11px] text-[var(--txt-3)] tnum truncate block')
                        _guide_link(h)
                    ui.icon('add').classes('text-[16px] text-[var(--txt-3)] shrink-0')
                row.on('click', lambda _, x=h: self._add_place(geocode.from_harbour(x)))

    # ── Fast handlingslinje i bunden af panelet ─────────────────────
    @ui.refreshable_method
    def action_bar(self) -> None:
        """Det man skal kunne nå uanset hvor langt man har rullet."""
        if self._busy:
            return

        if self.s.step == 1:
            if len(self.s.waypoints) < 2:
                return
            self._route_action_bar()
        elif self.s.step == 2 and self.s.windows:
            with self._bar():
                ui.button('Se sejlplanen', icon='arrow_forward',
                          on_click=lambda: self._go_to_step(3)) \
                    .props('unelevated no-caps size=lg') \
                    .classes('w-full btn-primary')
        elif self.s.step == 3 and len(self.s.windows) > 1:
            with self._bar():
                ui.button('Vælg en anden afgang', icon='schedule',
                          on_click=lambda: self._go_to_step(2)) \
                    .props('outline no-caps').classes('w-full text-[var(--txt-2)]')

    @staticmethod
    def _bar():
        return ui.element('div').classes(
            'border-t border-[var(--line)] bg-[var(--sea-1)] px-4 py-3')

    def _route_action_bar(self) -> None:
        """Bunden af panelet: én knap, og intet andet.

        Før stod indstillingerne her som en sammenklappelig linje, der lignede
        en knap lige over den rigtige knap. To knap-agtige ting oven på hinanden
        er én for meget — nu bor indstillingerne oppe i panelet som navngivne
        rækker, og herNEDE er der kun dét, man skal trykke på.
        """
        with self._bar():
            ui.button('Find bedste afgangstider', icon='travel_explore',
                      on_click=self.run_analysis) \
                .props('unelevated no-caps size=lg') \
                .classes('w-full btn-primary')

    @staticmethod
    def _short_date(iso: str) -> str:
        try:
            d = date.fromisoformat(iso)
            return f'{d.day}. {month(d, short=True)}'
        except (TypeError, ValueError):
            return iso

    # ── Trin 2: afgangsvinduer ──────────────────────────────────────
    def _windows_panel(self) -> None:
        if not self.s.windows:
            with ui.element('div').classes('empty'):
                ui.icon('schedule').classes('text-[40px] text-[var(--txt-3)] mb-2')
                ui.label('Ingen beregning endnu').classes('empty-title')
                ui.label('Gå tilbage til Rute og tryk "Find bedste afgangstider".') \
                    .classes('empty-sub')
            ui.button('Tilbage til ruten', icon='arrow_back',
                      on_click=lambda: self._go_to_step(1)) \
                .props('outline no-caps').classes('w-full mt-3')
            return

        best = self.s.windows[0]
        days = len({w.depart.date() for w in self.s.windows})
        # Rækkefølgen er vores anbefaling, ikke en afgørelse. Alle de afgange,
        # der giver noget forskelligt, står på listen — også dem på en dag med
        # dårligere vejr. Valget er skipperens.
        ui.html(
            f'<div class="text-[12.5px] text-[var(--txt-2)] leading-snug mb-3">'
            f'{len(self.s.windows)} afgange at vælge imellem, fordelt på '
            f'{days} {"dag" if days == 1 else "dage"}. Vi vil pege på '
            f'<b>{esc(full(best.depart))}</b> — men vælg selv.</div>')

        for i, w in enumerate(self.s.windows):
            self._window_card(i, w)

    def _window_card(self, i: int, w) -> None:
        selected = i == self.s.selected
        rank = {0: 'BEDST', 1: 'NR. 2', 2: 'NR. 3'}.get(i, f'NR. {i + 1}')

        card = ui.element('div').classes(f'win mt-3 {"win--sel" if selected else ""}')
        with card:
            ui.html(f'<div class="win-rank">{rank}</div>')

            with ui.element('div').classes('flex items-baseline gap-2 mb-0.5'):
                ui.html(f'<div class="win-day">{esc(day(w.depart))}</div>')
                ui.element('div').classes('flex-1')
                ui.html(self._verdict_chip(w))

            with ui.element('div').classes('flex items-baseline gap-2'):
                ui.html(f'<div class="win-time tnum">{clock(w.depart)}</div>')
                # En afgang, der ikke når frem, må ikke stå med en ankomsttid.
                # Kortet viser så, hvor langt man kommer.
                if w.incomplete:
                    ui.html(f'<div class="win-arrive tnum">→ når '
                            f'{w.reached_nm:.0f} af {w.total_nm:.0f} sømil</div>')
                else:
                    ui.html(f'<div class="win-arrive tnum">→ {esc(day_time(w.arrival))} '
                            f'· {esc(spell(w.under_way_h))} under vejs</div>')

            if w.stops:
                names = ' · '.join(f'{s.name} {day_time(s.arrive)}' for s in w.stops)
                ui.html(f'<div class="win-stops">'
                        f'<span class="material-icons" style="font-size:14px">hotel</span>'
                        f'{esc(names)}</div>')

            ui.html(f'<div class="hourbar mt-2.5">{self._hourbar(w)}</div>')

            with ui.element('div').classes('flex gap-1.5 mt-2.5 flex-wrap'):
                ui.html(chip('air', f'{w.worst_wind_kn:.0f} kn'))
                ui.html(chip('waves', f'{dk(w.worst_wave_m)} m'))
                ui.html(chip('speed', f'{dk(w.avg_speed_kn)} kn'))
                if w.stops:
                    ui.html(chip('hotel', f'{w.nights} nat'))
                if w.night_hours:
                    ui.html(chip('dark_mode', f'{w.night_hours} t mørke'))
                if self.s.boat.is_motor and w.fuel_l:
                    ui.html(chip('local_gas_station', f'{w.fuel_l:.0f} l'))
                elif w.motor_hours:
                    ui.html(chip('settings', f'{w.motor_hours} t motor'))

        card.on('click', lambda _, k=i: self._select_window(k))

    @staticmethod
    def _verdict_chip(w) -> str:
        if w.late_arrival:
            return '<span class="chip chip--stop">Fremme efter sejldøgnet</span>'
        if w.red_hours:
            return f'<span class="chip chip--stop">{w.red_hours} t frarådes</span>'
        if w.yellow_hours:
            return f'<span class="chip chip--warn">{w.yellow_hours} t skærpet</span>'
        return '<span class="chip chip--go">Gode forhold</span>'

    @staticmethod
    def _hourbar(w) -> str:
        return ''.join(f'<i style="background:{STATUS_COLOR[s.status]}"'
                       f'{" class=night" if s.night else ""}></i>'
                       for s in w.segments)

    # ── Trin 3: analyse ─────────────────────────────────────────────
    def _analysis_panel(self) -> None:
        """Venstre side på trin 3: skift afgang. Selve planen står i hovedfeltet.

        Her er der ingen grund til at gentage hele afgangskortet — planen ved
        siden af siger allerede alt om den valgte. Én linje pr. afgang er nok
        til at skifte, og så fylder panelet ikke mere end det skal.
        """
        if not self.s.plan:
            self._go_to_step(2)
            return

        ui.html('<div class="text-[12.5px] text-[var(--txt-2)] leading-snug mb-2.5">'
                'Planen står til højre. Vælg en anden afgang her, så skrives '
                'den om med det samme.</div>')

        with ui.element('div').classes('card overflow-hidden'):
            for i, w in enumerate(self.s.windows):
                if i:
                    ui.html('<div class="hairline"></div>')
                self._departure_row(i, w)

    def _departure_row(self, i: int, w) -> None:
        """Én afgang på én linje — dato, klokkeslæt, dom og antal nætter."""
        chosen = i == self.s.selected
        row = ui.element('div').classes(
            'flex items-center gap-2.5 px-3 py-2 cursor-pointer transition-colors '
            + ('bg-[var(--accent-soft)]' if chosen else 'hover:bg-[var(--sea-3)]'))
        with row:
            ui.html(f'<i class="dot" style="background:'
                    f'{STATUS_COLOR[w.verdict]}"></i>')
            ui.label(day(w.depart)).classes(
                'text-[12px] text-[var(--txt-3)] w-[68px] shrink-0')
            ui.label(clock(w.depart)).classes(
                'text-[14px] font-bold tnum w-[46px] shrink-0'
                + (' text-[var(--accent)]' if chosen else ''))
            ui.label(f'→ {w.reached_nm:.0f}/{w.total_nm:.0f} sm'
                     if w.incomplete else f'→ {day_time(w.arrival)}').classes(
                'text-[11.5px] text-[var(--txt-3)] tnum flex-1 truncate')
            if w.stops:
                ui.html(chip('hotel', str(w.nights)).replace('chip ', 'chip shrink-0 '))
        row.on('click', lambda _, k=i: self._select_window(k))

    # ── Sejlplanen i hovedfeltet ────────────────────────────────────
    @ui.refreshable_method
    def plan_view(self) -> None:
        """Planen lægger sig over kortet, når man er nået til trin 3."""
        p = self.s.plan
        if self.s.step != 3 or not p:
            return

        boat = self.s.boat
        route = self.s.route
        names = ' → '.join(w.name for w in route.waypoints)

        self._stow_plan(boat, route, p)

        with ui.element('div').classes('plan-view scroll-y'):
            with ui.element('div').classes('mx-auto max-w-[78ch] px-5 md:px-8 py-6 md:py-8'):

                # ── Hoved ──
                with ui.element('div').classes(
                        'flex items-start gap-4 flex-wrap pb-4 mb-5 '
                        'border-b border-[var(--line)]'):
                    # `basis-full` paa telefonen: ellers klemmer knapperne
                    # teksten sammen i stedet for selv at rykke ned, og
                    # undertitlen blev brudt til ét ord per linje.
                    with ui.element('div').classes(
                            'min-w-0 basis-full md:basis-0 md:flex-1'):
                        ui.label('Sejlplan').classes('section-label')
                        ui.label(names).classes(
                            'text-[19px] md:text-[30px] font-bold leading-tight '
                            'tracking-tight mt-1 block')
                        # Nåede planen ikke frem, står der ingen ankomst i
                        # hovedet. Det er dét, øjet falder på først, og en
                        # ankomsttid, der ikke findes, er værre end ingen.
                        tail = (f'når {p.reached_nm:.0f} af {p.total_nm:.0f} sømil'
                                if p.incomplete else f'ankomst {full(p.arrival)}')
                        ui.label(f'{boat.name} · afgang {full(p.depart)} · {tail}') \
                            .classes('text-[13.5px] text-[var(--txt-2)] mt-1.5 block')
                    with ui.row().classes('gap-1.5 shrink-0'):
                        ui.button('Udskriv', icon='print', on_click=self._print_plan) \
                            .props('outline dense no-caps').classes('text-[var(--txt-2)]')
                        ui.button('Kopiér', icon='content_copy', on_click=self._copy_plan) \
                            .props('outline dense no-caps').classes('text-[var(--txt-2)]')
                        ui.button('Kortet', icon='arrow_back',
                                  on_click=lambda: self._go_to_step(2)) \
                            .props('outline dense no-caps') \
                            .classes('text-[var(--txt-2)]')

                self._plan_overview(p, boat, route)
                self._plan_warnings(p, boat)
                self._plan_days(p)
                self._key_figures(p, boat)
                self._plan_stretches(p, route, boat)
                self._weather_tab()
                self._ai_tab()

    def _plan_overview(self, p, boat, route) -> None:
        if not self._section('Overblik', 'overblik', 'sadan'):
            return
        with ui.element('div').classes('card px-4 py-3.5 mb-4'):
            for paragraph in narrative.overview(boat, route, p):
                ui.label(paragraph).classes(
                    'text-[13.5px] leading-relaxed text-[var(--txt-2)] mb-2 last:mb-0 block')

    # ── Afsnit i sejlplanen ─────────────────────────────────────────
    # Planen var én lang rulle. Time for time alene er fyrre rækker, og for at
    # komme til skippervurderingen skulle man forbi det hele. Nu kan hvert
    # afsnit klappes sammen, og de lange starter lukkede — de er opslagsværk,
    # ikke læsestof.
    def _toggle_section(self, key: str, standard: bool) -> None:
        self._sections[key] = not self._sections.get(key, standard)
        self.plan_view.refresh()

    def _section(self, title: str, key: str, topic: str = '',
                 standard: bool = True, hint: str = '') -> bool:
        """Tegn overskriften, og sig om indholdet skal med."""
        is_open = self._sections.get(key, standard)
        row = ui.element('div').classes(
            'flex items-center gap-1 mb-1.5 cursor-pointer select-none group')
        with row:
            ui.icon('expand_more').classes(
                'text-[18px] text-[var(--txt-3)] transition-transform '
                + ('' if is_open else '-rotate-90'))
            ui.label(title).classes('section-label')
            if topic:
                helpui.dot(topic)
            ui.element('div').classes('flex-1')
            if hint and not is_open:
                ui.label(hint).classes('text-[11px] text-[var(--txt-3)] tnum')
        row.on('click', lambda _: self._toggle_section(key, standard))
        return is_open

    def _outlook(self, p):
        """Hvad prognosen siger om dagene, efter man er fremme.

        Det er dét, der afgør, om turen skal lægges nu eller til næste weekend
        — og det er det eneste, ingen opdager selv, fordi man kigger på vejret
        frem til ankomsten og ikke længere.
        """
        route = self.s.route
        if not self.s.weather or not route.waypoints:
            return None
        try:
            series = weather.series_at(self.s.weather, route.total_nm,
                                       route.total_nm)
            return weatherbound.look_ahead(
                p, series, self.s.limits, route.waypoints[-1].name)
        except Exception:
            return None

    def _plan_warnings(self, p, boat) -> None:
        # De haster ikke lige meget. "Du kommer ikke hjem igen" og "husk
        # lanterner" stod før med det samme tegn i den samme farve — og så
        # holder man op med at læse dem. Nu står det, der haster, øverst.
        items = narrative.warnings(p, self.s.limits, boat, self._outlook(p))
        rank = {narrative.NOTE_STOP: 0, narrative.NOTE_WARN: 1,
                narrative.NOTE_INFO: 2, narrative.NOTE_GOOD: 3}
        items = sorted(items, key=lambda n: rank.get(n.level, 9))

        if not self._section('Vær opmærksom på', 'advarsler', 'graenser',
                             hint=f'{len(items)}'):
            return
        with ui.element('div').classes('card px-4 py-3.5 mb-4 flex flex-col gap-2.5'):
            for note in items:
                with ui.element('div').classes('flex gap-2.5 items-start'):
                    tone = narrative.NOTE_TONE.get(note.level, 'var(--txt-3)')
                    ui.icon(narrative.NOTE_ICON.get(note.level, 'info')) \
                        .style(f'color: {tone}') \
                        .classes('text-[17px] shrink-0 mt-0.5')
                    ui.label(note.text).classes(
                        'text-[13px] leading-relaxed text-[var(--txt-2)]')

    def _plan_days(self, p) -> None:
        """Turen delt op i de sejldøgn den falder i — og hvor der overnattes."""
        if len(p.days) < 2:
            return
        if not self._section('Dag for dag', 'dage', 'sejldogn',
                             hint=f'{len(p.days)} døgn'):
            return
        with ui.element('div').classes('daylist mb-4'):
            for i, d in enumerate(p.days):
                stop = p.stops[i] if i < len(p.stops) else None
                with ui.element('div').classes('card px-4 py-3.5'):
                    with ui.element('div').classes('flex items-baseline gap-2 mb-1'):
                        ui.html(f'<span class="daynum">{i + 1}</span>')
                        ui.label(f'{d.frm} → {d.to}') \
                            .classes('text-[13.5px] font-semibold truncate flex-1')
                        ui.html(f'<span class="chip tnum">{nm(d.nm)} sm</span>')
                    ui.label(f'{day(d.date, short=False)} · {clock(d.depart)}–'
                             f'{clock(d.arrive)} · {spell(d.under_way_h)} under vejs') \
                        .classes('text-[11.5px] text-[var(--txt-3)] block')
                    if stop:
                        ui.label(f'Overnatning i {stop.name}, {stop.detail}. '
                                 f'{nm(stop.detour_nm)} sømil ind fra ruten. '
                                 f'Videre {clock(stop.depart)} næste morgen.') \
                            .classes('text-[12.5px] text-[var(--txt-2)] mt-1.5 '
                                     'leading-relaxed block')
                        # Man skal ligge dér en nat. Så vil man vide, om der er
                        # vand på broen og plads til gæster.
                        url = harbours.guide_url_at(stop.lat, stop.lon)
                        if url:
                            ui.link('Læs om havnen i havnelods.dk →', url) \
                                .props('target="_blank" rel="noopener"') \
                                .classes('text-[12px] text-[var(--accent)] '
                                         'no-underline hover:underline mt-1 block')

    def _key_figures(self, p, boat) -> None:
        lim = self.s.limits
        metrics = [
            (spell(p.under_way_h), 'Sejltid', ''),
            (f'{dk(p.avg_speed_kn)} kn', 'Gns. fart', ''),
            (f'{p.total_nm:.0f} sm', 'Distance', ''),
            (f'{p.worst_wind_kn:.0f} kn', 'Højeste vind',
             self._level(p.worst_wind_kn, lim.max_wind)),
            (f'{dk(p.worst_wave_m)} m', 'Højeste bølger',
             self._level(p.worst_wave_m, lim.max_wave)),
        ]
        if boat.is_motor:
            metrics.append((f'{p.fuel_l:.0f} l', 'Brændstof', ''))
        else:
            metrics.append((f'{p.red_hours} t', 'Frarådet',
                            'val--stop' if p.red_hours else 'val--go'))

        if not self._section('Nøgletal', 'nogletal', 'nogletal'):
            return
        with ui.element('div').classes('metrics metrics--wide mb-4'):
            for value, label, cls in metrics:
                ui.html(f'<div class="metric"><div class="metric-val {cls}">{esc(value)}</div>'
                        f'<div class="metric-lbl">{esc(label)}</div></div>')

        ui.html(f'<div class="hourbar hourbar--tall">{self._hourbar(p)}</div>')
        with ui.row().classes('gap-3 mt-1.5 mb-4'):
            for status in (GO, WARN, STOP):
                ui.html(f'<span class="text-[11px] text-[var(--txt-3)] flex items-center gap-1.5">'
                        f'<i class="dot" style="background:{STATUS_COLOR[status]}"></i>'
                        f'{STATUS_LABEL[status]}</span>')

    @staticmethod
    def _level(value: float, limit: float) -> str:
        if value > limit:
            return 'val--stop'
        if value > limit * 0.8:
            return 'val--warn'
        return 'val--go'

    def _plan_stretches(self, p, route, boat) -> None:
        """Turen delt op dér, hvor kursen skifter — ikke dér, hvor man satte et kryds."""
        briefs = narrative.stretch_briefs(route, p, boat)
        if not self._section('Stræk for stræk', 'straek', 'straek',
                             standard=False, hint=f'{len(briefs)} stræk'):
            return
        ui.label('Ruten er delt op efter kursskift, så hvert stykke gælder præcis '
                 'dér, hvor du styrer den kurs.') \
            .classes('text-[11.5px] text-[var(--txt-3)] mb-2 block leading-snug')
        with ui.element('div').classes('plan-legs mb-4'):
            for brief in briefs:
                self._stretch_card(brief)

    @staticmethod
    def _stretch_card(brief) -> None:
        with ui.element('div').classes('card px-4 py-3.5'):
            with ui.element('div').classes('flex items-center gap-2 mb-1'):
                ui.html(f'<i class="dot" style="background:'
                        f'{STATUS_COLOR[brief.status]}"></i>')
                ui.label(brief.headline).classes(
                    'text-[13.5px] font-semibold flex-1 truncate')
                ui.html(f'<span class="chip tnum">{esc(brief.heading)}</span>')
            ui.label(f'{brief.starts} → {brief.ends}') \
                .classes('text-[11.5px] text-[var(--txt-3)] mb-1.5 block')
            ui.label(brief.sentence).classes(
                'text-[13px] leading-relaxed text-[var(--txt-2)] block')

    def _print_plan(self) -> None:
        """Åbn planen i et nyt vindue, hvor browserens udskrift kan tage over."""
        text = self._plan_text()
        if not text:
            return
        ui.run_javascript(f"""
            const w = window.open('', '_blank');
            w.document.write(
              '<html><head><title>Sejlplan</title><style>'
              + 'body{{font:13px/1.6 ui-monospace,Menlo,Consolas,monospace;'
              + 'padding:32px;max-width:80ch;margin:auto;color:#111}}'
              + 'pre{{white-space:pre-wrap;word-wrap:break-word}}'
              + '</style></head><body><pre>' + {json.dumps(text)} + '</pre></body></html>');
            w.document.close();
            w.focus();
            setTimeout(() => w.print(), 350);
        """)

    def _copy_plan(self) -> None:
        text = self._plan_text()
        if not text:
            return
        ui.clipboard.write(text)
        ui.notify('Hele sejlplanen er kopieret', type='positive', position='bottom')

    def _plan_text(self) -> str:
        p = self.s.plan
        if not p:
            return ''
        return narrative.as_text(self.s.boat, self.s.route, p, self.s.limits)

    def _weather_tab(self) -> None:
        p = self.s.plan
        if not p:
            return

        if not self._section('Time for time', 'timer', 'time-for-time',
                             standard=False,
                             hint=f'{len(p.segments)} timer'):
            return
        if not self.s.has_waves:
            ui.html('<div class="chip chip--warn mb-2">Ingen bølgeprognose for dette '
                    'farvand — vurder søgangen ud fra vind og stræk.</div>')

        motor = self.s.boat.is_motor
        # Strømmen får kun en søjle, når der er noget at vise. På en tur i
        # Smålandsfarvandet står den på nul hele vejen, og en søjle med bare
        # nuller i stjæler plads fra dem, der betyder noget.
        strom = any(abs(x.cur_along_kn) >= 0.2 for x in p.segments)
        rows = []
        current_day = None
        for s in p.segments:
            d = s.time.date()
            if d != current_day:
                current_day = d
                rows.append(f'<tr class="wx-day"><td colspan="{8 if strom else 7}">'
                            f'{esc(day(s.time, False))}</td></tr>')
            # Sidste kolonne er det, der gør tabellen brugbar ombord: ikke bare
            # hvor hårdt det blæser, men hvordan båden ligger i det.
            mode = s.sea if motor else ('motor' if s.motoring else point_of_sail(s.twa))
            rows.append(
                f'<tr>'
                f'<td class="num tnum">{clock(s.time)}</td>'
                f'<td><i class="dot" style="background:{STATUS_COLOR[s.status]}"></i></td>'
                f'<td class="num tnum">{s.wind_kn:.0f}</td>'
                f'<td class="tnum">{esc(compass(s.wind_dir))}</td>'
                f'<td class="tnum">{dk(s.wave_m)}</td>'
                + (f'<td class="num tnum" style="color:{_cur_tone(s)}">'
                   f'{dk(s.cur_along_kn, sign=True)}</td>' if strom else '')
                + f'<td class="num tnum">{dk(s.speed_kn)}</td>'
                f'<td style="color:var(--txt-3)">{esc(mode)}</td>'
                f'</tr>')

        ui.html(
            '<div class="card overflow-hidden"><table class="wx-table">'
            '<thead><tr><th>Tid</th><th></th><th>Vind</th><th>Fra</th>'
            f'<th>Bølger</th>{"<th>Strøm</th>" if strom else ""}'
            f'<th>Fart</th><th>{"Søen" if motor else "Sejlføring"}</th>'
            f'</tr></thead><tbody>{"".join(rows)}</tbody></table></div>')

        peak = max(p.segments, key=lambda s: s.wind_kn)
        ui.label(f'Kraftigst omkring {day_time(peak.time)}: {peak.wind_kn:.0f} kn '
                 f'({beaufort(peak.wind_kn)}) fra {compass(peak.wind_dir)}, '
                 f'kast op til {peak.gust_kn:.0f} kn.') \
            .classes('text-[11.5px] text-[var(--txt-3)] leading-snug mt-2 block')

        if strom:
            # Sig hvad tallet er, og hvad det ikke er. Modellen er global og
            # opløser ikke de danske bælter helt — i Storebælt og Grønsund kan
            # der løbe mere, end den viser, og det skal skipperen vide.
            med = sum(x.cur_along_kn for x in p.segments) / len(p.segments)
            ui.label(
                f'Farten er over grunden — strømmen er regnet med, og står i '
                f'søjlen Strøm: {dk(abs(med))} knob '
                f'{"med" if med >= 0 else "imod"} i snit. Tallene kommer fra en '
                f'global havmodel, der ikke opløser de danske bælter helt. I '
                f'Storebælt og Grønsund kan der løbe mere, end den viser.') \
                .classes('text-[11.5px] text-[var(--txt-3)] leading-snug mt-1 block')

    def _ai_tab(self) -> None:
        # Er vurderingen ikke slået til, findes afsnittet ikke. En bruger kan
        # ikke sætte en nøgle på vores server, og en besked om .env-filer i et
        # dokument, man har betalt for, er vores problem — ikke hans.
        if not settings.ai_available:
            return

        if not self._section('Skippervurdering', 'skipper', 'skipper',
                             standard=bool(self.s.ai_text)):
            return

        if not self.s.ai_text:
            with ui.element('div').classes('empty pb-4'):
                ui.icon('auto_awesome').classes('text-[38px] text-[var(--accent)] opacity-70 mb-2')
                ui.label('Få en skippervurdering').classes('empty-title')
                ui.label('En erfaren sejlkonsulent gennemgår ruten ben for ben og '
                         'anbefaler, hvornår du bør kaste los.').classes('empty-sub')

        self.ai_output()

        label = 'Lav analysen om' if self.s.ai_text else 'Analysér ruten'
        ui.button(label, icon='auto_awesome', on_click=self.run_ai) \
            .props('unelevated no-caps size=lg') \
            .props('color=secondary').classes('w-full mt-3 font-bold')

    @ui.refreshable_method
    def ai_output(self) -> None:
        if self.s.ai_text:
            ui.markdown(self.s.ai_text).classes('ai-text')

    # ════════════════════════════════════════════════════════════════
    # Handlinger
    # ════════════════════════════════════════════════════════════════
    def refresh(self, fit: bool = False) -> None:
        """Tegn hele fladen om, så intet står tilbage med gamle tal."""
        self.stepbar.refresh()
        self.panel.refresh()
        self.action_bar.refresh()
        self.plan_view.refresh()
        self.header_summary.refresh()
        self.map_hint.refresh()
        self._redraw_map(fit=fit)
        # Retningen gælder ét skift. Ellers ville panelet glide hver gang ruten
        # blev regnet om i baggrunden.
        self._nav = 'none'

    def _refresh_panel(self) -> None:
        self.panel.refresh()
        self.action_bar.refresh()
        self.plan_view.refresh()

    def _redraw_map(self, fit: bool = False) -> None:
        if not self.map:
            return
        route = self.s.route
        self.map.draw(route, self.s.plan if self.s.step >= 2 else None)
        if fit:
            self.map.fit(route)

    # ── Ruten gennem vandet ─────────────────────────────────────────
    def _schedule_route(self, fit: bool = False) -> None:
        """Læg havvejen i baggrunden. Fladen venter ikke på den."""
        if self._route_task:
            self._route_task.cancel()
            self._route_task = None
        if len(self.s.waypoints) < 2 or self.s.route_ready:
            self.s.routing = False
            return
        self.s.routing = True
        self.map_hint.refresh()
        self._route_task = asyncio.create_task(self._compute_route(fit))


    async def _compute_route(self, fit: bool) -> None:
        key = signature(self.s.waypoints)
        points = [(w.lat, w.lon) for w in self.s.waypoints]
        try:
            legs = await asyncio.to_thread(searoute.plan_route, points)
        except asyncio.CancelledError:
            raise
        except Exception:      # noqa: BLE001 – ruten må aldrig kunne vælte siden
            self.s.routing = False
            with self.client:
                self.map_hint.refresh()
            return

        if not self.s.set_tracks(key, legs):
            return             # ruten er ændret imens; et nyt kald er på vej

        with self.client:
            self.waypoint_list.refresh()
            self.action_bar.refresh()
            self.header_summary.refresh()
            self.map_hint.refresh()
            self._redraw_map(fit=fit)

    def _plan_lost(self, had_plan: bool) -> None:
        """En ændret rute kasserer de beregnede afgange. Det skal man vide.

        Før skete det lydløst: man flyttede et punkt og stod pludselig på trin 1
        igen, uden at forstå hvor sejlplanen blev af.
        """
        if had_plan:
            ui.notify('Ruten er ændret — find afgangstiderne igen',
                      type='warning', position='bottom')

    # ── Waypoints ───────────────────────────────────────────────────
    def _point_on_map(self, lat: float, lon: float) -> geocode.Place | None:
        """Hvad brugeren ramte. None hvis det er land, man ikke kan sejle på.

        Man sigter sjældent efter et punkt i det åbne vand. Rammer man en havn,
        er det havnen man mener. Rammer man kysten, er det som regel vandet lige
        ved siden af — og ellers er det en fejl, der er værd at sige fra om, i
        stedet for at lægge en rute til midten af Sverige.
        """
        if not landmask.is_water(lat, lon):
            near = harbours.nearest(lat, lon, 1)
            if near and haversine(lat, lon, near[0].lat, near[0].lon) < geocode.HIT_NM:
                return geocode.from_harbour(near[0])
            water = landmask.nearest_water(lat, lon, max_nm=1.5)
            if water == (lat, lon):
                ui.notify('Der er land her. Vælg et sted i vandet, eller søg '
                          'efter en havn.', type='warning', position='bottom')
                return None
            lat, lon = water
        return geocode.at_point(lat, lon)

    def _map_clicked(self, lat: float, lon: float) -> None:
        place = self._point_on_map(lat, lon)
        if place:
            self._add_place(place)

    def _harbour_clicked(self, lat: float, lon: float, name: str) -> None:
        found = [h for h in harbours.nearest(lat, lon, 3) if h.name == name]
        place = geocode.from_harbour(found[0]) if found else \
            geocode.Place(name, 'Lystbådehavn', lat, lon, geocode.HAVN)
        self._add_place(place)

    def _marker_dragged(self, index: int, lat: float, lon: float) -> None:
        """Markøren er trukket et nyt sted hen — så hedder punktet også noget nyt.

        Trak man slutpunktet fra Præstø til Skanör, flyttede ruten sig, men
        navnet blev stående. Resten af planen — overskriften, dagene, GPX-filen,
        briefingen til Claude — talte så om Præstø, mens man sejlede til Sverige.
        Navnet skal følge med positionen.
        """
        if not (0 <= index < len(self.s.waypoints)):
            return
        place = self._point_on_map(lat, lon)
        if place is None:
            self.refresh()      # tegn markøren tilbage hvor den lå
            return

        had_plan = bool(self.s.windows)
        wp = self.s.waypoints[index]
        wp.lat, wp.lon = place.lat, place.lon
        wp.name, wp.detail = place.name, place.detail
        self.s.invalidate()
        self.s.persist()
        self.refresh()
        self._schedule_route()
        ui.notify(f'Punkt {index + 1} flyttet til {place.name}', position='bottom')
        self._plan_lost(had_plan)

    def _add_place(self, place: geocode.Place) -> None:
        """Læg et punkt ind. Er der tvivl om hvor, så spørg.

        Et nyt punkt hører hjemme dér, hvor det koster mindst ekstra vej — og
        som regel er det åbenlyst. Men lægger man Rødvig ind på en rute, der
        går begge veje forbi den, er der to lige gode svar, og så er det ikke
        vores valg at træffe. Samme regel som ved afgangstiderne.
        """
        wp = Waypoint(place.lat, place.lon, place.name, place.detail)
        options = self._insert_options(wp)

        if len(options) > 1 and options[1][0] < options[0][0] + AMBIGUOUS_NM:
            self._ask_position(wp, options)
            return
        self._put(wp, options[0][1] if options else len(self.s.waypoints))

    def _put(self, wp: Waypoint, index: int) -> None:
        had_plan = bool(self.s.windows)
        self.s.insert(index, wp)
        self._suggestions = []
        if self.search_input:
            self.search_input.value = ''
        self.refresh(fit=True)
        self._schedule_route(fit=True)

        where = ('tilføjet' if index >= len(self.s.waypoints) - 1
                 else f'lagt ind som stop nr. {index + 1}')
        ui.notify(f'{wp.name} {where}', type='positive', position='bottom')
        self._plan_lost(had_plan)

    def _insert_options(self, wp: Waypoint) -> list[tuple[float, int, str]]:
        """Hver plads i ruten, hvad den koster i ekstra sømil, og hvad den hedder."""
        wps = self.s.waypoints
        if len(wps) < 2:
            return [(0.0, len(wps), 'Som nyt punkt')]

        def d(a, b) -> float:
            return haversine(a.lat, a.lon, b.lat, b.lon)

        out = [(d(wps[-1], wp), len(wps), f'Som ny destination, efter {wps[-1].name}'),
               (d(wp, wps[0]), 0, f'Som ny afgang, før {wps[0].name}')]
        for i in range(len(wps) - 1):
            out.append((d(wps[i], wp) + d(wp, wps[i + 1]) - d(wps[i], wps[i + 1]),
                        i + 1, f'Mellem {wps[i].name} og {wps[i + 1].name}'))
        out.sort(key=lambda row: row[0])
        return out

    def _ask_position(self, wp: Waypoint, options: list) -> None:
        """To lige gode pladser. Så skal skipperen pege."""
        with ui.dialog() as ask, ui.card().classes(
                'w-full max-w-[420px] p-0 bg-[var(--sea-1)] rounded-[var(--r)]'):
            with ui.element('div').classes('px-5 pt-5 pb-1'):
                ui.label(f'Hvor skal {wp.name} ligge?')                     .classes('text-[16px] font-bold block')
                ui.label('Der er mere end ét sted, den passer lige godt. '
                         'Vælg selv — du kan altid flytte den bagefter.')                     .classes('text-[12.5px] text-[var(--txt-2)] leading-snug '
                             'mt-1 block')

            with ui.element('div').classes('px-5 pt-3 pb-1'):
                for cost, index, label in options[:4]:
                    row = ui.element('div').classes(
                        'card px-3.5 py-2.5 mb-2 flex items-center gap-3 '
                        'cursor-pointer hover:border-[var(--line-2)]')
                    with row:
                        with ui.element('div').classes('min-w-0 flex-1'):
                            ui.label(label).classes(
                                'text-[13px] font-medium truncate block')
                            ui.label(f'{nm(cost)} sømil ekstra')                                 .classes('text-[11px] text-[var(--txt-3)] '
                                         'tnum block')
                        ui.icon('chevron_right').classes(
                            'text-[18px] text-[var(--txt-3)] shrink-0')
                    row.on('click', lambda _, k=index: (ask.close(),
                                                        self._put(wp, k)))

            with ui.row().classes('w-full items-center px-5 pb-4 no-wrap'):
                ui.element('div').classes('flex-1')
                ui.button('Fortryd', on_click=ask.close)                     .props('flat no-caps').classes('text-[var(--txt-2)]')
        ask.open()

    def _best_position(self, wp: Waypoint) -> int:
        """Hvor i ruten hører punktet hjemme?

        Et nyt punkt lægges dér, hvor det koster mindst ekstra vej. Sætter man
        en havn midt på ruten, bliver den et mellemstop; ligger den ude i den
        ene ende, bliver den en ny endestation. Det er næsten altid det, man
        mener, og man kan altid flytte den bagefter.
        """
        wps = self.s.waypoints
        if len(wps) < 2:
            return len(wps)

        def d(a, b) -> float:
            return haversine(a.lat, a.lon, b.lat, b.lon)

        best_index, best_cost = len(wps), d(wps[-1], wp)
        for i in range(len(wps) - 1):
            cost = d(wps[i], wp) + d(wp, wps[i + 1]) - d(wps[i], wps[i + 1])
            if cost < best_cost - 0.5:
                best_index, best_cost = i + 1, cost
        # Foran ruten hører den til, hvis den ligger nærmere start end alt andet.
        if d(wp, wps[0]) < best_cost - 0.5:
            best_index = 0
        return best_index

    async def _add_named(self, name: str) -> None:
        """En genvej skal foreslå, ikke bestemme.

        "Bornholm" er ikke ét sted — der er havne hele vejen rundt om øen, og
        "København" er en håndfuld. Før tog vi det første, søgningen gav, og
        lagde det ind uden at spørge. Nu ender genvejen samme sted som hvis man
        havde tastet navnet selv: listen over de steder, der findes, og så
        peger brugeren.
        """
        if self.search_input is not None:
            self.search_input.value = name
            return
        # Uden søgefelt (skulle ikke kunne ske) er det bedre at lægge noget ind
        # end ingenting.
        results = await geocode.search(name, limit=1)
        if results:
            self._add_place(results[0])

    def _remove(self, index: int) -> None:
        had_plan = bool(self.s.windows)
        self.s.remove(index)
        self.refresh(fit=True)
        self._schedule_route(fit=True)
        self._plan_lost(had_plan)

    def _move(self, index: int, delta: int) -> None:
        had_plan = bool(self.s.windows)
        self.s.move(index, delta)
        self.refresh()
        self._schedule_route()
        self._plan_lost(had_plan)

    def _reverse_route(self) -> None:
        if len(self.s.waypoints) < 2:
            return
        had_plan = bool(self.s.windows)
        self.s.reverse()
        self.refresh()
        self._schedule_route()
        ui.notify('Ruten er vendt om', position='bottom')
        self._plan_lost(had_plan)

    # ── Planen med om bord ──────────────────────────────────────────
    def _stow_plan(self, boat, route, plan) -> None:
        """Læg planen ned i telefonen, hver gang man ser på den.

        Netop dér er den værd at gemme: brugeren har valgt sin afgang og læser
        den igennem. Går dækningen senere, er det den her, der kommer frem.
        """
        try:
            html = offline.document(boat, route, plan, self.s.limits,
                                    outlook=self._outlook(plan))
            self.client.run_javascript(pwa.save_plan_js(html))
        except Exception:
            # En plan, der ikke kunne gemmes til senere, må ikke forhindre
            # nogen i at læse den nu.
            pass

    # ── Mine ruter ──────────────────────────────────────────────────
    def _save_route(self) -> None:
        myroutes.save_dialog(self.s, lambda: self.refresh())

    def _open_routes(self) -> None:
        myroutes.open_dialog(self.s, self._open_saved, lambda: self.refresh())

    def _open_saved(self, rid: str) -> None:
        """Læg en gemt rute på bordet. Havvejen skal regnes forfra."""
        if not self.s.open_route(rid):
            ui.notify('Ruten kunne ikke åbnes', type='warning', position='bottom')
            return
        self._suggestions = []
        if self.search_input:
            self.search_input.value = ''
        self.refresh(fit=True)
        self._schedule_route(fit=True)
        ui.notify(f'"{self.s.saved_name}" er åbnet', position='bottom')

    def _clear_route(self) -> None:
        """Spørg først. Det her sletter hele arbejdet, og der er ingen fortryd."""
        if not self.s.waypoints:
            return

        with ui.dialog() as ask, ui.card().classes(
                'w-full max-w-[380px] p-0 bg-[var(--sea-1)] rounded-[var(--r)]'):
            with ui.element('div').classes('px-5 pt-5 pb-3'):
                ui.label('Ryd hele ruten?').classes('text-[16px] font-bold block')
                ui.label(f'{len(self.s.waypoints)} punkter og den beregnede plan '
                         f'forsvinder. Det kan ikke fortrydes.') \
                    .classes('text-[13px] text-[var(--txt-2)] leading-snug mt-1 block')
            with ui.row().classes('w-full items-center gap-2 px-5 pb-4 no-wrap'):
                ui.element('div').classes('flex-1')
                ui.button('Behold', on_click=ask.close) \
                    .props('flat no-caps').classes('text-[var(--txt-2)]')
                ui.button('Ryd', on_click=lambda: self._do_clear(ask)) \
                    .props('unelevated no-caps') \
                    .classes('bg-[var(--stop)] text-white font-bold px-4')
        ask.open()

    def _do_clear(self, dialog) -> None:
        dialog.close()
        self.s.clear()
        self._suggestions = []
        self.refresh(fit=True)
        ui.notify('Ruten er ryddet', position='bottom')

    # ── Søgning ─────────────────────────────────────────────────────
    def _search_changed(self, e) -> None:
        """Søg mens der tastes, men vent til fingrene falder til ro."""
        query = (e.value or '').strip()
        if self._search_task:
            self._search_task.cancel()
        if len(query) < 2:
            self._suggestions = []
            self._no_hits = ''
            self._searching = False
            self.suggestion_list.refresh()
            return
        self._search_task = asyncio.create_task(self._search_later(query))

    async def _search_later(self, query: str) -> None:
        try:
            await asyncio.sleep(0.28)
            self._searching = True
            self.suggestion_list.refresh()
            self._suggestions = await geocode.search(query)
            self._no_hits = '' if self._suggestions else query
        except asyncio.CancelledError:
            return
        finally:
            self._searching = False
        self.suggestion_list.refresh()

    def _accept_first_suggestion(self) -> None:
        if self._suggestions:
            self._add_place(self._suggestions[0])

    # ── Beregning ───────────────────────────────────────────────────
    async def run_analysis(self) -> None:
        if not self.s.can_analyse:
            ui.notify('Tilføj mindst to punkter først', type='warning', position='bottom')
            return

        self._busy = 'Lægger ruten udenom land…'
        self._refresh_panel()
        try:
            if not self.s.route_ready:
                key = signature(self.s.waypoints)
                points = [(w.lat, w.lon) for w in self.s.waypoints]
                legs = await asyncio.to_thread(searoute.plan_route, points)
                self.s.set_tracks(key, legs)
            route = self.s.route

            self._busy = 'Henter vejrudsigt for hvert ben…'
            self._refresh_panel()
            self.s.weather = await weather.fetch_weather(route)
            self.s.has_waves = weather.has_wave_data(self.s.weather)

            self._busy = 'Finder havne undervejs og gennemsejler alle afgangstider…'
            self._refresh_panel()
            await asyncio.sleep(0)  # lad panelet nå at tegne sig

            stops = await asyncio.to_thread(harbours.stopovers, route)
            self.s.windows = await asyncio.to_thread(
                find_windows, self.s.boat, route, self.s.weather, self.s.limits, stops)
        except weather.WeatherError as exc:
            self._busy = ''
            self._refresh_panel()
            ui.notify(str(exc), type='negative', position='bottom')
            return
        finally:
            self._busy = ''

        self.s.selected = 0
        self.s.ai_text = ''

        if not self.s.windows:
            self.s.step = 1
            self._nav = 'back'
            self.refresh()
            ui.notify('Ingen afgange passer til dine grænser. Prøv et bredere '
                      'datointerval, et længere sejldøgn eller en højere vindgrænse.',
                      type='warning', position='bottom', timeout=7000)
            return

        self.s.step = 2
        self._nav = 'fwd'
        self.refresh()

        best = self.s.windows[0]
        if best.late_arrival:
            ui.notify(f'Turen kan ikke nås inden kl. {self.s.limits.day_end:02d}:00. '
                      f'Se forslagene — de fleste kræver en overnatning undervejs.',
                      type='warning', position='bottom', timeout=8000)
        elif best.stops:
            ui.notify(f'{len(self.s.windows)} afgange fundet. Turen kræver '
                      f'{best.nights} overnatning{"er" if best.nights > 1 else ""} '
                      f'undervejs — første stop i {best.stops[0].name}.',
                      type='positive', position='bottom', timeout=7000)
        else:
            ui.notify(f'{len(self.s.windows)} afgangstider fundet',
                      type='positive', position='bottom')

    def _select_window(self, index: int) -> None:
        self.s.selected = index
        self.s.ai_text = ''
        self._refresh_panel()
        self._redraw_map()

    # ── AI ──────────────────────────────────────────────────────────
    async def run_ai(self) -> None:
        p = self.s.plan
        if not p:
            return

        self.s.ai_text = ''
        self.ai_output.refresh()
        spinner = ui.notification('Claude læser vejrudsigten…', spinner=True,
                                  position='bottom', timeout=None)
        buffer: list[str] = []
        last_flush = 0.0
        started = False

        try:
            async for chunk in ai.stream_analysis(
                    self.s.boat, self.s.route, p, self.s.windows,
                    self.s.limits, self.s.has_waves):
                buffer.append(chunk)
                if not started:
                    started = True
                    spinner.dismiss()
                # Tegn ikke om for hvert lille stykke tekst – ca. 8 gange
                # i sekundet er rigeligt til at det ser levende ud.
                now = time.monotonic()
                if now - last_flush > 0.12:
                    last_flush = now
                    self.s.ai_text = ''.join(buffer)
                    self.ai_output.refresh()
        except ai.AIUnavailable as exc:
            spinner.dismiss()
            ui.notify(str(exc), type='negative', position='bottom', timeout=6000)
            return
        finally:
            if not started:
                spinner.dismiss()

        self.s.ai_text = ''.join(buffer).strip()
        self.ai_output.refresh()

    # ── Deling ──────────────────────────────────────────────────────
    async def _copy_link(self) -> None:
        if not self.s.waypoints:
            ui.notify('Der er ingen rute at dele endnu', position='bottom')
            return
        token = share.encode_route(self.s.waypoints, self.s.boat_id)
        origin = await ui.run_javascript('window.location.origin', timeout=3)
        ui.clipboard.write(f'{origin}/?rute={token}')
        ui.notify('Delelink kopieret — send det til gasterne',
                  type='positive', position='bottom')

    def _download_gpx(self) -> None:
        if not self.s.waypoints:
            ui.notify('Der er ingen rute at eksportere endnu', position='bottom')
            return
        wps = self.s.waypoints
        name = f'{wps[0].name} → {wps[-1].name}' if len(wps) > 1 else wps[0].name
        ui.download.content(share.to_gpx(self.s.route, name), share.filename(wps))

    # ── Indstillinger ───────────────────────────────────────────────
    def _toggle_theme(self) -> None:
        self.dark.value = not self.dark.value
        # Quasars egne farver skal med over — guldet er lysere i mørk tilstand.
        theme.palette(bool(self.dark.value))
        if self.map:
            self.map.set_dark(bool(self.dark.value))

    def _open_settings(self) -> None:
        from .settings import settings_dialog
        settings_dialog(self)
