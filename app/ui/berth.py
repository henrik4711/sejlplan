"""Meldinger om plads i havnen — at give dem og at se dem.

Den, der ligger i Marstal klokken to, ved noget, den der kommer klokken seks
ikke kan regne sig frem til. Det tager to sekunder at give videre, og det er
hele designet: tre knapper, ingen konto, ingen indbakke.

Meldingerne vises, hvor havnene i forvejen står — i listen over havne undervejs
og ved overnatningerne i planen. Alderen står altid med, for den er halvdelen af
oplysningen: "fuld" for tre timer siden er noget andet end "fuld" i går aftes.
"""
from __future__ import annotations

from nicegui import app, ui

from .. import reports
from ..config import settings

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
            if rep.note:
                ui.label(f'”{rep.note}”').classes(
                    'text-[11.5px] text-[var(--txt-3)] leading-snug block')


def button(harbour, on_done=None, small: bool = True) -> None:
    """Knappen, der åbner meldingen. Kun hvis der er noget at melde til."""
    if not available():
        return
    btn = ui.button('Meld plads', icon='campaign',
                    on_click=lambda: dialog(harbour, on_done)) \
        .props(f'flat dense no-caps{" size=sm" if small else ""}') \
        .classes('text-[var(--accent)] shrink-0')
    # Rækken under lægger havnen ind i ruten. En melding skal ikke også gøre
    # det — første gang det blev prøvet, åbnede den "hvor skal havnen ligge".
    btn.on('click.stop', lambda _: None)


def dialog(harbour, on_done=None) -> None:
    """Tre knapper og en valgfri bemærkning. Ikke mere."""
    author = author_id()
    note = {'text': ''}

    with ui.dialog() as dlg, ui.card().classes(
            'w-full max-w-[420px] p-0 bg-[var(--sea-1)] rounded-[var(--r)]'):

        with ui.element('div').classes('px-5 pt-5 pb-1'):
            ui.label('Er der plads?').classes('text-[16px] font-bold block')
            ui.label(f'{harbour.name} — din melding hjælper den, der kommer '
                     f'i eftermiddag. Den står i halvandet døgn og forsvinder '
                     f'så af sig selv.') \
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
                        ui.label(label).classes(
                            'text-[12px] font-medium block')
                    card.on('click', lambda _, lv=level: _send(
                        harbour, lv, note['text'], author, dlg, on_done))

            field = ui.input(placeholder='Bemærkning (valgfrit) — fx "plads ved '
                                         'ydermolen"') \
                .props(f'outlined dense maxlength={reports.NOTE_MAX}') \
                .classes('w-full mt-3')
            field.on_value_change(lambda e: note.update(text=e.value or ''))

            ui.label('Meldingen er anonym. Vi gemmer hverken navn eller '
                     'position — kun havnen, svaret og hvornår.') \
                .classes('text-[11px] text-[var(--txt-3)] leading-snug '
                         'mt-2 block')

        with ui.row().classes('w-full items-center px-5 py-4 no-wrap'):
            ui.element('div').classes('flex-1')
            ui.button('Fortryd', on_click=dlg.close) \
                .props('flat no-caps').classes('text-[var(--txt-2)]')

    dlg.open()


def _send(harbour, level: str, note: str, author: str, dlg, on_done) -> None:
    rep = reports.add(harbour.lat, harbour.lon, harbour.name, level,
                      note, author)
    dlg.close()
    if rep is None:
        ui.notify('Du har meldt rigeligt i dag. Prøv igen i morgen.',
                  type='warning', position='bottom')
        return
    ui.notify(f'Tak — {harbour.name} står nu som "{rep.label}".',
              type='positive', position='bottom')
    if on_done:
        on_done()
