"""Trimrådet, foldet ind under det stræk, det hører til.

Det står lukket. Den, der har sejlet i tredive år, skal ikke have at vide,
hvor løjgangsvognen hører hjemme — men den, der har haft båden i to somre,
skal kunne finde det uden at lede.
"""
from __future__ import annotations

from html import escape as esc

from nicegui import ui

from .. import trim
from ..i18n import t


def card(brief) -> None:
    """Én sammenfoldet linje under et stræk."""
    if brief.is_motor:
        return
    # Vindstyrken midt i spændet. Bommen står ikke anderledes ved 12 end ved
    # 13 knob, men den gør ved 8 og ved 22 — og det er dét, spændet fanger.
    kn = (brief.wind_min + brief.wind_max) / 2
    råd = trim.advise(brief.twa, kn)
    if råd is None:
        return

    with ui.expansion(t('Optimér mine sejl'), icon='tune') \
            .props('dense dense-toggle') \
            .classes('trim mt-2 w-full'):
        # Tegningen først. Rådet står i ord nedenunder, men "bommen ud til
        # tyve-tredive grader" er en sætning, man kan læse forkert — og her
        # vender den samme vej som virkeligheden, for strækket har en halse.
        tegning(brief.twa, brief.tack)
        _indhold(råd, kn)


def _indhold(råd: trim.Trim, kn: float) -> None:
    ui.label(t('Ved {kn} knob på {sejlføring}. Et udgangspunkt — dine sejl '
               'og deres alder bestemmer resten.',
               kn=f'{kn:.0f}', sejlføring=t(råd.sail))) \
        .classes('text-[11px] text-[var(--txt-3)] leading-snug mb-2 block')

    if råd.warning:
        with ui.element('div').classes(
                'px-3 py-2.5 mb-2 rounded-[9px] flex items-start gap-2.5 '
                'bg-[var(--warn-soft)] border border-[var(--warn)]'):
            ui.icon('warning_amber').classes(
                'text-[17px] text-[var(--warn)] shrink-0 mt-0.5')
            ui.label(t(råd.warning)).classes(
                'text-[12px] leading-snug')

    with ui.element('div').classes('card overflow-hidden'):
        for i, (navn, tekst) in enumerate(råd.rows):
            if i:
                ui.html('<div class="hairline"></div>')
            with ui.element('div').classes(
                    'flex items-start gap-3 px-3 py-2'):
                ui.html(f'<span class="trim-part">{esc(t(navn))}</span>')
                ui.label(t(tekst)).classes(
                    'text-[12px] leading-snug text-[var(--txt-2)] flex-1')

    for ikon, overskrift, tekst in (
            ('visibility', t('Kig efter'), råd.watch),
            ('compress', t('Rebning'), råd.reef)):
        with ui.element('div').classes('flex items-start gap-2.5 mt-2'):
            ui.icon(ikon).classes(
                'text-[15px] text-[var(--accent)] shrink-0 mt-0.5')
            with ui.element('div').classes('min-w-0'):
                ui.label(overskrift).classes(
                    'text-[11px] font-semibold block')
                ui.label(t(tekst)).classes(
                    'text-[11.5px] text-[var(--txt-2)] leading-snug block')


def tegning(twa: float, tack: str = 'styrbords halse') -> None:
    """Sejlføringen set oppefra.

    "Bommen ud til tyve-tredive grader" er en sætning, man kan læse forkert.
    En tegning kan man ikke — og det er dét, der gør, at man ikke står og er
    i tvivl, når man skal skøde ud.
    """
    with ui.element('div').classes(
            'trim-fig flex items-center gap-3 mb-2.5'):
        ui.html(f'<div class="trim-art">{trim.diagram(twa, tack)}</div>')
        with ui.element('div').classes('min-w-0 flex-1'):
            ui.label(t('Set oppefra, stævnen opad.')) \
                .classes('text-[11px] font-semibold block')
            ui.label(t('Den stiplede pil er vinden. Det gyldne er storsejlet, '
                       'det grønne forsejlet.')) \
                .classes('text-[10.5px] text-[var(--txt-3)] leading-snug '
                         'block mt-0.5')
            if twa >= trim.I_VINDØJET:
                ui.label(t('Bommen står omkring {grader}° fra midterlinjen.',
                           grader=f'{trim.boom_angle(twa):.0f}')) \
                    .classes('text-[11px] text-[var(--txt-2)] leading-snug '
                             'block mt-1 tnum')
