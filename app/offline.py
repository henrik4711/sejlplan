"""Sejlplanen som ét selvstændigt dokument.

Det her er dét, der ligger tilbage, når dækningen er væk. Sejlplan tegner
fladen på serveren og sender den ned over en websocket, så uden forbindelse er
der ingen flade at vise — men det er heller ikke dét, man har brug for på vandet.
Man skal ikke *lægge* en rute uden dækning. Man skal kunne *læse* den, man
allerede har lagt.

Så dokumentet her skal kunne stå helt alene: al styling ligger indeni, der
hentes hverken skrifter, billeder eller kort udefra. Det bruger telefonens egne
skrifttyper og følger dens lyse eller mørke indstilling, og så er der ikke ét
eneste kald ud af siden. Så kan det lægges i browserens cache og hentes frem
midt i Kattegat.
"""
from __future__ import annotations

from datetime import datetime
from html import escape as esc

from .boats import Boat
from .dates import clock, day_time, full, spell
from .narrative import (day_lines, num, overview, stretch_briefs,
                        warnings)
from .sailing import Limits, Plan, Route, compass, point_of_sail

# Skrifterne er telefonens egne. En webskrift skal hentes, og det er præcis
# dét, der ikke kan lade sig gøre herude.
CSS = """
:root {
  --bg: #F4F1EC; --card: #FFFFFF; --ink: #12212F;
  --ink-2: rgba(18,33,47,.68); --ink-3: rgba(18,33,47,.45);
  --line: rgba(13,27,42,.12); --gold: #A8752A;
  --go: #1E9E52; --warn: #C2751E; --stop: #C93B3B;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #0D1B2A; --card: #16232F; --ink: #F0EDE8;
    --ink-2: rgba(240,237,232,.66); --ink-3: rgba(240,237,232,.40);
    --line: rgba(240,237,232,.12); --gold: #E8B96A;
    --go: #35B96A; --warn: #E9963B; --stop: #E4645C;
  }
}
* { box-sizing: border-box; }
body {
  margin: 0; padding: 0 0 48px;
  background: var(--bg); color: var(--ink);
  font: 15px/1.55 -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto,
        'Helvetica Neue', Arial, sans-serif;
  -webkit-text-size-adjust: 100%;
}
.wrap { max-width: 46rem; margin: 0 auto; padding: 0 20px; }
.tnum { font-variant-numeric: tabular-nums; }

.bar {
  background: var(--gold); color: #12212F;
  font-size: 12.5px; font-weight: 700; letter-spacing: .02em;
  padding: 9px 20px; text-align: center;
}
@media (prefers-color-scheme: dark) { .bar { color: #0D1B2A; } }

header { padding: 26px 0 18px; border-bottom: 1px solid var(--line); }
.eyebrow {
  font-size: 11px; font-weight: 700; letter-spacing: .09em;
  text-transform: uppercase; color: var(--ink-3);
}
h1 { font-size: 21px; line-height: 1.25; margin: 6px 0 8px; letter-spacing: -.01em; }
.sub { font-size: 13.5px; color: var(--ink-2); margin: 0; }

h2 {
  font-size: 11px; font-weight: 700; letter-spacing: .09em;
  text-transform: uppercase; color: var(--ink-3);
  margin: 30px 0 10px;
}
p { margin: 0 0 11px; }

.card {
  background: var(--card); border: 1px solid var(--line);
  border-radius: 14px; padding: 15px 17px; margin-bottom: 10px;
}
.card p:last-child { margin-bottom: 0; }

.keys { display: grid; grid-template-columns: repeat(2, 1fr); gap: 9px; }
@media (min-width: 33rem) { .keys { grid-template-columns: repeat(3, 1fr); } }
.key { background: var(--card); border: 1px solid var(--line);
       border-radius: 12px; padding: 11px 13px; }
.key b { display: block; font-size: 19px; letter-spacing: -.01em; }
.key span { display: block; font-size: 10.5px; letter-spacing: .07em;
            text-transform: uppercase; color: var(--ink-3); margin-top: 2px; }

.warn { border-left: 3px solid var(--warn); }

.day { display: flex; gap: 13px; margin-bottom: 12px; }
.day .n {
  flex: none; width: 25px; height: 25px; border-radius: 50%;
  background: var(--gold); color: #12212F;
  font-size: 12.5px; font-weight: 700;
  display: flex; align-items: center; justify-content: center;
}
@media (prefers-color-scheme: dark) { .day .n { color: #0D1B2A; } }
.day .t { min-width: 0; }
.day .t b { font-size: 14.5px; }
.day .t span { display: block; font-size: 12.5px; color: var(--ink-2); }

.leg { margin-bottom: 15px; }
.leg b { font-size: 14.5px; }
.leg .meta { font-size: 11.5px; color: var(--ink-3); margin: 1px 0 3px; }
.leg p { font-size: 13.5px; color: var(--ink-2); margin: 0; }

.scroll { overflow-x: auto; -webkit-overflow-scrolling: touch; }
table { border-collapse: collapse; width: 100%; font-size: 13px; }
th {
  text-align: left; font-size: 10px; letter-spacing: .07em;
  text-transform: uppercase; color: var(--ink-3);
  padding: 0 10px 6px 0; font-weight: 700; white-space: nowrap;
}
td { padding: 4px 10px 4px 0; border-top: 1px solid var(--line); white-space: nowrap; }
tr.head td { font-weight: 700; padding-top: 14px; border-top: 0; }
.dot { display: inline-block; width: 7px; height: 7px; border-radius: 50%;
       margin-right: 6px; vertical-align: 1px; }

footer { margin-top: 34px; padding-top: 16px; border-top: 1px solid var(--line);
         font-size: 11.5px; color: var(--ink-3); }
"""


def _keys(boat: Boat, plan: Plan) -> list[tuple[str, str]]:
    out = [
        (spell(plan.under_way_h), 'Under vejs'),
        (f'{num(plan.avg_speed_kn)} kn', 'Gns. fart'),
        (f'{num(plan.total_nm, 0)} sm', 'Distance'),
        (f'{num(plan.worst_wind_kn, 0)} kn', 'Højeste vind'),
        (f'{num(plan.worst_wave_m)} m', 'Højeste bølger'),
    ]
    if boat.is_motor or plan.fuel_l >= 1:
        out.append((f'{num(plan.fuel_l, 0)} l', 'Brændstof'))
    else:
        out.append((f'{plan.red_hours} t', 'Frarådet'))
    return out


def document(boat: Boat, route: Route, plan: Plan, limits: Limits,
             saved: datetime | None = None) -> str:
    """Byg hele planen som én HTML-fil uden et eneste kald ud af siden."""
    saved = saved or datetime.now()
    names = ' → '.join(w.name for w in route.waypoints)
    tail = (f'når {plan.reached_nm:.0f} af {plan.total_nm:.0f} sømil'
            if plan.incomplete else f'ankomst {full(plan.arrival)}')

    p: list[str] = []
    add = p.append

    add(f'<div class="bar">Gemt om bord {day_time(saved)} · '
        f'virker uden dækning</div>')
    add('<div class="wrap">')

    add('<header>'
        '<div class="eyebrow">Sejlplan</div>'
        f'<h1>{esc(names)}</h1>'
        f'<p class="sub">{esc(boat.name)} · afgang {esc(full(plan.depart))} '
        f'· {esc(tail)}</p>'
        '</header>')

    add('<h2>Overblik</h2><div class="card">')
    for para in overview(boat, route, plan):
        add(f'<p>{esc(para)}</p>')
    add('</div>')

    notes = warnings(plan, limits, boat)
    if notes:
        add('<h2>Vær opmærksom på</h2>')
        for note in notes:
            add(f'<div class="card warn"><p>{esc(note)}</p></div>')

    add('<h2>Nøgletal</h2><div class="keys">')
    for value, label in _keys(boat, plan):
        add(f'<div class="key"><b class="tnum">{esc(value)}</b>'
            f'<span>{esc(label)}</span></div>')
    add('</div>')

    if len(plan.days) > 1:
        add('<h2>Dag for dag</h2>')
        for i, line in enumerate(day_lines(plan), 1):
            head, _, rest = line.partition(': ')
            add(f'<div class="day"><div class="n">{i}</div><div class="t">'
                f'<b>{esc(head)}</b><span>{esc(rest or line)}</span>'
                f'</div></div>')

    briefs = stretch_briefs(route, plan, boat)
    if briefs:
        add('<h2>Stræk for stræk</h2>')
        for b in briefs:
            add(f'<div class="leg"><b>{esc(b.headline)}</b>'
                f'<div class="meta tnum">{esc(b.heading)} · '
                f'{esc(b.starts)} → {esc(b.ends)}</div>'
                f'<p>{esc(b.sentence)}</p></div>')

    add('<h2>Time for time</h2><div class="scroll"><table>'
        '<tr><th>Tid</th><th>Vind</th><th>Fra</th><th>Bølger</th>'
        '<th>Fart</th><th>Sejlføring</th></tr>')
    seen = None
    for s in plan.segments:
        if s.time.date() != seen:
            seen = s.time.date()
            add(f'<tr class="head"><td colspan="6">{esc(day_time(s.time)[:-6])}'
                f'</td></tr>')
        colour = {'go': 'var(--go)', 'warn': 'var(--warn)'}.get(
            s.status, 'var(--stop)')
        mode = 'motor' if s.motoring else point_of_sail(s.twa)
        add(f'<tr><td class="tnum">'
            f'<span class="dot" style="background:{colour}"></span>'
            f'{esc(clock(s.time))}</td>'
            f'<td class="tnum">{num(s.wind_kn, 0)} kn</td>'
            f'<td>{esc(compass(s.wind_dir))}</td>'
            f'<td class="tnum">{num(s.wave_m)} m</td>'
            f'<td class="tnum">{num(s.speed_kn)} kn</td>'
            f'<td>{esc(mode)}</td></tr>')
    add('</table></div>')

    add('<footer>Prognoser er prognoser. Planen erstatter ikke søkort, '
        'farvandsudsigt eller almindelig sømandskab.<br>'
        f'Hentet {esc(full(saved))} og gemt i telefonen. Åbn Sejlplan med '
        f'dækning for at regne den om.</footer>')
    add('</div>')

    return (
        '<!doctype html><html lang="da"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        '<meta name="color-scheme" content="light dark">'
        f'<title>Sejlplan — {esc(names)}</title>'
        f'<style>{CSS}</style></head><body>'
        + ''.join(p) +
        '</body></html>'
    )
