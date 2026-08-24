"""Ingen funktion må kalde et navn, den ikke kan se.

Den her findes, fordi `harbours.py` tog `t()` i brug uden importen. Modulet
importerede fint — Python slår først navnet op, når funktionen bliver kaldt —
og `t()` sidder i `Harbour.detail`, som kortet kalder ved hvert sidebesøg. Så
gav hele siden 500, og der var ingenting, der virkede.

Første udgave af den her prøve så på alle navne i filen under ét. Den fandt
ingenting, fordi `t` også bruges som en lokal variabel længere nede i samme
fil — og det var jo netop dét, der gjorde fejlen usynlig. Så prøven skal kende
til scope: hvad et navn hedder ét sted i filen, siger ikke, at det findes et
andet sted.
"""
from __future__ import annotations

import ast
import builtins
import pathlib

import pytest

ROT = pathlib.Path(__file__).resolve().parent.parent / 'app'
FILER = sorted(p for p in ROT.rglob('*.py') if '__pycache__' not in str(p))

INDBYGGEDE = set(dir(builtins)) | {'__file__', '__name__', 'self', 'cls'}


def _bindinger(krop) -> set[str]:
    """Navne, det her scope selv binder — uden at gå ind i indlejrede scopes.

    Indlejrede funktioner tæller med ved navn (de bindes her), men deres
    indmad hører til deres eget scope.
    """
    navne = set()
    stak = list(krop)
    while stak:
        n = stak.pop()
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            navne.add(n.name)
            continue                      # indmaden er et andet scope
        if isinstance(n, ast.ImportFrom):
            navne |= {a.asname or a.name for a in n.names}
        elif isinstance(n, ast.Import):
            navne |= {(a.asname or a.name).split('.')[0] for a in n.names}
        elif isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store):
            navne.add(n.id)
        elif isinstance(n, (ast.Global, ast.Nonlocal)):
            navne |= set(n.names)
        elif isinstance(n, ast.ExceptHandler) and n.name:
            navne.add(n.name)
        stak.extend(ast.iter_child_nodes(n))
    return navne


def _argumenter(fn) -> set[str]:
    a = fn.args
    ud = {x.arg for x in (*a.posonlyargs, *a.args, *a.kwonlyargs)}
    for x in (a.vararg, a.kwarg):
        if x:
            ud.add(x.arg)
    return ud


def _kald_i_scope(krop) -> set[str]:
    """De navne, der kaldes som funktion her — ikke i indlejrede scopes."""
    ud = set()
    stak = list(krop)
    while stak:
        n = stak.pop()
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            continue
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name):
            ud.add(n.func.id)
        stak.extend(ast.iter_child_nodes(n))
    return ud


def _gennemgå(node, synlige: set[str], fejl: list) -> None:
    """Gå scopene igennem indefra og ud, som Python selv gør."""
    krop = node.body
    egne = _bindinger(krop) | INDBYGGEDE
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        egne |= _argumenter(node)
    her = synlige | egne

    for navn in _kald_i_scope(krop):
        if navn not in her:
            fejl.append((getattr(node, 'name', '<modul>'), navn))

    for barn in ast.walk(node):
        if barn is node:
            continue
        if isinstance(barn, (ast.FunctionDef, ast.AsyncFunctionDef,
                             ast.ClassDef)):
            # En klassekrop deler ikke sine navne med metoderne.
            arv = her if not isinstance(barn, ast.ClassDef) else synlige | egne
            if _er_direkte_barn(node, barn):
                _gennemgå(barn, arv, fejl)


def _er_direkte_barn(forælder, barn) -> bool:
    return any(b is barn for b in ast.iter_child_nodes(forælder))


@pytest.mark.parametrize('fil', FILER, ids=lambda p: p.name)
def test_kaldte_navne_findes(fil: pathlib.Path):
    tree = ast.parse(fil.read_text(encoding='utf-8'))
    fejl: list = []
    _gennemgå(tree, set(), fejl)
    besked = ', '.join(f'{hvor}() kalder {navn}()' for hvor, navn in fejl)
    assert not fejl, f'{fil.name}: {besked}'
