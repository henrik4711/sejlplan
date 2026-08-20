"""Brugerfladen: trinnene Rute → Afgang → Sejlplan.

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
from datetime import date, timedelta

from nicegui import ui

from .. import (ai, geocode, harbours, landmask, narrative, searoute, share,
                weather)
from ..boats import MOTORBOATS, SAILBOATS
from ..config import settings
from ..dates import clock, day, day_time, duration, full, month
from ..sailing import (GO, STATUS_COLOR, STATUS_LABEL, STOP, WARN, Waypoint,
                       beaufort, compass, find_windows, haversine,
                       point_of_sail)
from ..state import MAX_FORECAST_DAYS, Session, signature
from .mapview import RouteMap

STEPS = [(1, 'Rute'), (2, 'Afgang'), (3, 'Sejlplan')]

QUICK_START = ['København', 'Helsingør', 'Aarhus', 'Svendborg',
               'Bornholm', 'Skagen', 'Samsø', 'Marstal']


def esc(text: str) -> str:
    return html.escape(str(text), quote=True)


def dk(value: float, decimals: int = 1) -> str:
    """Tal med komma som decimaltegn. Det er sådan de skrives på dansk."""
    return f'{value:.{decimals}f}'.replace('.', ',')


def nm(value: float) -> str:
    return dk(value, 1)


class Planner:
    """Hele planlæggeren for én bruger."""

    def __init__(self) -> None:
        self.s = Session.restore()
        self.map: RouteMap | None = None
        self._search_task: asyncio.Task | None = None
        self._route_task: asyncio.Task | None = None
        self._suggestions: list[geocode.Place] = []
        self._searching = False
        self._busy = ''
        self._settings_open = False
        self.search_input: ui.input | None = None
        # Baggrundsopgaver skal opdatere netop den her browser. NiceGUI's
        # underforståede klient er ikke sat, når en opgave vågner op igen, så
        # vi holder fast i vores egen og går ind i den, før vi rører fladen.
        self.client = ui.context.client

    # ════════════════════════════════════════════════════════════════
    # Opbygning
    # ════════════════════════════════════════════════════════════════
    def build(self) -> None:
        # Hele appen bor i en skal, der er spændt ud over skærmen. Det er dét,
        # der gør at panelet kan rulle uafhængigt af hvor langt indholdet er.
        with ui.element('div').classes('app-shell'):
            self._header()

            with ui.element('div').classes(
                    'flex flex-col-reverse md:flex-row w-full flex-1 min-h-0 '
                    'gap-0 overflow-hidden'):

                # ── Arbejdspanel ──
                # `md:h-full` er ikke pynt. Uden en fast højde bliver en flex-
                # række så høj som sit højeste barn, og så vokser panelet med
                # sit indhold i stedet for at rulle: ti afgangskort blev til
                # 1679 px inde i en række på 722, og resten blev klippet væk.
                with ui.element('aside').classes(
                        'w-full md:w-[430px] md:h-full flex flex-col min-h-0 '
                        'basis-[58%] md:basis-auto md:flex-none '
                        'border-t md:border-t-0 md:border-r '
                        'border-[var(--line)] bg-[var(--sea-2)] z-10'):
                    with ui.element('div').classes('px-4 pt-3 pb-2 shrink-0'):
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
                        'relative min-h-0 basis-[42%] shrink-0 md:h-full '
                        'md:basis-auto md:flex-1 md:shrink'):
                    self.map = RouteMap(on_click=self._map_clicked,
                                        on_drag=self._marker_dragged,
                                        on_harbour=self._harbour_clicked,
                                        dark=bool(self.dark.value))
                    self._map_controls()
                    self._map_overlay()
                    self.plan_view()

        self._redraw_map(fit=True)
        self._schedule_route()

    def _header(self) -> None:
        with ui.element('header').classes('app-header text-[var(--txt-1)]'):

            ui.icon('sailing').classes('text-[22px] text-[var(--accent)]')
            ui.label('Sejlplan').classes('text-[17px] font-bold tracking-tight')

            self.header_summary()

            ui.element('div').classes('flex-1')

            self.boat_button()

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

    @ui.refreshable_method
    def boat_button(self) -> None:
        boat = self.s.boat
        ui.button(boat.name, icon=boat.icon, on_click=self._open_settings) \
            .props('flat dense no-caps') \
            .classes('text-[var(--txt-2)] text-[13px] max-sm:hidden') \
            .tooltip('Skift båd og grænser')

    def share_button(self) -> None:
        with ui.button(icon='ios_share').props('flat round dense') \
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
                'absolute top-3 right-3 z-[500] flex flex-col items-end gap-2'):

            with ui.element('div').classes('card flex overflow-hidden p-0.5 gap-0.5'):
                self.style_btns = {}
                for key, label, tip in (
                        ('chart', 'Søkort', 'Havkort med dybdeforhold'),
                        ('street', 'Landkort', 'Almindeligt kort med veje og byer')):
                    btn = ui.button(label, on_click=lambda _, k=key: self._set_map_style(k)) \
                        .props('flat dense no-caps size=sm') \
                        .classes('!px-2.5 !py-1 text-[11.5px] rounded-[8px]') \
                        .tooltip(tip)
                    self.style_btns[key] = btn
                self._paint_style_buttons()

            self.harbour_btn = ui.button(icon='sailing', on_click=self._toggle_harbours) \
                .props('flat dense square').classes('map-btn w-9 h-9') \
                .tooltip('Vis alle lystbådehavne — klik på en for at lægge den i ruten')
            self.seamark_btn = ui.button(icon='anchor', on_click=self._toggle_seamarks) \
                .props('flat dense square').classes('map-btn w-9 h-9') \
                .tooltip('Vis bøjer, fyr og sejlløb fra OpenSeaMap')
            ui.button(icon='center_focus_strong',
                      on_click=lambda: self.map and self.map.fit(self.s.route)) \
                .props('flat dense square').classes('map-btn w-9 h-9') \
                .tooltip('Zoom til hele ruten')

    def _paint_style_buttons(self) -> None:
        active = self.map.style if self.map else 'chart'
        for key, btn in self.style_btns.items():
            on = key == active
            btn.classes(add='bg-[var(--accent-soft)] text-[var(--accent)] font-bold' if on
                        else 'text-[var(--txt-3)]',
                        remove='text-[var(--txt-3)]' if on
                        else 'bg-[var(--accent-soft)] text-[var(--accent)] font-bold')

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
        ui.notify('Havnene vises fra zoomniveau 8 — klik på en prik for at '
                  'lægge havnen i ruten' if on else 'Havnene er skjult',
                  position='bottom')

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
                '<div class="card px-3.5 py-2 text-[12.5px] text-[var(--txt-2)] '
                'flex items-center gap-2 shadow-lg">'
                '<span class="spinner-dot"></span>Lægger ruten udenom land…</div>')
            return
        if len(self.s.waypoints) >= 2:
            return
        text = ('Klik på kortet, eller søg efter en havn, for at sætte afgangshavnen'
                if not self.s.waypoints else 'Klik igen for at sætte destinationen')
        ui.html(
            f'<div class="card px-3.5 py-2 text-[12.5px] text-[var(--txt-2)] '
            f'flex items-center gap-2 shadow-lg">'
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

    def _step_unlocked(self, num: int) -> bool:
        if num == 1:
            return True
        if num == 2:
            return self.s.can_analyse
        return bool(self.s.windows)

    def _go_to_step(self, num: int) -> None:
        if not self._step_unlocked(num):
            return
        self.s.step = num
        self.refresh()

    # ════════════════════════════════════════════════════════════════
    # Panelet
    # ════════════════════════════════════════════════════════════════
    @ui.refreshable_method
    def panel(self) -> None:
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
                       'input-class="text-[14px]"') \
                .classes('w-full') \
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

        if not self._suggestions:
            return

        with ui.element('div').classes('card overflow-hidden mb-3'):
            for i, place in enumerate(self._suggestions):
                if i:
                    ui.html('<div class="hairline"></div>')
                row = ui.element('div').classes(
                    'flex items-center gap-3 px-3 py-2.5 cursor-pointer '
                    'hover:bg-[var(--sea-3)] transition-colors')
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

        with ui.element('div').classes('flex items-baseline gap-2 mt-3 mb-1.5'):
            ui.html('<span class="section-label">Ruten</span>')
            ui.element('div').classes('flex-1')
            if self.s.routing:
                ui.html('<span class="text-[11px] text-[var(--txt-3)]">'
                        'beregner havvejen…</span>')

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

        with ui.element('div').classes('wp group'):
            ui.html(f'<div class="wp-pin wp-pin--{kind}">{i + 1}</div>')

            info = ui.element('div').classes('min-w-0 flex-1 cursor-pointer')
            with info:
                ui.label(wp.name).classes('wp-name truncate')
                ui.label(f'{role} · {wp.lat:.3f}°N {wp.lon:.3f}°Ø').classes('wp-meta truncate')
            info.on('click', lambda _, w=wp: self.map and self.map.focus(w.lat, w.lon))
            info.tooltip('Vis på kortet')

            with ui.element('div').classes('flex items-center shrink-0 '
                                           'opacity-40 group-hover:opacity-100 transition-opacity'):
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
        ui.html(f'<div class="text-[12px] text-[var(--txt-3)] px-1 pt-1">'
                f'{n_legs} ben · {nm(route.total_nm)} sømil ad havvejen</div>')
        if self.s.route_ready and not route.ok:
            ui.html('<div class="chip chip--warn mt-2">Et ben kunne ikke lægges '
                    'sikkert udenom land — kontrollér det selv på søkortet.</div>')

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
                    .classes('w-full bg-[var(--accent)] text-[var(--sea-1)] font-bold')
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
        lim = self.s.limits
        boat = self.s.boat

        with self._bar():
            # Sammenklappet: én linje der viser hvad der er valgt.
            header = ui.element('div').classes(
                'flex items-center gap-2.5 cursor-pointer select-none -mx-1 px-1 py-0.5 '
                'rounded-[8px] hover:bg-[var(--sea-3)] transition-colors')
            with header:
                ui.icon(boat.icon).classes('text-[18px] text-[var(--accent)] shrink-0')
                with ui.element('div').classes('min-w-0 flex-1 leading-tight'):
                    ui.label(boat.name).classes('text-[13px] font-semibold truncate block')
                    ui.label(f'{self._short_date(lim.date_from)}–{self._short_date(lim.date_to)}'
                             f' · sejldøgn {lim.day_start:02d}–{lim.day_end:02d}'
                             f' · maks {lim.max_wind:.0f} kn') \
                        .classes('text-[11.5px] text-[var(--txt-3)] truncate block')
                ui.icon('expand_less' if self._settings_open else 'expand_more') \
                    .classes('text-[20px] text-[var(--txt-3)] shrink-0')
            header.on('click', self._toggle_settings)

            if self._settings_open:
                with ui.element('div').classes('scroll-y max-h-[42dvh] mt-3'):
                    self.trip_settings()

            with ui.element('div').classes('flex items-center gap-2.5 mt-3'):
                ui.button('Find bedste afgangstider', icon='travel_explore',
                          on_click=self.run_analysis) \
                    .props('unelevated no-caps size=lg') \
                    .classes('flex-1 bg-[var(--accent)] text-[var(--sea-1)] font-bold')
                ui.html(f'<div class="text-right shrink-0 leading-tight">'
                        f'<div class="text-[15px] font-bold tnum">'
                        f'{self.s.total_nm:.0f}</div>'
                        f'<div class="text-[10.5px] text-[var(--txt-3)]">sømil</div></div>')

    @staticmethod
    def _short_date(iso: str) -> str:
        try:
            d = date.fromisoformat(iso)
            return f'{d.day}. {month(d, short=True)}'
        except (TypeError, ValueError):
            return iso

    def _toggle_settings(self) -> None:
        self._settings_open = not self._settings_open
        self.action_bar.refresh()

    @ui.refreshable_method
    def trip_settings(self) -> None:
        """Båd, datoer og sejldøgn — fremme i panelet, hvor de bliver brugt."""
        lim = self.s.limits
        with ui.element('div').classes('flex flex-col gap-3.5'):

            # ── Båd ──
            with ui.element('div'):
                self._field_label('Båd', 'directions_boat')
                options = {}
                for group, boats in (('Sejlbåde', SAILBOATS), ('Motorbåde', MOTORBOATS)):
                    for b in boats:
                        options[b.id] = f'{group[:-1]} · {b.name} · {b.summary}'
                ui.select(options, value=self.s.boat_id,
                          on_change=lambda e: self._change_boat(e.value)) \
                    .props('outlined dense options-dense behavior=menu') \
                    .classes('w-full text-[13px]')

            # ── Datoer ──
            with ui.element('div'):
                self._field_label('Hvornår kan du afgå', 'event')
                with ui.element('div').classes('grid grid-cols-2 gap-2'):
                    self._date_picker('Fra', lim.date_from, self._set_date_from)
                    self._date_picker('Til', lim.date_to, self._set_date_to)
                ui.label(f'Vejrudsigten rækker {MAX_FORECAST_DAYS} dage frem, '
                         f'til og med {day(self._horizon(), short=False)}.') \
                    .classes('text-[11px] text-[var(--txt-3)] mt-1.5 block')

            # ── Sejldøgn ──
            with ui.element('div'):
                self._field_label('Sejldøgn', 'schedule')
                with ui.element('div').classes('grid grid-cols-2 gap-2'):
                    self._hour_select('Tidligst ud', lim.day_start,
                                      lambda v: self._set_hour('day_start', v))
                    self._hour_select('Senest i havn', lim.day_end,
                                      lambda v: self._set_hour('day_end', v))
                ui.label(f'Du skal ligge fortøjet kl. {lim.day_end:02d}:00. Rækker '
                         f'turen ikke, finder planlæggeren en havn undervejs at '
                         f'overnatte i.') \
                    .classes('text-[11px] text-[var(--txt-3)] mt-1.5 block leading-snug')

            self._switch_row('Sejl også om natten', lim.night_ok,
                             'Så lægges ingen overnatninger ind — turen sejles i ét stræk.',
                             lambda v: self._set_flag('night_ok', v))

            # ── Grænser ──
            ui.html('<div class="hairline"></div>')
            with ui.element('div').classes('flex items-center justify-between gap-2'):
                with ui.element('div').classes('min-w-0'):
                    ui.label('Komfortgrænser').classes('text-[12.5px] font-medium')
                    ui.label(f'Op til {lim.max_wind:.0f} kn vind og '
                             f'{lim.max_wave:.1f} m bølger'.replace('.', ',')) \
                        .classes('text-[11.5px] text-[var(--txt-3)]')
                ui.button('Ret', icon='tune', on_click=self._open_settings) \
                    .props('flat dense no-caps size=sm') \
                    .classes('text-[var(--accent)] shrink-0')

    @staticmethod
    def _field_label(text: str, icon: str) -> None:
        with ui.element('div').classes('flex items-center gap-1.5 mb-1.5'):
            ui.icon(icon).classes('text-[15px] text-[var(--txt-3)]')
            ui.label(text).classes('text-[12.5px] font-medium')

    @staticmethod
    def _switch_row(label: str, value: bool, hint: str, on_set) -> None:
        with ui.row().classes('items-center no-wrap gap-3 w-full'):
            with ui.element('div').classes('flex-1 min-w-0'):
                ui.label(label).classes('text-[12.5px] font-medium')
                ui.label(hint).classes('text-[11px] text-[var(--txt-3)] leading-snug')
            ui.switch(value=value, on_change=lambda e: on_set(bool(e.value))) \
                .props('dense color=amber')

    @staticmethod
    def _horizon() -> date:
        return date.today() + timedelta(days=MAX_FORECAST_DAYS - 1)

    def _date_picker(self, label: str, value: str, on_set) -> None:
        """Datofelt med kalender. Læsevenlig tekst udadtil, ISO indeni."""
        with ui.element('div'):
            ui.label(label).classes('text-[11px] text-[var(--txt-3)] mb-1 block')
            field = ui.input(value=self._pretty_date(value)) \
                .props('outlined dense readonly input-class="text-[13px] cursor-pointer"') \
                .classes('w-full')
            lo, hi = date.today(), self._horizon()
            with field:
                with ui.menu().props('no-parent-event') as menu:
                    picker = ui.date(value=value).props(
                        'minimal today-btn '
                        f':options="d => d >= \'{lo.isoformat().replace("-", "/")}\' '
                        f'&& d <= \'{hi.isoformat().replace("-", "/")}\'"')

                    def handle(e) -> None:
                        if not e.value:
                            return
                        menu.close()
                        on_set(e.value)

                    picker.on_value_change(handle)
                with field.add_slot('append'):
                    ui.icon('event').classes('cursor-pointer text-[17px] text-[var(--txt-3)]')
            field.on('click', menu.open)

    @staticmethod
    def _pretty_date(iso: str) -> str:
        try:
            return day(date.fromisoformat(iso), short=False)
        except (TypeError, ValueError):
            return iso

    @staticmethod
    def _hour_select(label: str, value: int, on_set) -> None:
        with ui.element('div'):
            ui.label(label).classes('text-[11px] text-[var(--txt-3)] mb-1 block')
            ui.select({h: f'{h:02d}:00' for h in range(24)}, value=value,
                      on_change=lambda e: on_set(int(e.value))) \
                .props('outlined dense options-dense behavior=menu') \
                .classes('w-full text-[13px]')

    # ── Ændringer af planen ─────────────────────────────────────────
    def _change_boat(self, boat_id: str) -> None:
        if boat_id == self.s.boat_id:
            return
        self.s.set_boat(boat_id)
        self.boat_button.refresh()
        self.trip_settings.refresh()
        self.action_bar.refresh()
        self.stepbar.refresh()

    def _set_date_from(self, value: str) -> None:
        self.s.limits.date_from = value
        if self.s.limits.date_to < value:
            self.s.limits.date_to = value
        self._after_limit_change()

    def _set_date_to(self, value: str) -> None:
        self.s.limits.date_to = value
        if self.s.limits.date_from > value:
            self.s.limits.date_from = value
        self._after_limit_change()

    def _set_hour(self, field: str, value: int) -> None:
        setattr(self.s.limits, field, value)
        # Et sejldøgn der vender bagvendt giver ingen afgange – ret det stille op.
        if self.s.limits.day_start >= self.s.limits.day_end:
            if field == 'day_start':
                self.s.limits.day_end = min(23, value + 1)
            else:
                self.s.limits.day_start = max(0, value - 1)
        self._after_limit_change()

    def _set_flag(self, field: str, value: bool) -> None:
        setattr(self.s.limits, field, value)
        self._after_limit_change()

    def _after_limit_change(self) -> None:
        self.s.invalidate()
        self.s.persist()
        self.trip_settings.refresh()
        self.action_bar.refresh()
        self.stepbar.refresh()

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
        ui.html(
            f'<div class="text-[12.5px] text-[var(--txt-2)] leading-snug mb-3">'
            f'{len(self.s.windows)} mulige afgange i vinduet. Den bedste er '
            f'<b>{esc(full(best.depart))}</b>.</div>')

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
                ui.html(f'<div class="win-arrive tnum">→ {esc(day_time(w.arrival))} '
                        f'· {esc(duration(w.hours))} med fart i</div>')

            if w.stops:
                names = ' · '.join(f'{s.name} {day_time(s.arrive)}' for s in w.stops)
                ui.html(f'<div class="win-stops">'
                        f'<span class="material-icons" style="font-size:14px">hotel</span>'
                        f'{esc(names)}</div>')

            ui.html(f'<div class="hourbar mt-2.5">{self._hourbar(w)}</div>')

            with ui.element('div').classes('flex gap-1.5 mt-2.5 flex-wrap'):
                ui.html(f'<span class="chip tnum">💨 {w.worst_wind_kn:.0f} kn</span>')
                ui.html(f'<span class="chip tnum">🌊 {dk(w.worst_wave_m)} m</span>')
                ui.html(f'<span class="chip tnum">⌀ {dk(w.avg_speed_kn)} kn</span>')
                if w.stops:
                    ui.html(f'<span class="chip tnum">🛏 {w.nights} nat</span>')
                if w.night_hours:
                    ui.html(f'<span class="chip tnum">🌙 {w.night_hours} t</span>')
                if self.s.boat.is_motor and w.fuel_l:
                    ui.html(f'<span class="chip tnum">⛽ {w.fuel_l:.0f} l</span>')
                elif w.motor_hours:
                    ui.html(f'<span class="chip tnum">⚙ {w.motor_hours} t motor</span>')

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
            ui.label(f'→ {day_time(w.arrival)}').classes(
                'text-[11.5px] text-[var(--txt-3)] tnum flex-1 truncate')
            if w.stops:
                ui.html(f'<span class="chip tnum shrink-0">🛏 {w.nights}</span>')
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

        with ui.element('div').classes('plan-view scroll-y'):
            with ui.element('div').classes('mx-auto max-w-[78ch] px-5 md:px-8 py-6 md:py-8'):

                # ── Hoved ──
                with ui.element('div').classes(
                        'flex items-start gap-4 flex-wrap pb-4 mb-5 '
                        'border-b border-[var(--line)]'):
                    with ui.element('div').classes('min-w-0 flex-1'):
                        ui.label('Sejlplan').classes('section-label')
                        ui.label(names).classes(
                            'text-[26px] md:text-[30px] font-bold leading-tight '
                            'tracking-tight mt-1 block')
                        ui.label(f'{boat.name} · afgang {full(p.depart)} · '
                                 f'ankomst {full(p.arrival)}') \
                            .classes('text-[13.5px] text-[var(--txt-2)] mt-1.5 block')
                    with ui.row().classes('gap-1.5 shrink-0'):
                        ui.button('Udskriv', icon='print', on_click=self._print_plan) \
                            .props('outline dense no-caps').classes('text-[var(--txt-2)]')
                        ui.button('Kopiér', icon='content_copy', on_click=self._copy_plan) \
                            .props('outline dense no-caps').classes('text-[var(--txt-2)]')
                        ui.button(icon='map', on_click=lambda: self._go_to_step(2)) \
                            .props('outline dense round').classes('text-[var(--txt-2)]') \
                            .tooltip('Tilbage til kortet')

                self._plan_overview(p, boat, route)
                self._plan_warnings(p, boat)
                self._plan_days(p)
                self._key_figures(p, boat)
                self._plan_stretches(p, route, boat)
                self._weather_tab()
                self._ai_tab()

    def _plan_overview(self, p, boat, route) -> None:
        ui.label('Overblik').classes('section-label mb-1.5 block')
        with ui.element('div').classes('card px-4 py-3.5 mb-4'):
            for paragraph in narrative.overview(boat, route, p):
                ui.label(paragraph).classes(
                    'text-[13.5px] leading-relaxed text-[var(--txt-2)] mb-2 last:mb-0 block')

    def _plan_warnings(self, p, boat) -> None:
        items = narrative.warnings(p, self.s.limits, boat)
        # Ét punkt og intet at komme efter: så er det en god nyhed, ikke en advarsel.
        good = (len(items) == 1 and p.verdict == GO and not p.stops
                and not p.night_hours and not p.late_arrival)
        ui.label('Vær opmærksom på').classes('section-label mb-1.5 block')
        with ui.element('div').classes('card px-4 py-3.5 mb-4 flex flex-col gap-2.5'):
            for text in items:
                with ui.element('div').classes('flex gap-2.5 items-start'):
                    ui.icon('check_circle' if good else 'error_outline') \
                        .classes(f'text-[17px] shrink-0 mt-0.5 '
                                 f'{"text-[var(--go)]" if good else "text-[var(--warn)]"}')
                    ui.label(text).classes(
                        'text-[13px] leading-relaxed text-[var(--txt-2)]')

    def _plan_days(self, p) -> None:
        """Turen delt op i de sejldøgn den falder i — og hvor der overnattes."""
        if len(p.days) < 2:
            return
        ui.label('Dag for dag').classes('section-label mb-1.5 block')
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
                             f'{clock(d.arrive)} · {duration(d.hours)} med fart i') \
                        .classes('text-[11.5px] text-[var(--txt-3)] block')
                    if stop:
                        ui.label(f'Overnatning i {stop.name}, {stop.detail}. '
                                 f'{nm(stop.detour_nm)} sømil ind fra ruten. '
                                 f'Videre {clock(stop.depart)} næste morgen.') \
                            .classes('text-[12.5px] text-[var(--txt-2)] mt-1.5 '
                                     'leading-relaxed block')

    def _key_figures(self, p, boat) -> None:
        lim = self.s.limits
        metrics = [
            (duration(p.hours), 'Sejltid', ''),
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

        ui.label('Nøgletal').classes('section-label mb-1.5 block')
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
        ui.label('Stræk for stræk').classes('section-label mb-1 block')
        ui.label('Ruten er delt op efter kursskift, så hvert stykke gælder præcis '
                 'dér, hvor du styrer den kurs.') \
            .classes('text-[11.5px] text-[var(--txt-3)] mb-2 block leading-snug')
        with ui.element('div').classes('plan-legs mb-4'):
            for brief in narrative.stretch_briefs(route, p, boat):
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

        ui.label('Time for time').classes('section-label mt-4 mb-1.5 block')
        if not self.s.has_waves:
            ui.html('<div class="chip chip--warn mb-2">Ingen bølgeprognose for dette '
                    'farvand — vurder søgangen ud fra vind og stræk.</div>')

        motor = self.s.boat.is_motor
        rows = []
        current_day = None
        for s in p.segments:
            d = s.time.date()
            if d != current_day:
                current_day = d
                rows.append(f'<tr class="wx-day"><td colspan="7">'
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
                f'<td class="num tnum">{dk(s.speed_kn)}</td>'
                f'<td style="color:var(--txt-3)">{esc(mode)}</td>'
                f'</tr>')

        ui.html(
            '<div class="card overflow-hidden"><table class="wx-table">'
            '<thead><tr><th>Tid</th><th></th><th>Vind</th><th>Fra</th>'
            f'<th>Bølger</th><th>Fart</th><th>{"Søen" if motor else "Sejlføring"}</th>'
            f'</tr></thead><tbody>{"".join(rows)}</tbody></table></div>')

        peak = max(p.segments, key=lambda s: s.wind_kn)
        ui.label(f'Kraftigst omkring {day_time(peak.time)}: {peak.wind_kn:.0f} kn '
                 f'({beaufort(peak.wind_kn)}) fra {compass(peak.wind_dir)}, '
                 f'kast op til {peak.gust_kn:.0f} kn.') \
            .classes('text-[11.5px] text-[var(--txt-3)] leading-snug mt-2 block')

    def _ai_tab(self) -> None:
        ui.label('Skippervurdering').classes('section-label mt-5 mb-1.5 block')
        if not settings.ai_available:
            ui.html('<div class="card px-4 py-3.5 text-[12.5px] text-[var(--txt-3)] '
                    'leading-relaxed">Den AI-skrevne vurdering er ikke slået til på '
                    'denne server. Planen ovenfor er komplet uden den — sæt '
                    '<b>ANTHROPIC_API_KEY</b> i <b>.env</b> og genstart, hvis du også '
                    'vil have Claudes gennemgang.</div>')
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
            .classes('w-full mt-3 bg-[var(--teal)] text-white font-bold')

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
        self.boat_button.refresh()
        self.map_hint.refresh()
        self._redraw_map(fit=fit)

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

    # ── Waypoints ───────────────────────────────────────────────────
    def _map_clicked(self, lat: float, lon: float) -> None:
        """Et klik på kortet. Rammer det en havn eller land, retter vi det op.

        Man sigter sjældent efter et punkt i det åbne vand. Rammer klikket en
        havn, er det havnen man mener. Rammer det land, er det som regel kysten
        lige ved siden af — og ellers er det en fejl, der er værd at sige fra om,
        i stedet for at lægge en rute til midten af Sverige.
        """
        near = harbours.nearest(lat, lon, 1)
        if near and haversine(lat, lon, near[0].lat, near[0].lon) < 0.8:
            self._add_place(geocode.from_harbour(near[0]))
            return

        if not landmask.is_water(lat, lon):
            water = landmask.nearest_water(lat, lon, max_nm=1.5)
            if water == (lat, lon):
                ui.notify('Der er land her. Klik i vandet, eller søg efter en havn.',
                          type='warning', position='bottom')
                return
            lat, lon = water

        n = len(self.s.waypoints)
        self.s.add(Waypoint(lat, lon, 'Afgang' if n == 0 else f'Punkt {n + 1}'))
        self.refresh()
        self._schedule_route()

    def _harbour_clicked(self, lat: float, lon: float, name: str) -> None:
        found = [h for h in harbours.nearest(lat, lon, 3) if h.name == name]
        place = geocode.from_harbour(found[0]) if found else \
            geocode.Place(name, 'Lystbådehavn', lat, lon, geocode.HAVN)
        self._add_place(place)

    def _marker_dragged(self, index: int, lat: float, lon: float) -> None:
        if not (0 <= index < len(self.s.waypoints)):
            return
        wp = self.s.waypoints[index]
        wp.lat, wp.lon = lat, lon
        self.s.invalidate()
        self.s.persist()
        self.refresh()
        self._schedule_route()

    def _add_place(self, place: geocode.Place) -> None:
        wp = Waypoint(place.lat, place.lon, place.name)
        index = self._best_position(wp)
        self.s.insert(index, wp)
        self._suggestions = []
        if self.search_input:
            self.search_input.value = ''
        self.refresh(fit=True)
        self._schedule_route(fit=True)

        where = ('tilføjet' if index >= len(self.s.waypoints) - 1
                 else f'lagt ind som stop nr. {index + 1}')
        ui.notify(f'{place.name} {where}', type='positive', position='bottom')

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
        results = await geocode.search(name, limit=1)
        if results:
            self._add_place(results[0])

    def _remove(self, index: int) -> None:
        self.s.remove(index)
        self.refresh(fit=True)
        self._schedule_route(fit=True)

    def _move(self, index: int, delta: int) -> None:
        self.s.move(index, delta)
        self.refresh()
        self._schedule_route()

    def _reverse_route(self) -> None:
        if len(self.s.waypoints) < 2:
            return
        self.s.reverse()
        self.refresh()
        self._schedule_route()
        ui.notify('Ruten er vendt om', position='bottom')

    def _clear_route(self) -> None:
        self.s.clear()
        self._suggestions = []
        self.refresh(fit=True)

    # ── Søgning ─────────────────────────────────────────────────────
    def _search_changed(self, e) -> None:
        """Søg mens der tastes, men vent til fingrene falder til ro."""
        query = (e.value or '').strip()
        if self._search_task:
            self._search_task.cancel()
        if len(query) < 2:
            self._suggestions = []
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
            self.refresh()
            ui.notify('Ingen afgange passer til dine grænser. Prøv et bredere '
                      'datointerval, et længere sejldøgn eller en højere vindgrænse.',
                      type='warning', position='bottom', timeout=7000)
            return

        self.s.step = 2
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
        if self.map:
            self.map.set_dark(bool(self.dark.value))

    def _open_settings(self) -> None:
        from .settings import settings_dialog
        settings_dialog(self)
