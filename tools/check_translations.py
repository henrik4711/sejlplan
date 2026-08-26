"""Hvilke tekster mangler på et andet sprog?

Dansk er kilden, og den danske sætning er nøglen. Prisen for det er, at retter
man en dansk sætning, mister den sin oversættelse i stilhed. Det her værktøj
finder dem, så det ikke sker ubemærket.

Det leder efter kald til `t('…')` i koden og slår hver enkelt op i sprogtabellen.
Er den der ikke, står den danske sætning i stedet ude i programmet — det virker,
men det er ikke oversat.

Kør:  python tools/check_translations.py             (alle sprog)
      python tools/check_translations.py --sprog sv  (ét sprog)
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

# Bøjningerne har ingen dansk sætning at høre til — de er et fremmed sprogs
# form af et ord, der står i tabellen i forvejen. Tælles de med som
# forældede, står der en håndfuld falske hver gang, og så holder man op med
# at se på tallet.
PLURAL_MARK = '|flertal'
SENTENCE_MARK = '|sætning'


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
    # Også emnerne bag en lukket kontakt. Teksten står i koden og skal være
    # oversat den dag, funktionen åbnes — ikke først derefter.
    for group, topics in helptext.groups(alle=True):
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
    # VHF: kanaler, udtryk, opkaldet og nødopkaldet.
    ud.append(sm.VHF_CERTIFICATE)
    for kanal, brug in sm.CHANNELS:
        ud += [kanal, brug]
    for ord_, betyder in sm.PROWORDS:
        ud += [ord_, betyder]
    ud += list(sm.CALL_SCRIPT) + list(sm.PAN_PAN) + list(sm.DSC)
    for linje in sm.MAYDAY:
        ud += [linje.say, linje.note]
    return [x for x in ud if x]


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


def sprog() -> list[str]:
    """Hvilke sprog der tjekkes. `--sprog xx`, ellers dem alle sammen.

    Uden argument er svaret hvert sprog i vælgeren undtagen dansk — dansk *er*
    nøglen. Værktøjet kendte kun tysk, og så kunne et nyt sprog stå halvt
    oversat, uden at noget sagde det.
    """
    from app import i18n
    if '--sprog' in sys.argv:
        i = sys.argv.index('--sprog')
        if i + 1 < len(sys.argv):
            return [sys.argv[i + 1]]
    return [k for k in i18n.LANGUAGES if k != i18n.DA]


def main() -> None:
    from app import i18n

    found = all_strings()
    bad = [s for s in found if s.startswith('\0F-STRENG')]
    real = [s for s in found if not s.startswith('\0F-STRENG')]
    print(f'{len(real)} tekster markeret til oversættelse')

    for kode in sprog():
        # Samme tabeller, som i18n lægger sammen — også manualen og
        # sejlplanens prosa, ellers ville de tælle som umarkerede.
        navn = i18n.LANGUAGES.get(kode, (kode,))[0].lower()
        ord_ = i18n._saml(kode)
        if not ord_:
            print(f'\n{navn}: ingen tabel — app/lang/{kode}.py findes ikke')
            continue
        missing = [s for s in real if s not in ord_]
        stale = [s for s in ord_ if s not in real
                 and not s.endswith((PLURAL_MARK, SENTENCE_MARK))]

        print(f'\n{navn}: {len(real) - len(missing)} oversat, '
              f'{len(missing)} mangler')
        if stale:
            print(f'   {len(stale)} tekster hører ikke længere til nogen '
                  f'dansk sætning — de er sandsynligvis blevet omskrevet')
        if '--liste' in sys.argv:
            for overskrift, liste in (('MANGLER', missing),
                                      ('FORÆLDEDE', stale)):
                if liste:
                    print(f'   {overskrift}:')
                    for s in liste:
                        print(f'      {s}')
        if '--skabelon' in sys.argv and missing:
            print('    # ── mangler ──')
            for s in missing:
                key = s.replace("'", "\\'")
                print(f"    '{key}':\n        '',")

    if bad:
        print(f'\n{len(bad)} kald bruger en f-streng. De kan ikke slås op — '
              f'pladsholderne skal stå som {{navn}} i teksten:')
        for s in bad[:8]:
            print(f'   {s[10:60]}…')


if __name__ == '__main__':
    main()
