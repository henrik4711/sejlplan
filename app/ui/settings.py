"""Indstillingsdialog: båd, komfortgrænser og sejldøgn.

Alt herinde har brugbare standardværdier, så man kan planlægge en hel tur uden
nogensinde at åbne dialogen. Den er til dem, der vil skrue på det.

Bådvalget er delt i sejlbåde og motorbåde, fordi de to slags både planlægges
efter hver sin ting: vinden og søen. Valget trækker komfortgrænserne med sig —
en planende daycruiser skal ikke have samme bølgegrænse som en langturssejler.
"""
from __future__ import annotations

from datetime import date, timedelta

from nicegui import ui

from ..boats import MOTORBOATS, SAILBOATS
from .myboat import own_boat_block
from ..dates import day
from .. import i18n
from ..state import MAX_FORECAST_DAYS
from ..i18n import t


def settings_dialog(planner) -> None:
    """Åbn indstillingerne. Ændringer slår igennem, når dialogen lukkes."""
    s = planner.s
    lim = s.limits
    before = _snapshot(s)

    with ui.dialog() as dialog, ui.card().classes(
            'w-full max-w-[560px] p-0 bg-[var(--sea-1)] rounded-[var(--r)]'):

        # ── Titel ──
        with ui.row().classes('w-full items-center px-5 py-3.5 border-b '
                              'border-[var(--line)] no-wrap'):
            ui.icon('tune').classes('text-[20px] text-[var(--accent)]')
            ui.label(t('Indstillinger')).classes('text-[16px] font-bold flex-1')
            ui.button(icon='close', on_click=dialog.close).props('flat round dense')

        with ui.element('div').classes('scroll-y px-5 py-4 max-h-[72dvh] w-full'):

            # ── Båd ──
            @ui.refreshable
            def boat_block() -> None:
                # `limits_block` findes først længere nede i funktionen her.
                # `boat_block()` kaldes før da, så en direkte henvisning til
                # `limits_block.refresh` blev slået op med det samme og kastede
                # NameError — hele indstillingsdialogen kunne ikke åbnes. En
                # lambda venter med opslaget, til brugeren rent faktisk trykker.
                own_boat_block(s, boat_block.refresh,
                               lambda: limits_block.refresh())
                ui.html('<span class="section-label">Eller et eksempel</span>')
                ui.label('Vælg den, der ligner din mest, hvis du ikke vil taste '
                         'din egen ind.')                     .classes('text-[11px] text-[var(--txt-3)] mt-1 mb-2 block')
                for title, boats, note in (
                        (t('Sejlbåde'), SAILBOATS, 'Farten kommer fra polardiagrammet.'),
                        (t('Motorbåde'), MOTORBOATS,
                         'Farten er marchfarten, minus det søen tager.')):
                    with ui.element('div').classes('flex items-baseline gap-2 mb-2 mt-1'):
                        ui.html(f'<span class="section-label">{title}</span>')
                        ui.html(f'<span class="text-[11px] text-[var(--txt-3)]">{note}</span>')
                    with ui.element('div').classes('grid grid-cols-2 gap-2 mb-3'):
                        for boat in boats:
                            _boat_card(boat, boat.id == s.boat_id,
                                       lambda b=boat.id: _pick_boat(b))

            def _pick_boat(boat_id: str) -> None:
                s.set_boat(boat_id)
                boat_block.refresh()
                limits_block.refresh()

            boat_block()

            # ── Komfortgrænser ──
            ui.label(t('Komfortgrænser')).classes('section-label mb-1 block')
            ui.label('Over disse værdier markeres timerne som skærpede, '
                     'og et stykke over dem som frarådede. Bølgehøjden vejes efter '
                     'hvor søen kommer fra — modsø tæller hårdere end medsø.') \
                .classes('text-[11.5px] text-[var(--txt-3)] mb-3 block leading-snug')

            @ui.refreshable
            def limits_block() -> None:
                _slider_row(t('Højeste vind'), lim.max_wind, 5, 40, 1, 'kn',
                            lambda v: setattr(lim, 'max_wind', v))
                _slider_row(t('Højeste bølger'), lim.max_wave, 0.3, 4.0, 0.1, 'm',
                            lambda v: setattr(lim, 'max_wave', v), decimals=1)

            limits_block()

            # ── Datoer ──
            ui.label(t('Hvornår kan du afgå')).classes('section-label mt-5 mb-2 block')

            today = date.today()
            horizon = today + timedelta(days=MAX_FORECAST_DAYS - 1)

            with ui.element('div').classes('grid grid-cols-2 gap-3 mb-1'):
                _date_field(t('Tidligst afgang'), lim.date_from, today, horizon,
                            lambda v: _set_from(v))
                _date_field(t('Senest afgang'), lim.date_to, today, horizon,
                            lambda v: _set_to(v))

            def _set_from(value: str) -> None:
                lim.date_from = value
                if lim.date_to < lim.date_from:
                    lim.date_to = lim.date_from

            def _set_to(value: str) -> None:
                lim.date_to = value
                if lim.date_from > lim.date_to:
                    lim.date_from = lim.date_to

            ui.label(f'Vejrudsigten rækker til og med {day(horizon, short=False)}.') \
                .classes('text-[11px] text-[var(--txt-3)] mb-4 block')

            # ── Sejldøgn ──
            ui.label(t('Sejldøgn')).classes('section-label mt-5 mb-1 block')
            ui.label('Det tidsrum, du vil ligge og sejle i. Slutklokkeslættet er '
                     'ikke et ønske om at afgå senest da — det er hvornår du vil '
                     'ligge fortøjet. Rækker turen ikke, deler planlæggeren den og '
                     'finder en havn undervejs at overnatte i.') \
                .classes('text-[11.5px] text-[var(--txt-3)] mb-3 block leading-snug')

            @ui.refreshable
            def day_block() -> None:
                _slider_row('Tidligst ud af havn', lim.day_start, 0, 12, 1, ':00',
                            lambda v: _set_day('day_start', int(v)), decimals=0)
                _slider_row('Senest i havn igen', lim.day_end, 8, 23, 1, ':00',
                            lambda v: _set_day('day_end', int(v)), decimals=0)
                ui.label(f'Det giver {lim.day_hours} timers sejlads i døgnet.') \
                    .classes('text-[11px] text-[var(--txt-3)] -mt-1 mb-2 block')

            def _set_day(field: str, value: int) -> None:
                setattr(lim, field, value)
                if lim.day_start >= lim.day_end:
                    if field == 'day_start':
                        lim.day_end = min(23, value + 1)
                    else:
                        lim.day_start = max(0, value - 1)

            day_block()

            # ── Til- og fravalg ──
            ui.label(t('Sejlads')).classes('section-label mt-5 mb-2 block')
            _switch_row(t('Sejl også om natten'), lim.night_ok,
                        'Slået til lægges der ingen overnatninger ind — turen '
                        'sejles i ét stræk, og mørketimerne tælles for sig.',
                        lambda v: setattr(lim, 'night_ok', v))
            _switch_row(t('Brug motor i svag vind'), lim.use_motor,
                        'Under 3 knobs fart tændes motoren i beregningen.',
                        lambda v: setattr(lim, 'use_motor', v))

            # ── Appen ──
            _app_block()

        # ── Bund ──
        with ui.row().classes('w-full items-center gap-2 px-5 py-3.5 border-t '
                              'border-[var(--line)] no-wrap'):
            ui.button(t('Nulstil'), icon='restart_alt',
                      on_click=lambda: _reset(planner, dialog)) \
                .props('flat no-caps dense').classes('text-[var(--txt-3)]')
            ui.element('div').classes('flex-1')
            ui.button(t('Færdig'), on_click=dialog.close) \
                .props('unelevated no-caps') \
                .classes('btn-primary px-5')

    def _closed() -> None:
        if _snapshot(s) != before:
            # Grænserne indgår direkte i beregningen, så gamle resultater ryger.
            s.invalidate()
            s.persist()
        planner.refresh()

    dialog.on('hide', lambda _: _closed())
    dialog.open()


def _snapshot(s) -> tuple:
    lim = s.limits
    return (s.boat_id, tuple(sorted((k, str(v)) for k, v in s.custom.items())),
            lim.max_wind, lim.max_wave, lim.date_from, lim.date_to,
            lim.day_start, lim.day_end, lim.night_ok, lim.use_motor)


def _reset(planner, dialog) -> None:
    from ..state import default_limits
    planner.s.limits = default_limits()
    planner.s.set_boat('jeanneau')
    dialog.close()
    ui.notify('Indstillingerne er sat tilbage til standard', position='bottom')


# ── Byggeklodser ──────────────────────────────────────────────────────────────
def _boat_card(boat, chosen: bool, on_pick) -> None:
    card = ui.element('div').classes(
        'card px-3 py-2.5 cursor-pointer transition-all '
        + ('ring-1 ring-[var(--accent)] border-[var(--accent)]'
           if chosen else 'hover:border-[var(--line-2)]'))
    with card:
        with ui.row().classes('items-center gap-2 no-wrap'):
            ui.icon(boat.icon).classes(
                'text-[19px] ' + ('text-[var(--accent)]' if chosen
                                  else 'text-[var(--txt-3)]'))
            ui.label(boat.name).classes('text-[13px] font-semibold truncate')
        ui.label(boat.summary).classes(
            'text-[11px] text-[var(--txt-3)] mt-0.5 truncate block')
        ui.label(boat.crew_note or boat.desc).classes(
            'text-[11px] text-[var(--txt-3)] italic truncate block')
    card.on('click', lambda _: on_pick())


def _slider_row(label: str, value: float, lo: float, hi: float, step: float,
                unit: str, on_set, decimals: int = 0) -> None:
    with ui.element('div').classes('mb-3'):
        with ui.row().classes('items-baseline justify-between no-wrap mb-0.5'):
            ui.label(label).classes('text-[13px] font-medium')
            readout = ui.label(_fmt(value, unit, decimals)) \
                .classes('text-[13px] font-bold tnum text-[var(--accent)]')

        def handle(e) -> None:
            on_set(float(e.value))
            readout.text = _fmt(float(e.value), unit, decimals)

        ui.slider(min=lo, max=hi, step=step, value=value, on_change=handle) \
            .props('label-always=false dense color=amber').classes('w-full')


def _fmt(value: float, unit: str, decimals: int) -> str:
    number = f'{value:.{decimals}f}'
    return f'{number}{unit}' if unit.startswith(':') else f'{number} {unit}'


def _pretty(iso: str) -> str:
    """Datoen som man siger den, ikke som maskinen gemmer den."""
    try:
        return day(date.fromisoformat(iso), short=False)
    except (TypeError, ValueError):
        return iso


def _date_field(label: str, value: str, lo: date, hi: date, on_set) -> None:
    with ui.element('div'):
        ui.label(label).classes('text-[11.5px] text-[var(--txt-3)] mb-1 block')
        field = ui.input(value=_pretty(value)).props('outlined dense readonly '
                                                     'input-class="text-[13px] cursor-pointer"') \
            .classes('w-full')
        with field:
            with ui.menu().props('no-parent-event') as menu:
                picker = ui.date(value=value) \
                    .props(f'minimal :options="d => d >= \'{lo.isoformat().replace("-", "/")}\' '
                           f'&& d <= \'{hi.isoformat().replace("-", "/")}\'"')

                def handle(e) -> None:
                    if not e.value:
                        return
                    field.value = _pretty(e.value)
                    on_set(e.value)
                    menu.close()

                picker.on_value_change(handle)
            with field.add_slot('append'):
                ui.icon('event').classes('cursor-pointer text-[18px] text-[var(--txt-3)]') \
                    .on('click', menu.open)
        field.on('click', menu.open)


def _language_row() -> None:
    """Vælg sprog. Fladen tegnes om med det samme, så man kan se det virke."""
    def choose(code: str) -> None:
        i18n.set_lang(code)
        # Sproget sidder i hver eneste tekst på siden. Der er ikke noget at
        # opdatere delvist — siden hentes forfra.
        ui.navigate.reload()

    with ui.element('div').classes('grid grid-cols-2 gap-2'):
        for code, (name, flag) in i18n.LANGUAGES.items():
            valgt = code == i18n.lang()
            card = ui.element('div').classes(
                'card px-3 py-2.5 flex items-center gap-2.5 cursor-pointer '
                'transition-all '
                + ('ring-1 ring-[var(--accent)] border-[var(--accent)]'
                   if valgt else 'hover:border-[var(--line-2)]'))
            with card:
                ui.label(flag).classes('text-[18px] shrink-0')
                ui.label(name).classes('text-[13px] font-medium flex-1')
                if valgt:
                    ui.icon('check').classes(
                        'text-[16px] text-[var(--accent)] shrink-0')
            card.on('click', lambda _, c=code: choose(c))


def _app_block() -> None:
    """Læg Sejlplan på hjemmeskærmen — og fortæl, hvad den så kan uden dækning.

    Browseren viser selv et tilbud på Android, men aldrig på iPhone og sjældent
    på skrivebordet. Uden en synlig vej herind er det kun dem, der ved det i
    forvejen, der får appen.
    """
    ui.label(t('Sprog')).classes('section-label mt-5 mb-2 block')
    _language_row()

    ui.label(t('Appen')).classes('section-label mt-5 mb-2 block')
    with ui.element('div').classes('card px-3.5 py-3'):
        with ui.row().classes('items-center no-wrap gap-3 w-full'):
            ui.icon('install_mobile').classes('text-[20px] text-[var(--accent)] shrink-0')
            with ui.element('div').classes('flex-1 min-w-0'):
                ui.label(t('Læg på hjemmeskærmen')) \
                    .classes('text-[13px] font-medium block')
                ui.label('Så åbner Sejlplan i sit eget vindue — og den seneste '
                         'sejlplan kan læses uden dækning.') \
                    .classes('text-[11px] text-[var(--txt-3)] leading-snug block')
            ui.button(t('Installér'), on_click=_install) \
                .props('outline dense no-caps') \
                .classes('shrink-0 text-[var(--accent)]')


async def _install() -> None:
    """Tag browserens eget tilbud, hvis der er et. Ellers sig hvad man gør."""
    try:
        besked = await ui.run_javascript(_INSTALL_JS, timeout=15.0)
    except Exception:
        besked = 'Browseren kunne ikke installere appen herfra.'
    if besked:
        ui.notify(besked, position='bottom', multi_line=True,
                  classes='max-w-[340px]')


# Chrome gemmer sit tilbud i `window.sejlplanInstall`, når siden må installeres.
# Safari har intet tilbud at give — dér skal brugeren selv gøre det, og så er
# den eneste hjælp at sige præcis hvordan.
_INSTALL_JS = """
if (window.sejlplanInstall) {
  window.sejlplanInstall.prompt();
  await window.sejlplanInstall.userChoice;
  window.sejlplanInstall = null;
  return '';
}
if (window.matchMedia('(display-mode: standalone)').matches
    || window.navigator.standalone === true) {
  return 'Sejlplan kører allerede som app.';
}
if (/iPhone|iPad|iPod/.test(navigator.userAgent)) {
  return 'Tryk på Del nederst i Safari, og vælg "Føj til hjemmeskærm".';
}
return 'Åbn browserens menu og vælg "Installér Sejlplan" eller '
     + '"Føj til hjemmeskærm".';
"""


def _switch_row(label: str, value: bool, hint: str, on_set) -> None:
    with ui.row().classes('items-center no-wrap gap-3 mb-2.5 w-full'):
        with ui.element('div').classes('flex-1 min-w-0'):
            ui.label(label).classes('text-[13px] font-medium')
            ui.label(hint).classes('text-[11px] text-[var(--txt-3)] leading-snug')
        ui.switch(value=value, on_change=lambda e: on_set(bool(e.value))) \
            .props('dense color=amber')
