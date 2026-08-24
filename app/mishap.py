"""Når noget går galt, skal brugeren vide det.

Den værste fejl, vi har haft, var ikke en forkert udregning. Det var et tryk på
tandhjulet, der ikke gjorde noget som helst. Serveren kastede en undtagelse,
skrev den i loggen og sendte ingenting videre — og brugeren stod med en knap,
der bare var død. Man kan ikke rapportere en fejl, man ikke kan se.

Så nu bliver hver eneste undtagelse to ting: en linje i loggen med det, der
skal til for at finde den igen, og en besked på skærmen med et nummer, man kan
sige højt. Brugeren ved, at det ikke var ham, og vi kan finde linjen.
"""
from __future__ import annotations

import logging
import traceback
from datetime import datetime

from nicegui import app, ui

from .i18n import t

log = logging.getLogger('sejlplan')

# Fejlnumre tælles op i den kørende server. De skal ikke være unikke i verden,
# kun nemme at læse højt og finde igen i loggen fra samme dag.
_count = 0


def _number() -> str:
    global _count
    _count += 1
    return f'{datetime.now():%d%H%M}-{_count}'


def report(exc: Exception, where: str = '') -> str:
    """Skriv fejlen i loggen, og giv nummeret tilbage."""
    ref = _number()
    log.error('FEJL %s%s: %s\n%s', ref, f' i {where}' if where else '',
              exc, ''.join(traceback.format_exception(
                  type(exc), exc, exc.__traceback__)))
    return ref


def tell(exc: Exception, where: str = '') -> None:
    """Sig det til brugeren. Uden teknik, men med noget at gå videre med."""
    ref = report(exc, where)
    try:
        ui.notify(
            t('Noget gik galt her — det er ikke dig. Prøv igen, og skriv '
              'fejl {ref}, hvis det bliver ved.', ref=ref),
            type='negative', position='bottom', multi_line=True,
            timeout=9000, close_button='OK',
            classes='max-w-[380px]')
    except Exception:
        # Ingen brugerflade at sige det i. Loggen har den stadig.
        pass


def guard(where: str = ''):
    """Dekorator til handlinger, der ikke må dø i stilhed."""
    def wrap(fn):
        def inner(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except Exception as exc:      # noqa: BLE001 — det er hele pointen
                tell(exc, where or getattr(fn, '__name__', ''))
        inner.__name__ = getattr(fn, '__name__', 'inner')
        inner.__doc__ = fn.__doc__
        return inner
    return wrap


def install() -> None:
    """Fang alt, hvad NiceGUI ellers ville have slugt."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(name)s %(message)s')
    app.on_exception(lambda exc: tell(exc, 'brugerfladen'))
