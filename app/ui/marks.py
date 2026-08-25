"""Opslagsværket: sømærker, fyr, lanterner og signaler.

Teksten står i manualen; det her er den udgave, man slår op i, mens man sejler
— med tegningerne, og delt op så man kan finde det ene mærke, man står og
kigger på, uden at læse resten.
"""
from __future__ import annotations

from html import escape as esc

from nicegui import ui

from .. import seamanship as sm
from ..i18n import t


def dialog(planner=None) -> None:
    """Hele opslagsværket. Åbnes fra kortet og fra manualen."""
    if planner is not None:
        # Dialogen skal høre til fladen, ikke til dét, man kom fra.
        with planner.client.content:
            _byg()
        return
    _byg()


def _byg() -> None:
    with ui.dialog() as dlg, ui.card().classes(
            'w-full max-w-[520px] p-0 bg-[var(--sea-1)] rounded-[var(--r)]'):

        with ui.row().classes('w-full items-center px-5 py-3.5 border-b '
                              'border-[var(--line)] no-wrap'):
            ui.icon('waves').classes('text-[20px] text-[var(--accent)]')
            ui.label(t('Sømærker og signaler')).classes(
                'text-[16px] font-bold flex-1')
            ui.button(icon='close', on_click=dlg.close) \
                .props('flat round dense')

        with ui.element('div').classes(
                'scroll-y px-5 py-4 max-h-[74dvh] w-full'):
            ui.label(t('Afmærkningen er IALA A — Danmark, Tyskland, Sverige, '
                       'Norge og resten af Europa.')) \
                .classes('text-[11.5px] text-[var(--txt-3)] leading-snug '
                         'mb-3 block')

            _afmærkning()
            _fyr()
            _liste(t('Lanterner om natten'), sm.LANTERNS, 'light_mode')
            _liste(t('Dagsignaler'), sm.DAY_SHAPES, 'wb_sunny')
            _liste(t('Lydsignaler når I ser hinanden'), sm.SOUND_MANOEUVRE,
                   'campaign')
            _liste(t('Lydsignaler i nedsat sigtbarhed'), sm.SOUND_FOG,
                   'foggy')
            _liste(t('Nødsignaler'), sm.DISTRESS, 'sos')

            ui.html('<div class="hairline mt-4 mb-3"></div>')
            ui.label(t('En huskeseddel, ikke Søvejsreglerne. Er du i tvivl '
                       'om en vigepligt, er det reglerne, der gælder. Og '
                       'farerne står i søkortet — dem kender Sejlplan '
                       'ikke.')) \
                .classes('text-[11px] text-[var(--txt-3)] leading-snug block')

        with ui.row().classes('w-full items-center px-5 pb-4 no-wrap'):
            ui.element('div').classes('flex-1')
            ui.button(t('Luk'), on_click=dlg.close) \
                .props('flat no-caps').classes('text-[var(--txt-2)]')

    dlg.open()


def _overskrift(titel: str, ikon: str) -> None:
    with ui.element('div').classes('flex items-center gap-2 mt-4 mb-2'):
        ui.icon(ikon).classes('text-[16px] text-[var(--accent)]')
        ui.html(f'<span class="section-label">{esc(titel)}</span>')


def _afmærkning() -> None:
    _overskrift(t('Sømærker'), 'anchor')
    for m in sm.MARKS:
        with ui.element('div').classes(
                'card px-3.5 py-3 mb-2 flex items-start gap-3.5'):
            ui.html(f'<div class="mark-art">{m.svg}</div>')
            with ui.element('div').classes('min-w-0 flex-1'):
                ui.label(t(m.name)).classes(
                    'text-[13px] font-semibold block mb-0.5')
                ui.label(t(m.meaning)).classes(
                    'text-[11.5px] text-[var(--txt-3)] leading-snug block')
                ui.label(t(m.action)).classes(
                    'text-[12px] leading-snug block mt-1.5')
                with ui.element('div').classes(
                        'flex items-center gap-1.5 mt-1.5 flex-wrap'):
                    ui.html('<span class="chip">'
                            f'{esc(t(m.light))}</span>')
                if m.memo:
                    with ui.element('div').classes(
                            'flex items-start gap-1.5 mt-1.5'):
                        ui.icon('lightbulb').classes(
                            'text-[13px] text-[var(--accent)] shrink-0 '
                            'mt-0.5')
                        ui.label(t(m.memo)).classes(
                            'text-[11px] text-[var(--txt-2)] leading-snug')


def _fyr() -> None:
    _overskrift(t('Sådan læses en fyrkarakter'), 'flare')
    with ui.element('div').classes('card overflow-hidden'):
        for i, (kort, betyder) in enumerate(sm.LIGHTS):
            if i:
                ui.html('<div class="hairline"></div>')
            with ui.element('div').classes(
                    'flex items-start gap-3 px-3 py-1.5'):
                ui.html(f'<span class="trim-part tnum">{esc(kort)}</span>')
                ui.label(t(betyder)).classes(
                    'text-[12px] leading-snug text-[var(--txt-2)] flex-1')
    kort, betyder = sm.LIGHT_EXAMPLE
    with ui.element('div').classes('flex items-start gap-2.5 mt-2'):
        ui.icon('lightbulb').classes(
            'text-[15px] text-[var(--accent)] shrink-0 mt-0.5')
        with ui.element('div').classes('min-w-0'):
            ui.html(f'<b class="tnum text-[12px]">{esc(kort)}</b>')
            ui.label(t(betyder)).classes(
                'text-[11.5px] text-[var(--txt-2)] leading-snug block')
    ui.label(t(sm.SECTORS)).classes(
        'text-[11.5px] text-[var(--txt-2)] leading-snug mt-2 block')


def _liste(titel: str, rækker, ikon: str) -> None:
    _overskrift(titel, ikon)
    with ui.element('div').classes('card overflow-hidden'):
        for i, s in enumerate(rækker):
            if i:
                ui.html('<div class="hairline"></div>')
            with ui.element('div').classes('px-3 py-2'):
                ui.label(t(s.what)).classes(
                    'text-[12px] font-medium block')
                ui.label(t(s.means)).classes(
                    'text-[11.5px] text-[var(--txt-3)] leading-snug block '
                    'mt-0.5')
