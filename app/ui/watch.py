"""Vejrvagten i fladen: læg en vagt på den rute, du står med.

Tanken er simpel og gælder især dem, der ikke er bundet af en arbejdsuge: "vi
skal til Ærø engang i september — sig til, når det ser godt ud." Så skal man
ikke sidde og opdatere en side i fjorten dage.

Derfor spørger vi om så lidt som muligt: adressen, og hvornår du kan. Båden,
grænserne og sejldøgnet er dem, du allerede har sat — vagten regner med dem,
som de var, da du lagde den.
"""
from __future__ import annotations

from datetime import date, timedelta

from nicegui import ui

from .. import lookout, watch
from ..config import settings
from ..dates import day
from ..state import MAX_FORECAST_DAYS
from ..i18n import t

# Så langt frem kan man lægge en vagt. Prognosen rækker ti døgn, men en vagt
# giver netop mening længere ude end det — det er hele pointen, at den venter
# på, at prognosen når frem.
MAX_AHEAD_DAYS = 120


def dialog(s) -> None:
    """Læg en vagt på den rute, der ligger på bordet."""
    if len(s.waypoints) < 2:
        ui.notify('Læg først en rute med mindst to punkter',
                  type='warning', position='bottom')
        return

    if not settings.watch_available:
        _not_ready()
        return

    today = date.today()
    start = today + timedelta(days=MAX_FORECAST_DAYS)
    slut = start + timedelta(days=6)
    felter: dict = {}

    with ui.dialog() as dlg, ui.card().classes(
            'w-full max-w-[460px] p-0 bg-[var(--sea-1)] rounded-[var(--r)]'):

        with ui.row().classes('w-full items-center px-5 py-3.5 border-b '
                              'border-[var(--line)] no-wrap'):
            ui.icon('notifications_active') \
                .classes('text-[20px] text-[var(--accent)]')
            ui.label(t('Vejrvagt')).classes('text-[16px] font-bold flex-1')
            ui.button(icon='close', on_click=dlg.close).props('flat round dense')

        with ui.element('div').classes('scroll-y px-5 py-4 max-h-[70dvh] w-full'):
            ui.label(f'Vi holder øje med {s.route_title} og skriver til dig, '
                     f'når der er et vindue, du kan sejle i. Én mail — ikke '
                     f'en strøm af dem.') \
                .classes('text-[12.5px] text-[var(--txt-2)] leading-snug '
                         'mb-4 block')

            felter['name'] = ui.input('Dit navn (valgfrit)') \
                .props('outlined dense').classes('w-full mb-3')
            felter['email'] = ui.input('Din mailadresse') \
                .props('outlined dense type=email autofocus '
                       'inputmode=email autocomplete=email').classes('w-full')

            ui.label(t('Hvornår kan I komme afsted?')) \
                .classes('text-[11.5px] text-[var(--txt-3)] mt-5 mb-1 block')
            with ui.element('div').classes('grid grid-cols-2 gap-3'):
                felter['from'] = ui.input('Tidligst', value=start.isoformat()) \
                    .props('outlined dense type=date '
                           f'min={today.isoformat()} '
                           f'max={(today + timedelta(days=MAX_AHEAD_DAYS)).isoformat()}') \
                    .classes('w-full')
                felter['to'] = ui.input('Senest', value=slut.isoformat()) \
                    .props('outlined dense type=date '
                           f'min={today.isoformat()} '
                           f'max={(today + timedelta(days=MAX_AHEAD_DAYS)).isoformat()}') \
                    .classes('w-full')
            ui.label(f'Prognosen rækker {MAX_FORECAST_DAYS} døgn frem — til og '
                     f'med {day(today + timedelta(days=MAX_FORECAST_DAYS - 1), short=False)}. '
                     f'Ligger dit vindue længere ude, venter vagten, til '
                     f'prognosen når derhen.') \
                .classes('text-[11px] text-[var(--txt-3)] leading-snug mt-1.5 '
                         'block')

            ui.label(t('Hvor godt skal det være?')) \
                .classes('text-[11.5px] text-[var(--txt-3)] mt-5 mb-1 block')
            felter['quality'] = ui.toggle(
                {'god': 'Kun gode forhold', 'ok': 'Også skærpede'},
                value='god').props('no-caps unelevated dense spread') \
                .classes('w-full')
            ui.label(f'Målt mod dine egne grænser: {s.limits.max_wind:.0f} knob '
                     f'og {s.limits.max_wave:.1f} meter, sejldøgn '
                     f'{s.limits.day_start:02d}–{s.limits.day_end:02d}. '
                     f'Vi skriver kun, hvis du også kan komme hjem igen.') \
                .classes('text-[11px] text-[var(--txt-3)] leading-snug mt-1.5 '
                         'block')

            if not settings.storage_is_durable:
                ui.html('<div class="chip chip--warn mt-4">Serveren har ikke '
                        'et fast lager endnu — vagten forsvinder, hvis '
                        'Sejlplan bliver opdateret.</div>')

            ui.html('<div class="hairline mt-5 mb-3"></div>')
            ui.label('Vi bruger din adresse til denne ene besked og sletter '
                     'vagten bagefter. Du kan stoppe den når som helst med '
                     'linket i mailen.') \
                .classes('text-[11px] text-[var(--txt-3)] leading-snug block')

        with ui.row().classes('w-full items-center gap-2 px-5 py-3.5 border-t '
                              'border-[var(--line)] no-wrap'):
            ui.element('div').classes('flex-1')
            ui.button(t('Fortryd'), on_click=dlg.close) \
                .props('flat no-caps').classes('text-[var(--txt-2)]')
            ui.button(t('Hold øje'), icon='notifications_active',
                      on_click=lambda: _save(s, felter, dlg)) \
                .props('unelevated no-caps').classes('btn-primary px-4')

    dlg.open()


async def _save(s, felter: dict, dlg) -> None:
    email = (felter['email'].value or '').strip()
    if '@' not in email or '.' not in email.split('@')[-1]:
        ui.notify('Skriv en mailadresse, vi kan skrive til',
                  type='warning', position='bottom')
        return

    try:
        a = date.fromisoformat(felter['from'].value)
        b = date.fromisoformat(felter['to'].value)
    except (TypeError, ValueError):
        ui.notify('Vælg to datoer', type='warning', position='bottom')
        return
    if b < a:
        a, b = b, a
    if b < date.today():
        ui.notify('Vinduet ligger i fortiden', type='warning', position='bottom')
        return

    lim = s.limits
    w = watch.create(
        email=email, name=felter['name'].value or '',
        waypoints=[p.as_dict() for p in s.waypoints],
        boat={'boat_id': s.boat_id, 'custom': s.custom},
        limits={'max_wind': lim.max_wind, 'max_wave': lim.max_wave,
                'day_start': lim.day_start, 'day_end': lim.day_end,
                'night_ok': lim.night_ok, 'use_motor': lim.use_motor},
        date_from=a.isoformat(), date_to=b.isoformat(),
        quality=felter['quality'].value or 'god')

    dlg.close()
    if await lookout.confirm_mail(w):
        ui.notify(f'Vi har skrevet til {email}. Bekræft i mailen, '
                  f'så går vagten i gang.',
                  type='positive', position='bottom', multi_line=True,
                  timeout=9000, classes='max-w-[380px]')
    else:
        watch.cancel(w.id)
        ui.notify('Mailen kunne ikke sendes. Prøv igen om lidt.',
                  type='negative', position='bottom')


def _not_ready() -> None:
    """Sig hvad der mangler, i stedet for at lade knappen være død."""
    with ui.dialog() as dlg, ui.card().classes(
            'w-full max-w-[420px] p-0 bg-[var(--sea-1)] rounded-[var(--r)]'):
        with ui.element('div').classes('px-5 pt-5 pb-3'):
            ui.label('Vejrvagt er ikke slået til').classes(
                'text-[16px] font-bold block')
            ui.label('Serveren har ingen postkasse at skrive fra endnu. Når '
                     'den har, kan du bede Sejlplan holde øje med vejret til '
                     'en tur og skrive, når der er et vindue.') \
                .classes('text-[13px] text-[var(--txt-2)] leading-snug mt-1 '
                         'block')
        with ui.row().classes('w-full items-center px-5 pb-4 no-wrap'):
            ui.element('div').classes('flex-1')
            ui.button(t('Luk'), on_click=dlg.close) \
                .props('flat no-caps').classes('text-[var(--txt-2)]')
    dlg.open()
