"""Beskeder mellem to både, der begge er synlige.

Man trykker på en båd på kortet og skriver. Ikke en indbakke med fremmede, ikke
en opslagstavle — en samtale mellem to, der ligger i det samme farvand lige nu,
og som begge har valgt at være synlige.

Blokering og anmeldelse står i selve samtalen, ikke gemt i en menu et sted.
Skal man kunne bruge dem, skal de være der, hvor man opdager, at man har brug
for dem.
"""
from __future__ import annotations

from nicegui import ui

from .. import chat
from ..i18n import t
from . import fleet as fleetui


def available() -> bool:
    return chat.available()


def open_with(planner, other_mark: str, other_name: str) -> None:
    """Åbn samtalen med én bestemt båd."""
    mine = fleetui.mark()
    if not mine or not other_mark or mine == other_mark:
        return
    chat.mark_seen(mine, other_mark)
    planner.fleet_line.refresh()

    # Dialogen skal høre til fladen, ikke til den dialog man kom fra. Åbner man
    # samtalen fra indbakken, er indbakken ved at lukke i samme øjeblik — og en
    # dialog, der er lavet inde i den, forsvinder med den. Samme fælde som
    # tidsmåleren i flåden.
    with planner.client.content:
        _thread_dialog(planner, mine, other_mark, other_name)


def _thread_dialog(planner, mine: str, other_mark: str,
                   other_name: str) -> None:
    with ui.dialog() as dlg, ui.card().classes(
            'w-full max-w-[440px] p-0 bg-[var(--sea-1)] rounded-[var(--r)]'):

        with ui.row().classes('w-full items-center px-5 py-3.5 border-b '
                              'border-[var(--line)] no-wrap'):
            ui.icon('sailing').classes('text-[19px] text-[var(--accent)]')
            ui.label(other_name).classes(
                'text-[15px] font-bold flex-1 truncate')
            with ui.button(icon='more_horiz').props('flat round dense') \
                    .classes('text-[var(--txt-3)]'):
                with ui.menu().classes('min-w-[210px]'):
                    ui.menu_item(t('Bloker denne båd'),
                                 lambda: _block(planner, other_mark,
                                                other_name, dlg))
            ui.button(icon='close', on_click=dlg.close).props('flat round dense')

        beskeder = ui.element('div').classes(
            'scroll-y px-5 py-4 max-h-[52dvh] w-full flex flex-col gap-2')

        @ui.refreshable
        def traad() -> None:
            rows = chat.thread(mine, other_mark)
            if not rows:
                ui.label(t('Ingen beskeder endnu. Skriv den første.')) \
                    .classes('text-[12.5px] text-[var(--txt-3)] '
                             'text-center py-4 block')
                return
            for m in rows:
                _bubble(m, m.from_mark == mine, planner, other_name)

        with beskeder:
            traad()

        with ui.element('div').classes('px-5 pb-4 pt-1'):
            felt = ui.input(placeholder=t('Skriv en kort besked…')) \
                .props(f'outlined dense maxlength={chat.TEXT_MAX} '
                       f'autofocus').classes('w-full')

            def send() -> None:
                ok, grund = chat.send(mine, fleetui.saved_name() or 'Båd',
                                      other_mark, felt.value or '')
                if not ok:
                    ui.notify(t(grund) if grund else t('Kunne ikke sendes'),
                              type='warning', position='bottom')
                    return
                felt.value = ''
                traad.refresh()

            felt.on('keydown.enter', lambda _: send())
            with ui.row().classes('w-full items-center gap-2 mt-2 no-wrap'):
                ui.label(t('Beskeder forsvinder efter et døgn.')) \
                    .classes('text-[10.5px] text-[var(--txt-3)] flex-1 '
                             'leading-snug')
                ui.button(t('Send'), icon='send', on_click=send) \
                    .props('unelevated dense no-caps') \
                    .classes('btn-primary px-3 shrink-0')

    dlg.open()


def _bubble(m, mine: bool, planner, other_name: str) -> None:
    """Én besked. Anmeldelse sidder på den, ikke i en menu."""
    with ui.element('div').classes(
            'flex flex-col ' + ('items-end' if mine else 'items-start')):
        boks = ui.element('div').classes(
            'px-3 py-2 rounded-[13px] max-w-[85%] '
            + ('bg-[var(--accent-soft)]' if mine else 'bg-[var(--sea-3)]'))
        with boks:
            ui.label(m.text).classes(
                'text-[13px] leading-snug block whitespace-pre-wrap')
        with ui.element('div').classes('flex items-center gap-2 mt-0.5'):
            ui.label(m.age).classes('text-[10.5px] text-[var(--txt-3)]')
            if not mine:
                ui.button(t('Anmeld'),
                          on_click=lambda _=None, x=m: _report(x, planner)) \
                    .props('flat dense no-caps size=xs') \
                    .classes('text-[var(--txt-3)] hover:text-[var(--stop)]')


def _report(m, planner) -> None:
    """Anmeld en besked. Teksten gemmes, så den ikke dør med beskeden."""
    if chat.report_abuse(m.id, fleetui.mark()):
        ui.notify(t('Beskeden er anmeldt. Vi gemmer den, så den kan ses '
                    'efter.'), position='bottom', multi_line=True)
    else:
        ui.notify(t('Beskeden findes ikke længere.'), position='bottom')


def _block(planner, other_mark: str, other_name: str, dlg) -> None:
    """Bloker. Virker begge veje og med det samme."""
    with ui.dialog() as ask, ui.card().classes(
            'w-full max-w-[380px] p-0 bg-[var(--sea-1)] rounded-[var(--r)]'):
        with ui.element('div').classes('px-5 pt-5 pb-3'):
            ui.label(f'{t("Bloker")} {other_name}?').classes(
                'text-[16px] font-bold block')
            ui.label(t('I kan ikke længere skrive til hinanden, og I kan '
                       'ikke se hinanden på kortet. Det gælder begge veje.')) \
                .classes('text-[13px] text-[var(--txt-2)] leading-snug '
                         'mt-1 block')

        def gør() -> None:
            chat.block(fleetui.mark(), other_mark)
            ask.close()
            dlg.close()
            fleetui.refresh(planner)
            ui.notify(f'{other_name} {t("er blokeret")}', position='bottom')

        with ui.row().classes('w-full items-center gap-2 px-5 pb-4 no-wrap'):
            ui.element('div').classes('flex-1')
            ui.button(t('Fortryd'), on_click=ask.close) \
                .props('flat no-caps').classes('text-[var(--txt-2)]')
            ui.button(t('Bloker'), on_click=gør) \
                .props('unelevated no-caps') \
                .classes('bg-[var(--stop)] text-white font-bold px-4')
    ask.open()


def inbox_dialog(planner) -> None:
    """De både, der har skrevet. Én linje hver."""
    mine = fleetui.mark()
    rows = chat.inbox(mine)
    if not rows:
        ui.notify(t('Ingen beskeder'), position='bottom')
        return

    # Nyeste besked per båd — det er samtaler, ikke en liste af beskeder.
    seneste: dict = {}
    for m in rows:
        seneste[m.from_mark] = m

    with planner.client.content:
        _inbox(planner, seneste)


def _inbox(planner, seneste: dict) -> None:
    with ui.dialog() as dlg, ui.card().classes(
            'w-full max-w-[430px] p-0 bg-[var(--sea-1)] rounded-[var(--r)]'):
        with ui.row().classes('w-full items-center px-5 py-3.5 border-b '
                              'border-[var(--line)] no-wrap'):
            ui.icon('forum').classes('text-[20px] text-[var(--accent)]')
            ui.label(t('Beskeder')).classes('text-[16px] font-bold flex-1')
            ui.button(icon='close', on_click=dlg.close).props('flat round dense')

        with ui.element('div').classes('scroll-y px-5 py-4 max-h-[60dvh] w-full'):
            for m in sorted(seneste.values(), key=lambda x: x.when,
                            reverse=True):
                card = ui.element('div').classes(
                    'card px-3.5 py-2.5 mb-2 flex items-center gap-3 '
                    'cursor-pointer hover:border-[var(--line-2)]')
                with card:
                    ui.icon('sailing').classes(
                        'text-[17px] text-[var(--accent)] shrink-0')
                    with ui.element('div').classes('min-w-0 flex-1'):
                        ui.label(m.from_name or 'Båd').classes(
                            'text-[13px] font-semibold truncate block')
                        ui.label(m.text).classes(
                            'text-[11.5px] text-[var(--txt-3)] truncate block')
                    ui.label(m.age).classes(
                        'text-[10.5px] text-[var(--txt-3)] shrink-0')
                card.on('click', lambda _, k=m.from_mark,
                        n=m.from_name: (dlg.close(),
                                        open_with(planner, k, n or 'Båd')))
    dlg.open()
