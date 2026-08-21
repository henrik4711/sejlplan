"""Brugerens egen båd.

De faste både i `boats.py` er eksempler. Ingen ejer et eksempel — man ejer en
bestemt båd med en bestemt fart og et bestemt forbrug, og en plan, der regner på
en anden båds tal, er ikke ens egen plan. Herinde kan man taste sin ind.

Så få felter som muligt. For en motorbåd er det ligetil: marchfart, skrogtype,
forbrug. For en sejlbåd ville det rigtige være et polardiagram, men det har de
færreste liggende — så vi spørger om ét tal, enhver sejler kender: farten for
halvvind i jævn vind. `boats.scaled_polar` skalerer en almindelig krydsers
diagram, så det rammer dét tal.
"""
from __future__ import annotations

from nicegui import ui

from ..boats import (CUSTOM_ID, DISPLACEMENT, MOTOR, PLANING, SAIL, SEMI,
                     reference_speed)


def own_boat_block(s, refresh_boats, refresh_limits) -> None:
    """Kortet øverst i indstillingerne: din båd, eller en knap til at lave den."""
    ui.html('<span class="section-label">Din båd</span>')
    chosen = s.boat_id == CUSTOM_ID

    with ui.element('div').classes('mt-2 mb-4'):
        if not s.has_custom:
            ui.button('Læg din egen båd ind', icon='add',
                      on_click=lambda: editor(s, refresh_boats, refresh_limits)) \
                .props('outline no-caps').classes('w-full text-[var(--accent)]')
            ui.label('Længde, fart og forbrug. Så regner planen på din båd i '
                     'stedet for på et eksempel.') \
                .classes('text-[11px] text-[var(--txt-3)] mt-1.5 block leading-snug')
            return

        boat = s.boat
        card = ui.element('div').classes(
            'card px-3.5 py-3 flex items-center gap-3 cursor-pointer transition-all '
            + ('ring-1 ring-[var(--accent)] border-[var(--accent)]' if chosen
               else 'hover:border-[var(--line-2)]'))
        with card:
            ui.icon(boat.icon).classes(
                'text-[20px] shrink-0 ' + ('text-[var(--accent)]' if chosen
                                           else 'text-[var(--txt-3)]'))
            with ui.element('div').classes('min-w-0 flex-1'):
                ui.label(boat.name).classes('text-[13.5px] font-semibold truncate block')
                ui.label(boat.summary).classes(
                    'text-[11px] text-[var(--txt-3)] truncate block')
            ui.button('Ret', icon='edit',
                      on_click=lambda: editor(s, refresh_boats, refresh_limits)) \
                .props('flat dense no-caps size=sm').classes('text-[var(--accent)] shrink-0')

        def choose() -> None:
            s.set_boat(CUSTOM_ID)
            refresh_boats()
            refresh_limits()

        card.on('click', lambda _: choose())


def editor(s, refresh_boats, refresh_limits) -> None:
    """Formularen. Felterne skifter, alt efter om det er sejl eller motor."""
    spec = dict(s.custom) if s.custom else {'kind': SAIL}
    fields: dict = {}

    with ui.dialog() as dialog, ui.card().classes(
            'w-full max-w-[440px] p-0 bg-[var(--sea-1)] rounded-[var(--r)]'):

        with ui.row().classes('w-full items-center px-5 py-3.5 border-b '
                              'border-[var(--line)] no-wrap'):
            ui.icon('directions_boat').classes('text-[20px] text-[var(--accent)]')
            ui.label('Din båd').classes('text-[16px] font-bold flex-1')
            ui.button(icon='close', on_click=dialog.close).props('flat round dense')

        with ui.element('div').classes('scroll-y px-5 py-4 max-h-[66dvh] w-full'):
            fields['name'] = ui.input('Navn', value=spec.get('name') or '') \
                .props('outlined dense autofocus').classes('w-full')

            ui.label('Type').classes('text-[11.5px] text-[var(--txt-3)] mt-4 mb-1 block')
            kind = ui.toggle({SAIL: 'Sejlbåd', MOTOR: 'Motorbåd'},
                             value=spec.get('kind') or SAIL) \
                .props('no-caps unelevated dense spread').classes('w-full')
            fields['kind'] = kind

            _number(fields, 'length_m', 'Længde overalt', 'm',
                    spec.get('length_m'), 10.0)

            @ui.refreshable
            def by_kind() -> None:
                if kind.value == MOTOR:
                    _number(fields, 'cruise_kn', 'Marchfart i smult vande', 'kn',
                            spec.get('cruise_kn'), 12.0)
                    ui.label('Skrogtype').classes(
                        'text-[11.5px] text-[var(--txt-3)] mt-4 mb-1 block')
                    fields['hull'] = ui.toggle(
                        {DISPLACEMENT: 'Fortrængning', SEMI: 'Halvplanende',
                         PLANING: 'Planende'}, value=spec.get('hull') or SEMI) \
                        .props('no-caps unelevated dense spread').classes('w-full')
                    ui.label('Skroget afgør, hvor meget søen tager af farten. '
                             'En planende båd taber mest.') \
                        .classes('text-[11px] text-[var(--txt-3)] mt-1 block leading-snug')
                    _number(fields, 'fuel_lph', 'Forbrug ved marchfart', 'l/t',
                            spec.get('fuel_lph'), 40.0)
                else:
                    _number(fields, 'reach_kn', 'Fart for halvvind i 10 knobs vind',
                            'kn', spec.get('reach_kn'), reference_speed())
                    ui.label('Det ene tal skalerer et almindeligt polardiagram, så '
                             'farten passer til din båd. Ved du det ikke, så gæt på '
                             'en god dag med fuld sejlføring.') \
                        .classes('text-[11px] text-[var(--txt-3)] mt-1 block leading-snug')
                    _number(fields, 'motor_speed_kn', 'Fart for motor', 'kn',
                            spec.get('motor_speed_kn'), 5.5)
                    _number(fields, 'fuel_lph', 'Forbrug for motor', 'l/t',
                            spec.get('fuel_lph'), 3.0)

            by_kind()
            kind.on_value_change(lambda _: by_kind.refresh())

            ui.html('<div class="hairline mt-5 mb-3"></div>')
            ui.label('Hvad du kan holde til').classes('section-label mb-1 block')
            ui.label('Over de her værdier markerer planen timerne som skærpede.') \
                .classes('text-[11px] text-[var(--txt-3)] mb-1 block leading-snug')
            _number(fields, 'max_wind_kn', 'Højeste vind', 'kn',
                    spec.get('max_wind_kn'), 20.0)
            _number(fields, 'max_wave_m', 'Højeste bølger', 'm',
                    spec.get('max_wave_m'), 1.5)

        with ui.row().classes('w-full items-center gap-2 px-5 py-3.5 border-t '
                              'border-[var(--line)] no-wrap'):
            ui.element('div').classes('flex-1')
            ui.button('Annullér', on_click=dialog.close) \
                .props('flat no-caps').classes('text-[var(--txt-2)]')
            ui.button('Gem båden',
                      on_click=lambda: _save(s, fields, dialog,
                                             refresh_boats, refresh_limits)) \
                .props('unelevated no-caps') \
                .classes('bg-[var(--accent)] text-[var(--sea-1)] font-bold px-4')

    dialog.open()


def _number(fields: dict, key: str, label: str, unit: str, value, fallback) -> None:
    fields[key] = ui.number(label, value=value if value is not None else fallback,
                            min=0, step=0.1, suffix=f' {unit}') \
        .props('outlined dense').classes('w-full mt-3')


def _save(s, fields: dict, dialog, refresh_boats, refresh_limits) -> None:
    spec = {key: field.value for key, field in fields.items()}
    if not str(spec.get('name') or '').strip():
        ui.notify('Giv båden et navn', type='warning', position='bottom')
        return
    s.set_custom(spec)
    dialog.close()
    refresh_boats()
    refresh_limits()
    ui.notify(f'{s.boat.name} er gemt og valgt', type='positive', position='bottom')
