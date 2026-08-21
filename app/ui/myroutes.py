"""Mine ruter.

En tur på fjorten dage kan ikke planlægges på én gang — vejrudsigten rækker ti
døgn. Så må ruten kunne ligge og vente, mens prognosen ruller frem. Og har man
først lagt en rute, man er glad for, skal den ikke tastes ind igen næste sommer.

Ruterne ligger i sessionen sammen med alt andet, så de rejser med den kopi, der
lægges i browserens eget lager. En udrulning kan ikke tage dem.

Ét tryk på Gem opdaterer den rute, man arbejder i. Det er sådan, man forventer
det af alt andet, man skriver i — en tvilling skal man bede om.
"""
from __future__ import annotations

from datetime import date

from nicegui import ui

from ..dates import day


def save_dialog(s, refresh) -> None:
    """Gem ruten. Har man en åben i forvejen, er det den, der opdateres."""
    if len(s.waypoints) < 1:
        ui.notify('Der er ingen rute at gemme', type='warning', position='bottom')
        return

    open_name = s.saved_name

    with ui.dialog() as dialog, ui.card().classes(
            'w-full max-w-[420px] p-0 bg-[var(--sea-1)] rounded-[var(--r)]'):
        with ui.element('div').classes('px-5 pt-5 pb-1'):
            ui.label('Gem ruten' if not open_name else 'Gem ændringer') \
                .classes('text-[16px] font-bold block')
            ui.label(f'{len(s.waypoints)} punkter · {s.total_nm:.0f} sømil') \
                .classes('text-[12.5px] text-[var(--txt-3)] mt-0.5 block')

        with ui.element('div').classes('px-5 pt-3'):
            navn = ui.input('Navn', value=open_name or s.route_title) \
                .props('outlined dense autofocus maxlength=60').classes('w-full')

        def gem(as_new: bool) -> None:
            s.save_route(navn.value, as_new=as_new)
            dialog.close()
            refresh()
            ui.notify(f'"{s.saved_name}" er gemt', type='positive', position='bottom')

        with ui.row().classes('w-full items-center gap-2 px-5 py-4 no-wrap'):
            if open_name:
                # Kun relevant, når der findes en at lave en kopi af.
                ui.button('Gem som ny', on_click=lambda: gem(True)) \
                    .props('flat no-caps').classes('text-[var(--txt-2)]')
            ui.element('div').classes('flex-1')
            ui.button('Fortryd', on_click=dialog.close) \
                .props('flat no-caps').classes('text-[var(--txt-2)]')
            ui.button('Gem', on_click=lambda: gem(False)) \
                .props('unelevated no-caps').classes('btn-primary px-4')

        navn.on('keydown.enter', lambda _: gem(False))

    dialog.open()


def open_dialog(s, open_saved, refresh) -> None:
    """Hylden med gemte ruter."""
    with ui.dialog() as dialog, ui.card().classes(
            'w-full max-w-[460px] p-0 bg-[var(--sea-1)] rounded-[var(--r)]'):

        with ui.row().classes('w-full items-center px-5 py-3.5 border-b '
                              'border-[var(--line)] no-wrap'):
            ui.icon('bookmarks').classes('text-[20px] text-[var(--accent)]')
            ui.label('Mine ruter').classes('text-[16px] font-bold flex-1')
            ui.button(icon='close', on_click=dialog.close).props('flat round dense')

        body = ui.element('div').classes('scroll-y px-5 py-4 max-h-[62dvh] w-full')

        @ui.refreshable
        def liste() -> None:
            rows(s, lambda rid: (dialog.close(), open_saved(rid)),
                 lambda: (liste.refresh(), refresh()))

        with body:
            liste()

    dialog.open()


def rows(s, on_open, changed) -> None:
    """Selve listen. Bruges både i dialogen og på den tomme rute-side."""
    if not s.routes:
        with ui.element('div').classes('empty py-6'):
            ui.icon('bookmark_border') \
                .classes('text-[36px] text-[var(--accent)] opacity-40 mb-2')
            ui.label('Ingen gemte ruter endnu').classes('empty-title')
            ui.label('Læg en rute, og tryk Gem. Så ligger den her næste gang — '
                     'også hvis du lukker fanen.').classes('empty-sub')
        return

    for row in list(s.routes):
        _row(s, row, on_open, changed)


def _row(s, row: dict, on_open, changed) -> None:
    rid = row.get('id') or ''
    aktiv = rid == s.route_id and bool(s.waypoints)
    n = len(row.get('waypoints') or [])

    card = ui.element('div').classes(
        'card px-3.5 py-2.5 mb-2 flex items-center gap-3 cursor-pointer '
        'transition-all '
        + ('ring-1 ring-[var(--accent)] border-[var(--accent)]' if aktiv
           else 'hover:border-[var(--line-2)]'))
    with card:
        ui.icon('bookmark' if aktiv else 'bookmark_border').classes(
            'text-[19px] shrink-0 '
            + ('text-[var(--accent)]' if aktiv else 'text-[var(--txt-3)]'))

        with ui.element('div').classes('min-w-0 flex-1'):
            ui.label(row.get('name') or 'Uden navn') \
                .classes('text-[13.5px] font-semibold truncate block')
            ui.label(f'{n} punkter · {row.get("nm", 0):.0f} sømil '
                     f'· gemt {_when(row.get("saved"))}') \
                .classes('text-[11px] text-[var(--txt-3)] truncate block')

        with ui.button(icon='more_horiz').props('flat round dense size=sm') \
                .classes('shrink-0 text-[var(--txt-3)]') as menu_btn:
            with ui.menu().classes('min-w-[180px]'):
                ui.menu_item('Omdøb', lambda: _rename(s, row, changed))
                ui.menu_item('Slet', lambda: _confirm_delete(s, row, changed))
        # Menuknappen må ikke også åbne ruten under sig.
        menu_btn.on('click.stop', lambda _: None)

    card.on('click', lambda _, k=rid: on_open(k))


def _rename(s, row: dict, changed) -> None:
    with ui.dialog() as ask, ui.card().classes(
            'w-full max-w-[380px] p-0 bg-[var(--sea-1)] rounded-[var(--r)]'):
        with ui.element('div').classes('px-5 pt-5 pb-1'):
            ui.label('Omdøb ruten').classes('text-[16px] font-bold block')
        with ui.element('div').classes('px-5 pt-3'):
            navn = ui.input('Navn', value=row.get('name') or '') \
                .props('outlined dense autofocus maxlength=60').classes('w-full')

        def gem() -> None:
            s.rename_route(row.get('id') or '', navn.value)
            ask.close()
            changed()

        with ui.row().classes('w-full items-center gap-2 px-5 py-4 no-wrap'):
            ui.element('div').classes('flex-1')
            ui.button('Fortryd', on_click=ask.close) \
                .props('flat no-caps').classes('text-[var(--txt-2)]')
            ui.button('Gem', on_click=gem) \
                .props('unelevated no-caps').classes('btn-primary px-4')
        navn.on('keydown.enter', lambda _: gem())
    ask.open()


def _confirm_delete(s, row: dict, changed) -> None:
    """Spørg først. En gemt rute er noget, nogen har brugt tid på."""
    with ui.dialog() as ask, ui.card().classes(
            'w-full max-w-[380px] p-0 bg-[var(--sea-1)] rounded-[var(--r)]'):
        with ui.element('div').classes('px-5 pt-5 pb-3'):
            ui.label('Slet ruten?').classes('text-[16px] font-bold block')
            ui.label(f'"{row.get("name") or "Uden navn"}" forsvinder. '
                     f'Det kan ikke fortrydes.') \
                .classes('text-[13px] text-[var(--txt-2)] leading-snug mt-1 block')

        def slet() -> None:
            s.delete_route(row.get('id') or '')
            ask.close()
            changed()
            ui.notify('Ruten er slettet', position='bottom')

        with ui.row().classes('w-full items-center gap-2 px-5 pb-4 no-wrap'):
            ui.element('div').classes('flex-1')
            ui.button('Behold', on_click=ask.close) \
                .props('flat no-caps').classes('text-[var(--txt-2)]')
            ui.button('Slet', on_click=slet).props('unelevated no-caps') \
                .classes('bg-[var(--stop)] text-white font-bold px-4')
    ask.open()


def _when(iso: str | None) -> str:
    """'i dag', 'i går', ellers datoen. Det er sådan man husker det."""
    try:
        d = date.fromisoformat(str(iso))
    except (TypeError, ValueError):
        return 'tidligere'
    delta = (date.today() - d).days
    if delta <= 0:
        return 'i dag'
    if delta == 1:
        return 'i går'
    return day(d, short=False)
