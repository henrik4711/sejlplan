"""Oversigten over de både, der er synlige lige nu.

Kortet er godt til at vise, *hvor* nogen er. Det er dårligt til at svare på
"hvem er der overhovedet". En båd er en lille trekant, og zoomer man ud, så
hele farvandet er med, kan man ikke se dem — og zoomer man ind, ser man kun
dem, der tilfældigvis er inden for skærmen.

Så det her er listen. Dem, der ligger i en havn, står under havnens navn —
for det er dét, man vil vide, når man leder efter nogen at drikke kaffe med.
Resten står under Undervejs, med afstand og pejling, for dér er det den
oplysning, der betyder noget.
"""
from __future__ import annotations

from nicegui import ui

from .. import chat, fleetmap
from ..i18n import t
from ..sailing import bearing, compass
from . import fleet as fleetui
from . import talk


def available() -> bool:
    return fleetmap.available()


def dialog(planner) -> None:
    """Hele oversigten. Åbnes fra linjen om flåden og fra kortet."""
    # Dialogen skal høre til fladen, ikke til dét, man kom fra — ellers
    # forsvinder den sammen med den dialog, der lukkede. Samme fælde som
    # tidsmåleren og samtalerne.
    with planner.client.content:
        _byg(planner)


def _byg(planner) -> None:
    mine = fleetui.mark()
    både = list(planner.fleet)
    grupper, undervejs = fleetmap.by_harbour(både)
    ulæst = _ulæste(mine)

    with ui.dialog() as dlg, ui.card().classes(
            'w-full max-w-[460px] p-0 bg-[var(--sea-1)] rounded-[var(--r)]'):

        with ui.row().classes('w-full items-center px-5 py-3.5 border-b '
                              'border-[var(--line)] no-wrap'):
            ui.icon('groups').classes('text-[20px] text-[var(--accent)]')
            ui.label(t('Både i nærheden')).classes(
                'text-[16px] font-bold flex-1')
            ui.button(icon='close', on_click=dlg.close) \
                .props('flat round dense')

        with ui.element('div').classes('scroll-y px-5 py-4 max-h-[64dvh] w-full'):
            if not både:
                _tomt(planner)
            else:
                for havn, hold in grupper:
                    _gruppe(planner, dlg, havn.name, hold, ulæst,
                            detalje=havn.detail)
                if undervejs:
                    _gruppe(planner, dlg, t('Undervejs'), undervejs, ulæst)

        with ui.row().classes('w-full items-center px-5 pb-4 no-wrap'):
            ui.label(t('Du ser kun både, der også har gjort sig synlige.')) \
                .classes('text-[10.5px] text-[var(--txt-3)] leading-snug '
                         'flex-1')
            ui.button(t('Luk'), on_click=dlg.close) \
                .props('flat no-caps').classes('text-[var(--txt-2)] shrink-0')

    dlg.open()


def _ulæste(mine: str) -> set[str]:
    """Mærkerne på de både, der har skrevet og venter på svar."""
    if not chat.available() or not mine:
        return set()
    try:
        return {m.from_mark for m in chat.inbox(mine) if not m.seen}
    except Exception:
        return set()


def _tomt(planner) -> None:
    with ui.element('div').classes('empty py-6'):
        ui.icon('sailing').classes(
            'text-[36px] text-[var(--accent)] opacity-40 mb-2')
        if not planner.last_pos:
            ui.label(t('Vi ved ikke, hvor du er endnu')).classes('empty-title')
            ui.label(t('Uden en position kan vi ikke sige, hvem der er i '
                       'nærheden. Sig ja til position, hvis browseren '
                       'spørger.')).classes('empty-sub')
            return
        ui.label(t('Ingen andre både i nærheden')).classes('empty-title')
        ui.label(t('Der er ingen inden for tres sømil, der har gjort sig '
                   'synlig lige nu.')).classes('empty-sub')


def _gruppe(planner, dlg, titel: str, hold: list, ulæst: set,
            detalje: str = '') -> None:
    with ui.element('div').classes('flex items-baseline gap-2 mb-1.5 mt-1'):
        ui.html(f'<span class="section-label">{_ren(titel)}</span>')
        ui.html('<span class="text-[11px] text-[var(--txt-3)]">'
                f'{_ren(_antal(len(hold)))}</span>')
    if detalje:
        ui.label(detalje).classes(
            'text-[10.5px] text-[var(--txt-3)] -mt-1 mb-1.5 block')
    for b in hold:
        _række(planner, dlg, b, b.mark in ulæst)


def _antal(n: int) -> str:
    from ..i18n import plural
    return plural(n, 'båd', 'både')


def _række(planner, dlg, b, venter: bool) -> None:
    row = ui.element('div').classes(
        'card px-3.5 py-2.5 mb-2 flex items-center gap-3 cursor-pointer '
        'hover:border-[var(--line-2)]'
        + (' border-[var(--accent)]' if venter else ''))
    with row:
        ui.icon('sailing').classes(
            'text-[17px] shrink-0 '
            + ('text-[var(--accent)]' if venter else 'text-[var(--txt-3)]'))
        with ui.element('div').classes('min-w-0 flex-1'):
            ui.label(b.name or t('Båd')).classes(
                'text-[13px] font-semibold truncate block')
            ui.label(_hvor(planner, b)).classes(
                'text-[11px] text-[var(--txt-3)] truncate block')
        if venter:
            ui.html('<span class="chip chip--go">'
                    f'{_ren(t("har skrevet"))}</span>')
        ui.icon('chat_bubble_outline').classes(
            'text-[16px] text-[var(--txt-3)] shrink-0')
    if talk.available():
        row.on('click', lambda _, m=b.mark, n=b.name: (
            dlg.close(), talk.open_with(planner, m, n or t('Båd'))))


def _hvor(planner, b) -> str:
    """Afstand, pejling og alder — den ene linje, der siger noget."""
    dele = []
    her = planner.last_pos
    if her:
        nm = fleetmap.distance_nm(her[0], her[1], b.lat, b.lon)
        retning = compass(bearing(her[0], her[1], b.lat, b.lon))
        dele.append(t('{sm} sm mod {retning}',
                      sm=f'{nm:.1f}'.replace('.', ','), retning=retning))
    dele.append(b.age)
    return ' · '.join(dele)


def _ren(s: str) -> str:
    return (s or '').replace('<', '').replace('>', '')
