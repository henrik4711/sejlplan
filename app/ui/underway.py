"""Undervejs: hvor er jeg i forhold til planen?

Telefonen ved, hvor båden er. Det er det eneste, der skal til for at svare på
det spørgsmål, man rent faktisk har i cockpittet: er jeg foran eller bagud, og
hvornår er jeg så fremme?

Positionen bliver hos brugeren og den ene beregning på serveren. Den gemmes
ikke, og den sendes ikke til nogen. Der er ingen, der kan se, hvor du er.

Om iPhone: positionen virker i Safari og i appen på hjemmeskærmen, men **kun
mens skærmen er tændt og Sejlplan er fremme**. Låser man telefonen, holder den
op. Det er iOS, der bestemmer det, og det står i fladen, så ingen tror, det er
en fejl.
"""
from __future__ import annotations

from nicegui import ui

from .. import progress
from ..dates import clock

# Positionen hentes ikke oftere end det. Oftere koster batteri uden at sige
# noget nyt — en sejlbåd flytter sig ikke meget på et halvt minut.
EVERY_MS = 30_000

WATCH_JS = """
(function () {
  if (!navigator.geolocation) {
    emitEvent('pos-fejl', 'Telefonen giver ikke adgang til position.');
    return;
  }
  if (window.sejlplanWatch != null) return;

  const send = (p) => emitEvent('pos', {
    lat: p.coords.latitude, lon: p.coords.longitude,
    nøjagtighed: p.coords.accuracy,
    fart: p.coords.speed, kurs: p.coords.heading,
  });

  // Ét hurtigt svar først, så der står noget med det samme, og derefter
  // opdateringer. Uden det ser der tomt ud i det halve minut, hvor telefonen
  // leder efter satellitter.
  navigator.geolocation.getCurrentPosition(send, () => {}, {
    enableHighAccuracy: true, timeout: 15000, maximumAge: 30000});

  window.sejlplanWatch = navigator.geolocation.watchPosition(
    send,
    (err) => emitEvent('pos-fejl',
      err.code === 1 ? 'Du har sagt nej til position. Slå det til i '
                     + 'browserens indstillinger for siden.'
                     : 'Kunne ikke finde positionen.'),
    {enableHighAccuracy: true, timeout: 20000, maximumAge: %(age)d});
})();
"""

STOP_JS = """
if (window.sejlplanWatch != null) {
  navigator.geolocation.clearWatch(window.sejlplanWatch);
  window.sejlplanWatch = null;
}
"""


def bar(planner) -> None:
    """Linjen øverst i sejlplanen, når man er undervejs."""
    if not planner.underway:
        with ui.element('div').classes('flex items-center gap-2 mb-4'):
            ui.button('Jeg er undervejs', icon='my_location',
                      on_click=planner.start_underway) \
                .props('outline dense no-caps') \
                .classes('text-[var(--accent)]')
            ui.label('Følg med i, om du er foran eller bagud.') \
                .classes('text-[11.5px] text-[var(--txt-3)] leading-snug')
        return

    p = planner.progress
    with ui.element('div').classes(
            'card px-4 py-3 mb-4 border-[var(--accent)] '
            'bg-[var(--accent-soft)]'):
        with ui.element('div').classes('flex items-center gap-2 mb-1'):
            ui.icon('my_location').classes(
                'text-[17px] text-[var(--accent)] shrink-0')
            ui.label('Undervejs').classes(
                'section-label flex-1')
            ui.button('Stop', on_click=planner.stop_underway) \
                .props('flat dense no-caps size=sm') \
                .classes('text-[var(--txt-3)]')

        if planner.pos_error:
            ui.label(planner.pos_error).classes(
                'text-[12.5px] text-[var(--stop)] leading-snug block')
            return

        if p is None:
            with ui.row().classes('items-center gap-2'):
                ui.spinner(size='16px').classes('text-[var(--accent)]')
                ui.label('Leder efter positionen…').classes(
                    'text-[12.5px] text-[var(--txt-2)]')
            return

        if not p.on_route:
            ui.label(f'Du er {p.off_route_nm:.1f} sømil fra ruten. '
                     f'Så længe det er sådan, kan vi ikke sige, om du er '
                     f'foran eller bagud.'.replace('.', ',', 1)) \
                .classes('text-[12.5px] text-[var(--txt-2)] leading-snug block')
            return

        _numbers(p)


def _numbers(p) -> None:
    if not p.started:
        ui.label('Turen er ikke begyndt endnu — afgangen ligger frem i tiden. '
                 'Når du har kastet los, står der her, om du er foran eller '
                 'bagud.') \
            .classes('text-[12.5px] text-[var(--txt-2)] leading-snug block')
        return

    tone = {'foran': 'var(--go)', 'bagud': 'var(--warn)',
            'som planlagt': 'var(--txt-1)', 'fremme': 'var(--go)',
            'ikke begyndt': 'var(--txt-2)'}[p.verdict]

    if p.arrived:
        ui.label('Du er fremme. God tur — og velkommen i havn.') \
            .classes('text-[13px] block').style(f'color: {tone}')
        return

    minutes = abs(p.ahead_min)
    if p.verdict == 'som planlagt':
        head = 'Du følger planen'
    else:
        head = (f'Du er {minutes:.0f} minutter {p.verdict}'
                if minutes < 90 else
                f'Du er {minutes / 60:.1f} timer {p.verdict}'.replace('.', ','))

    ui.label(head).classes('text-[15px] font-semibold block mb-1') \
        .style(f'color: {tone}')

    dele = [f'{_da(p.along_nm)} sømil sejlet',
            f'{_da(p.remaining_nm)} tilbage',
            f'{_da(p.made_good_kn)} knob i snit']
    ui.label(' · '.join(dele)).classes(
        'text-[12px] text-[var(--txt-2)] tnum block')

    if p.eta:
        ui.label(f'Med den fart er du fremme {clock(p.eta)}.') \
            .classes('text-[12px] text-[var(--txt-3)] block mt-0.5')

    ui.label('Positionen bliver på din telefon. Den gemmes ikke, og ingen '
             'andre kan se den.') \
        .classes('text-[10.5px] text-[var(--txt-3)] leading-snug block mt-2')


def _da(value: float, decimals: int = 1) -> str:
    return f'{value:.{decimals}f}'.replace('.', ',')


def start(planner) -> None:
    """Bed om positionen og begynd at følge med."""
    planner.underway = True
    planner.pos_error = ''
    planner.progress = None
    ui.run_javascript(WATCH_JS % {'age': EVERY_MS})
    planner.plan_view.refresh()


def stop(planner) -> None:
    planner.underway = False
    planner.progress = None
    planner.pos_error = ''
    ui.run_javascript(STOP_JS)
    planner.plan_view.refresh()


def position(planner, lat: float, lon: float) -> None:
    """En ny position er kommet ind. Regn den om til et forspring."""
    planner.pos_error = ''
    planner.progress = progress.where(
        planner.s.route, planner.s.plan, lat, lon)
    planner.plan_view.refresh()
