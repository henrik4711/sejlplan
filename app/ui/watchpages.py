"""De to sider, links i mailen fører til.

Bekræft og stop. Begge skal kunne åbnes af en, der har fået en mail og trykket
på et link — ikke af en, der er logget ind. Derfor er nøglen i adressen, og den
er lang nok til, at man ikke gætter den.

Siderne er små med vilje. Man er kommet for at trykke ja eller for at slippe;
begge dele skal tage ét blik.
"""
from __future__ import annotations

from datetime import date

from nicegui import ui

from .. import theme, watch
from ..dates import day


def register() -> None:
    """Læg siderne på plads. Kaldes én gang ved opstart."""

    @ui.page('/vagt/ja/{watch_id}')
    def confirm_page(watch_id: str) -> None:
        theme.apply()
        w = watch.confirm(watch_id)
        if w is None:
            _shell('Vagten findes ikke',
                   'Linket er forkert, eller vagten er allerede stoppet.',
                   'help_outline')
            return
        start, end = w.window
        _shell(
            'Vagten er i gang',
            f'Vi holder øje med {w.title} mellem '
            f'{day(start, short=False)} og {day(end, short=False)}. '
            f'Du hører fra os, når der er et vindue, du kan sejle i — '
            f'og kun den ene gang.',
            'notifications_active', stop_id=w.id)

    @ui.page('/vagt/stop/{watch_id}')
    def stop_page(watch_id: str) -> None:
        theme.apply()
        w = watch.cancel(watch_id)
        if w is None:
            _shell('Vagten findes ikke',
                   'Linket er forkert, eller vagten er allerede stoppet.',
                   'help_outline')
            return
        _shell('Vagten er stoppet',
               f'Vi holder ikke længere øje med {w.title}, og vi skriver ikke '
               f'til dig om den igen.',
               'notifications_off')


def _shell(title: str, body: str, icon: str, stop_id: str = '') -> None:
    """Én besked, midt på siden. Der er ikke andet at lave her."""
    with ui.element('div').classes(
            'fixed inset-0 flex items-center justify-center px-6 '
            'bg-[var(--sea-2)]'):
        with ui.element('div').classes(
                'card px-7 py-8 max-w-[430px] w-full text-center'):
            ui.icon(icon).classes(
                'text-[42px] text-[var(--accent)] opacity-80 mb-3')
            ui.label(title).classes(
                'text-[20px] font-bold leading-tight block mb-2')
            ui.label(body).classes(
                'text-[13.5px] text-[var(--txt-2)] leading-relaxed block')

            with ui.row().classes('items-center justify-center gap-2 mt-6 w-full'):
                ui.button('Åbn Sejlplan',
                          on_click=lambda: ui.navigate.to('/')) \
                    .props('unelevated no-caps').classes('btn-primary px-4')
                if stop_id:
                    ui.button('Stop vagten',
                              on_click=lambda: ui.navigate.to(
                                  f'/vagt/stop/{stop_id}')) \
                        .props('flat no-caps').classes('text-[var(--txt-3)]')

            ui.label(f'Sejlplan · {date.today():%Y}').classes(
                'text-[11px] text-[var(--txt-3)] mt-6 block')
