"""Hvilke tekster mangler på et andet sprog?

Dansk er kilden, og den danske sætning er nøglen. Prisen for det er, at retter
man en dansk sætning, mister den sin oversættelse i stilhed. Det her værktøj
finder dem, så det ikke sker ubemærket.

Det leder efter kald til `t('…')` i koden og slår hver enkelt op i sprogtabellen.
Er den der ikke, står den danske sætning i stedet ude i programmet — det virker,
men det er ikke oversat.

Kør:  python tools/check_translations.py
      python tools/check_translations.py --liste     (skriv de manglende ud)
      python tools/check_translations.py --skabelon  (klar til at klippe ind)
"""
from __future__ import annotations

import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# Funktionerne, hvis første argument er en tekst, der skal oversættes.
CALLS = {'t', 'plural'}

# Flertalsformerne har ingen dansk sætning at høre til — de er en tysk
# bøjning af et ord, der står i tabellen i forvejen.
PLURAL_MARK = '|flertal'


def _text_args(node: ast.Call) -> list[str]:
    """De tekster, et kald bærer. `plural` har to."""
    out = []
    for arg in node.args:
        if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
            out.append(arg.value)
        elif isinstance(arg, ast.JoinedStr):
            # En f-streng kan ikke slås op — pladsholderne skal stå i teksten
            # som {navn}, ikke være sat ind på forhånd.
            return ['\0F-STRENG: ' + ''.join(
                v.value for v in arg.values
                if isinstance(v, ast.Constant) and isinstance(v.value, str))]
    return out


def strings_in(path: Path) -> list[str]:
    try:
        tree = ast.parse(path.read_text(encoding='utf-8'))
    except (OSError, SyntaxError):
        return []
    out = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        fn = node.func
        name = (fn.id if isinstance(fn, ast.Name)
                else fn.attr if isinstance(fn, ast.Attribute) else '')
        if name in CALLS:
            out += _text_args(node)
    return out


def manual_strings() -> list[str]:
    """Manualens tekster.

    De står som data i `app/help.py` og går først gennem `t()` ude i fladen,
    når siden tegnes. En scanner, der kun leder efter `t('…')`, ser dem ikke —
    og så ville 2600 ord manual tælle som oversat, uden at være det.
    """
    from app import help as helptext
    out = []
    for group, topics in helptext.groups():
        out.append(group)
        for e in topics:
            out += [e.title, e.short, *e.body]
    out.append(helptext.DISCLAIMER)
    out += seamanship_strings()
    return [s.strip() for s in out if s and s.strip()]


def seamanship_strings() -> list[str]:
    """Sømærkerne og signalerne.

    De står som data med tegninger ved siden af, og går gennem `t()` ude i
    fladen. En scanner, der kun leder efter `t('…')`, ser dem ikke.
    """
    from app import seamanship as sm
    ud: list[str] = []
    for m in sm.MARKS:
        ud += [m.name, m.meaning, m.action, m.light, m.memo]
    for _kort, betyder in sm.LIGHTS:
        ud.append(betyder)
    ud += [sm.LIGHT_EXAMPLE[1], sm.SECTORS]
    for gruppe in (sm.LANTERNS, sm.DAY_SHAPES, sm.SOUND_MANOEUVRE,
                   sm.SOUND_FOG, sm.DISTRESS):
        for sig in gruppe:
            ud += [sig.what, sig.means]
    return ud


def trim_strings() -> list[str]:
    """Trimrådene. Samme sag: data, ikke `t()`-kald.

    Alle kombinationer af vinkel og vindstyrke køres igennem, så vi fanger
    hver eneste sætning — også dem, der kun står frem i hård vind på læns.
    """
    from app import trim
    ud: list[str] = []
    for twa in range(0, 181, 5):
        for kn in (4, 10, 16, 22, 30):
            r = trim.advise(twa, kn)
            if r is None:
                continue
            ud += [r.sail, r.watch, r.reef, r.warning]
            for navn, tekst in r.rows:
                ud += [navn, tekst]
    return [x for x in ud if x]


def all_strings() -> list[str]:
    """Alt, der er markeret til oversættelse, i den rækkefølge filerne læses."""
    seen, out = set(), []
    for p in sorted((ROOT / 'app').rglob('*.py')):
        if '__pycache__' in str(p) or p.parent.name == 'lang':
            continue
        for s in strings_in(p):
            if s not in seen:
                seen.add(s)
                out.append(s)
    for s in manual_strings() + trim_strings():
        if s not in seen:
            seen.add(s)
            out.append(s)
    return out


def main() -> None:
    from app.lang import de, de_manual, de_plan, de_soe, de_ui
    # Samme tre tabeller, som i18n lægger sammen. Læste værktøjet kun de.py,
    # ville manualen og sejlplanens prosa tælle som umarkerede.
    ord_ = {**de.WORDS, **de_ui.WORDS, **de_manual.WORDS,
            **de_plan.WORDS, **de_soe.WORDS}

    found = all_strings()
    bad = [s for s in found if s.startswith('\0F-STRENG')]
    real = [s for s in found if not s.startswith('\0F-STRENG')]
    missing = [s for s in real if s not in ord_]
    stale = [s for s in ord_
             if s not in real and not s.endswith(PLURAL_MARK)]

    print(f'{len(real)} tekster markeret til oversættelse')
    print(f'{len(real) - len(missing)} oversat til tysk, {len(missing)} mangler')
    if stale:
        print(f'{len(stale)} tyske tekster hører ikke længere til nogen dansk '
              f'sætning — de er sandsynligvis blevet omskrevet')
    if bad:
        print(f'\n{len(bad)} kald bruger en f-streng. De kan ikke slås op — '
              f'pladsholderne skal stå som {{navn}} i teksten:')
        for s in bad[:8]:
            print(f'   {s[10:60]}…')

    if '--liste' in sys.argv:
        print('\nMANGLER:')
        for s in missing:
            print(f'   {s}')
    if '--skabelon' in sys.argv:
        print('\n    # ── mangler ──')
        for s in missing:
            key = s.replace("'", "\\'")
            print(f"    '{key}':\n        '',")
    if stale and '--liste' in sys.argv:
        print('\nFORÆLDEDE:')
        for s in stale:
            print(f'   {s}')


if __name__ == '__main__':
    main()
