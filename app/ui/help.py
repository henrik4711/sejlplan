"""Hjælpen i fladen: spørgsmålstegnet og manualen.

Begge dele læser `app.help`. Spørgsmålstegnet står ved siden af dét, det
handler om, og åbner en boble med samme tekst, som står i manualen. Manualen
er ét dokument, der kan hentes og printes — selvstændigt, uden et eneste kald
ud af siden, så den også kan læses i cockpittet.
"""
from __future__ import annotations

from datetime import datetime
from html import escape as esc

from nicegui import ui

from .. import help as helptext


def dot(topic_id: str) -> None:
    """Et lille spørgsmålstegn, der åbner emnet i en boble.

    Det står ved siden af overskriften, ikke som en knap for sig. Den, der
    ved hvad et sejldøgn er, skal ikke forstyrres af det.
    """
    topic = helptext.by_id(topic_id)
    if topic is None:
        return

    with ui.button(icon='help_outline') \
            .props('flat round dense size=xs') \
            .classes('help-dot shrink-0 text-[var(--txt-3)] '
                     'hover:text-[var(--accent)]'):
        with ui.menu().classes('help-bubble'):
            with ui.element('div').classes('px-4 py-3.5 max-w-[330px]'):
                ui.label(topic.title).classes(
                    'text-[13.5px] font-bold block mb-1')
                ui.label(topic.short).classes(
                    'text-[12.5px] text-[var(--txt-2)] leading-snug block mb-2')
                for para in topic.body:
                    ui.label(para).classes(
                        'text-[12px] text-[var(--txt-3)] leading-relaxed '
                        'block mb-1.5 last:mb-0')


def manual_dialog() -> None:
    """Hele manualen i én dialog, med en knap til at hente den."""
    with ui.dialog() as dialog, ui.card().classes(
            'w-full max-w-[620px] p-0 bg-[var(--sea-1)] rounded-[var(--r)]'):

        with ui.row().classes('w-full items-center px-5 py-3.5 border-b '
                              'border-[var(--line)] no-wrap'):
            ui.icon('menu_book').classes('text-[20px] text-[var(--accent)]')
            ui.label('Manual').classes('text-[16px] font-bold flex-1')
            ui.button('Hent', icon='download',
                      on_click=_download) \
                .props('outline dense no-caps').classes('text-[var(--txt-2)]')
            ui.button(icon='close', on_click=dialog.close).props('flat round dense')

        with ui.element('div').classes('scroll-y px-5 py-4 max-h-[72dvh] w-full'):
            ui.label('Sejlplan fra ende til anden. Det samme står i boblerne '
                     'ude i programmet — her er det bare samlet.') \
                .classes('text-[12.5px] text-[var(--txt-2)] leading-snug '
                         'mb-4 block')
            for group, topics in helptext.groups():
                if group:
                    ui.html(f'<span class="section-label">{esc(group)}</span>')
                for t in topics:
                    with ui.element('div').classes('card px-4 py-3.5 mt-2 mb-2'):
                        ui.label(t.title).classes(
                            'text-[14px] font-bold block mb-0.5')
                        ui.label(t.short).classes(
                            'text-[12.5px] text-[var(--accent)] leading-snug '
                            'block mb-2')
                        for para in t.body:
                            ui.label(para).classes(
                                'text-[12.5px] text-[var(--txt-2)] '
                                'leading-relaxed block mb-2 last:mb-0')
            ui.html('<div class="hairline mt-4 mb-3"></div>')
            ui.label(helptext.DISCLAIMER).classes(
                'text-[11.5px] text-[var(--txt-3)] leading-relaxed block')

    dialog.open()


def _download() -> None:
    ui.download.content(document(), 'sejlplan-manual.html')


# ── Manualen som ét selvstændigt dokument ────────────────────────────────────
# Samme princip som offline-planen: ingen skrifter, billeder eller stilark
# hentes udefra. Den skal kunne læses i en havn uden dækning og printes uden
# at falde fra hinanden.
CSS = """
:root { --bg:#fff; --ink:#12212F; --ink2:rgba(18,33,47,.70);
        --ink3:rgba(18,33,47,.48); --line:rgba(13,27,42,.14); --gold:#A8752A; }
@media (prefers-color-scheme: dark) {
  :root { --bg:#0D1B2A; --ink:#F0EDE8; --ink2:rgba(240,237,232,.70);
          --ink3:rgba(240,237,232,.45); --line:rgba(240,237,232,.14);
          --gold:#E8B96A; }
}
* { box-sizing: border-box; }
body { margin:0; padding:0 20px 60px; background:var(--bg); color:var(--ink);
  font:15px/1.6 -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto,
       'Helvetica Neue', Arial, sans-serif; -webkit-text-size-adjust:100%; }
.wrap { max-width:44rem; margin:0 auto; }
header { padding:40px 0 20px; border-bottom:2px solid var(--gold); }
.eyebrow { font-size:11px; font-weight:700; letter-spacing:.10em;
  text-transform:uppercase; color:var(--gold); }
h1 { font-size:30px; margin:8px 0 6px; letter-spacing:-.015em; }
.lead { font-size:14.5px; color:var(--ink2); margin:0; max-width:34em; }
h2 { font-size:11px; font-weight:700; letter-spacing:.10em;
  text-transform:uppercase; color:var(--ink3); margin:34px 0 4px; }
h3 { font-size:17px; margin:20px 0 2px; letter-spacing:-.01em; }
.short { font-size:13.5px; color:var(--gold); margin:0 0 8px; font-weight:600; }
p { margin:0 0 10px; color:var(--ink2); }
footer { margin-top:40px; padding-top:16px; border-top:1px solid var(--line);
  font-size:12px; color:var(--ink3); }
@media print {
  body { padding:0; font-size:11pt; }
  h3 { page-break-after:avoid; } h2 { page-break-after:avoid; }
  footer { page-break-before:avoid; }
}
"""


def document() -> str:
    """Manualen som én fil, der kan stå alene."""
    stamp = datetime.now()
    parts = ['<div class="wrap"><header>'
             '<div class="eyebrow">Manual</div><h1>Sejlplan</h1>'
             '<p class="lead">Find den bedste afgang, og tag sejlplanen med '
             'til søs. Her står, hvad tallene betyder, og hvad du selv skal '
             'tage stilling til.</p></header>']

    for group, topics in helptext.groups():
        if group:
            parts.append(f'<h2>{esc(group)}</h2>')
        for t in topics:
            parts.append(f'<h3>{esc(t.title)}</h3>'
                         f'<p class="short">{esc(t.short)}</p>')
            parts += [f'<p>{esc(para)}</p>' for para in t.body]

    parts.append(f'<footer>{esc(helptext.DISCLAIMER)}<br>'
                 f'Hentet {stamp:%d. %B %Y}.</footer></div>')

    return ('<!doctype html><html lang="da"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<meta name="color-scheme" content="light dark">'
            '<title>Sejlplan — manual</title>'
            f'<style>{CSS}</style></head><body>'
            + ''.join(parts) + '</body></html>')
