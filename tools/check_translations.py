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
    return [s.strip() for s in out if s and s.strip()]


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
    for s in manual_strings():
        if s not in seen:
            seen.add(s)
            out.append(s)
    return out


def main() -> None:
    from app.lang import de, de_manual, de_plan, de_ui
    # Samme tre tabeller, som i18n lægger sammen. Læste værktøjet kun de.py,
    # ville manualen og sejlplanens prosa tælle som umarkerede.
    ord_ = {**de.WORDS, **de_ui.WORDS, **de_manual.WORDS,
            **de_plan.WORDS}

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
