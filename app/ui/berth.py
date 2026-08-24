"""Meldinger om plads i havnen — at give dem og at se dem.

Den, der ligger i Marstal klokken to, ved noget, den der kommer klokken seks
ikke kan regne sig frem til. Det tager to sekunder at give videre, og det er
hele designet: tre knapper, ingen konto, ingen indbakke — og ingen fritekst.

Der var et bemærkningsfelt et øjeblik. Det er væk igen, og det var det rigtige:
med det fandtes der ét sted i Sejlplan, hvor én bruger kunne skrive noget, en
anden læste. Så snart det sted findes, skal nogen kunne anmelde, og nogen skal
moderere. Uden feltet findes problemet ikke.

Meldingerne vises, hvor havnene i forvejen står — i listen over havne undervejs
og ved overnatningerne i planen. Alderen står altid med, for den er halvdelen af
oplysningen: "fuld" for tre timer siden er noget andet end "fuld" i går aftes.
"""
from __future__ import annotations

from nicegui import app, ui

from .. import reports
from ..config import settings
from ..i18n import t

# Browserens eget mærke. Ikke en konto — kun nok til at man kan slette sin egen
# melding, og til at holde igen med hvor mange, én browser kan give.
MARK_KEY = 'sejlplan_melder'


def author_id() -> str:
    """Hvem der melder, set fra serveren: en tilfældig streng i sessionen."""
    try:
        mark = app.storage.user.get(MARK_KEY)
        if not mark:
            import secrets
            mark = secrets.token_urlsafe(12)
            app.storage.user[MARK_KEY] = mark
        return str(mark)
    except (RuntimeError, KeyError):
        return ''


def available() -> bool:
    """Meldinger kræver et sted at ligge. Uden lager, ingen meldinger."""
    return bool(settings.storage_dir)


def badge(rep) -> None:
    """Den lille mærkat med den nyeste melding."""
    if rep is None:
        return
    ui.html(
        f'<span class="chip" style="color:{rep.tone};border-color:{rep.tone}33">'
        f'<span class="material-icons chip-ico">{rep.icon}</span>'
        f'{rep.label} · {rep.age}</span>')


def line(rep) -> None:
    """Meldingen som en linje med bemærkning, hvis der er en."""
    if rep is None:
        return
    with ui.element('div').classes('flex items-start gap-2 mt-1'):
        ui.icon(rep.icon).style(f'color: {rep.tone}') \
            .classes('text-[16px] shrink-0 mt-0.5')
        with ui.element('div').classes('min-w-0'):
            ui.label(f'{rep.label} — meldt {rep.age}').classes(
                'text-[12px] block').style(f'color: {rep.tone}')


def button(harbour, on_done=None, small: bool = True) -> None:
    """Knappen, der åbner meldingen. Kun hvis der er noget at melde til."""
    if not available():
        return
    btn = ui.button(t('Meld plads'), icon='campaign',
                    on_click=lambda: dialog(harbour, on_done)) \
        .props(f'flat dense no-caps{" size=sm" if small else ""}') \
        .classes('text-[var(--accent)] shrink-0')
    # Rækken under lægger havnen ind i ruten. En melding skal ikke også gøre
    # det — første gang det blev prøvet, åbnede den "hvor skal havnen ligge".
    btn.on('click.stop', lambda _: None)


def nearby_dialog(planner) -> None:
    """Meld plads i en havn — den, du ligger i, eller en du søger frem.

    Ligger man i Marstal, er det Marstal, man ved noget om. Den behøver ikke at
    stå på den rute, man har lagt. Så vi viser havnene omkring positionen med
    den nærmeste øverst, for det er næsten altid den, man ligger i.

    Og der er en søgning. Uden den kunne man kun melde om de tolv nærmeste, og
    ligger man hjemme ved computeren og vil fortælle om havnen, man lige er
    kommet fra, var der ingen vej ind. Det er ikke en kant — det er den
    almindelige måde at bruge det på.
    """
    from .. import harbours as havne

    here = planner.last_pos
    if not here:
        # Uden position tages rutens sidste punkt — man planlægger tit hjemme,
        # og så er det destinationen, man ville melde om.
        wps = planner.s.waypoints
        here = (wps[-1].lat, wps[-1].lon) if wps else None

    with ui.dialog() as dlg, ui.card().classes(
            'w-full max-w-[460px] p-0 bg-[var(--sea-1)] rounded-[var(--r)]'):

        with ui.element('div').classes('px-5 pt-5 pb-1'):
            ui.label(t('Meld plads')).classes('text-[16px] font-bold block')
            ui.label(t('Søg havnen frem, eller vælg en af dem omkring dig.')) \
                .classes('text-[12.5px] text-[var(--txt-2)] leading-snug '
                         'mt-1 block')

        with ui.element('div').classes('px-5 pt-3'):
            felt = ui.input(placeholder=t('Søg efter en havn…')) \
                .props('outlined dense clearable autocomplete=off '
                       'autofocus').classes('w-full')
            with felt.add_slot('prepend'):
                ui.icon('search').classes('text-[18px] text-[var(--txt-3)]')

        liste = ui.element('div').classes(
            'scroll-y px-5 py-3 max-h-[54dvh] w-full')

        def vis(havneliste, overskrift: str = '') -> None:
            liste.clear()
            with liste:
                if overskrift:
                    ui.label(overskrift).classes(
                        'section-label mb-2 block')
                if not havneliste:
                    ui.label(t('Ingen havne med det navn. Prøv en anden '
                               'stavemåde.')) \
                        .classes('text-[12px] text-[var(--txt-3)] '
                                 'leading-snug block py-2')
                    return
                meldt = reports.recent(
                    [reports.key_of(h.lat, h.lon) for h in havneliste])
                for h in havneliste:
                    v = meldt.get(reports.key_of(h.lat, h.lon))
                    row = ui.element('div').classes(
                        'card px-3.5 py-2.5 mb-2 flex items-center gap-3 '
                        'cursor-pointer hover:border-[var(--line-2)]')
                    with row:
                        ui.icon('anchor').classes(
                            'text-[17px] text-[var(--txt-3)] shrink-0')
                        with ui.element('div').classes('min-w-0 flex-1'):
                            ui.label(h.name).classes(
                                'text-[13px] font-medium truncate block')
                            ui.label(h.detail).classes(
                                'text-[11px] text-[var(--txt-3)] truncate '
                                'block')
                        if v is not None:
                            ui.icon(v.icon).style(f'color: {v.tone}') \
                                .classes('text-[17px] shrink-0')
                        ui.icon('chevron_right').classes(
                            'text-[17px] text-[var(--txt-3)] shrink-0')
                    row.on('click', lambda _, x=h: (dlg.close(),
                                                    dialog(x, planner.refresh)))

        def naere() -> None:
            if not here:
                liste.clear()
                with liste:
                    ui.label(t('Vi ved ikke, hvor du er. Søg havnen frem '
                               'foroven — eller slå "Jeg er undervejs" til.')) \
                        .classes('text-[12px] text-[var(--txt-3)] '
                                 'leading-snug block py-2')
                return
            vis(havne.nearest(here[0], here[1], count=12),
                t('Havne omkring dig'))

        def soeg(e) -> None:
            tekst = str(e.value or '').strip()
            if len(tekst) < 2:
                naere()
                return
            vis(havne.search(tekst, limit=12), t('Søgeresultater'))

        felt.on_value_change(soeg)
        naere()

        with ui.row().classes('w-full items-center px-5 pb-4 no-wrap'):
            ui.element('div').classes('flex-1')
            ui.button(t('Fortryd'), on_click=dlg.close) \
                .props('flat no-caps').classes('text-[var(--txt-2)]')

    dlg.open()


def dialog(harbour, on_done=None) -> None:
    """Tre knapper og en valgfri bemærkning. Ikke mere."""
    author = author_id()

    with ui.dialog() as dlg, ui.card().classes(
            'w-full max-w-[420px] p-0 bg-[var(--sea-1)] rounded-[var(--r)]'):

        with ui.element('div').classes('px-5 pt-5 pb-1'):
            ui.label(t('Er der plads?')).classes('text-[16px] font-bold block')
            ui.label(t('{havn} — din melding hjælper den, der kommer i '
                       'eftermiddag. Den står i halvandet døgn og forsvinder '
                       'så af sig selv.', havn=harbour.name)) \
                .classes('text-[12.5px] text-[var(--txt-2)] leading-snug '
                         'mt-1 block')

        with ui.element('div').classes('px-5 pt-4'):
            with ui.element('div').classes('grid grid-cols-3 gap-2'):
                for level, (label, icon, tone) in reports.LEVELS.items():
                    card = ui.element('div').classes(
                        'card px-2 py-3 text-center cursor-pointer '
                        'hover:border-[var(--line-2)] transition-all')
                    with card:
                        ui.icon(icon).style(f'color: {tone}') \
                            .classes('text-[26px] block mx-auto mb-1')
                        ui.label(t(label)).classes(
                            'text-[12px] font-medium block')
                    card.on('click', lambda _, lv=level: _send(
                        harbour, lv, author, dlg, on_done))

            ui.label(t('Meldingen er anonym, og der er ikke andet at '
                       'skrive: kun havnen, svaret og hvornår. Så findes der '
                       'ikke et sted i Sejlplan, hvor nogen kan skrive noget '
                       'til nogen — og dermed heller ikke noget at '
                       'moderere.')) \
                .classes('text-[11px] text-[var(--txt-3)] leading-snug '
                         'mt-3 block')

        with ui.row().classes('w-full items-center px-5 py-4 no-wrap'):
            ui.element('div').classes('flex-1')
            ui.button(t('Fortryd'), on_click=dlg.close) \
                .props('flat no-caps').classes('text-[var(--txt-2)]')

    dlg.open()


def _send(harbour, level: str, author: str, dlg, on_done) -> None:
    rep = reports.add(harbour.lat, harbour.lon, harbour.name, level, author)
    dlg.close()
    if rep is None:
        ui.notify(t('Du har meldt rigeligt i dag. Prøv igen i morgen.'),
                  type='warning', position='bottom')
        return
    ui.notify(t('Tak — {havn} står nu som "{svar}".', havn=harbour.name,
                svar=t(rep.label)),
              type='positive', position='bottom')
    if on_done:
        on_done()
