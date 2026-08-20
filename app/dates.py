"""Danske dato- og klokkeslætsformater.

Python bruger serverens locale til %A og %B, og den er sjældent dansk på en
server. Derfor slår vi navnene op selv — så ser det ens ud alle steder.
"""
from __future__ import annotations

from datetime import date, datetime

WEEKDAYS = ['mandag', 'tirsdag', 'onsdag', 'torsdag', 'fredag', 'lørdag', 'søndag']
WEEKDAYS_SHORT = ['man', 'tir', 'ons', 'tor', 'fre', 'lør', 'søn']
MONTHS = ['januar', 'februar', 'marts', 'april', 'maj', 'juni',
          'juli', 'august', 'september', 'oktober', 'november', 'december']
MONTHS_SHORT = ['jan', 'feb', 'mar', 'apr', 'maj', 'jun',
                'jul', 'aug', 'sep', 'okt', 'nov', 'dec']


def weekday(d: date | datetime, short: bool = False) -> str:
    return (WEEKDAYS_SHORT if short else WEEKDAYS)[d.weekday()]


def month(d: date | datetime, short: bool = False) -> str:
    return (MONTHS_SHORT if short else MONTHS)[d.month - 1]


def full(t: datetime) -> str:
    """'tirsdag 18. august kl. 06:00'"""
    return f'{weekday(t)} {t.day}. {month(t)} kl. {t:%H:%M}'


def day_time(t: datetime) -> str:
    """'tir 18/8 06:00'"""
    return f'{weekday(t, short=True)} {t.day}/{t.month} {t:%H:%M}'


def day(t: date | datetime, short: bool = True) -> str:
    """'tir 18. aug'"""
    return f'{weekday(t, short)} {t.day}. {month(t, short=True)}'


def clock(t: datetime) -> str:
    return f'{t:%H:%M}'


def duration(hours: int) -> str:
    """'18 t' eller '1 d 6 t' når turen strækker sig over et døgn."""
    if hours < 24:
        return f'{hours} t'
    d, h = divmod(hours, 24)
    return f'{d} d {h} t' if h else f'{d} d'


def spell(hours: float) -> str:
    """Et tidsrum sagt som man siger det: '40 min', '2½ t', '1 d 6 t'."""
    if hours < 1:
        return f'{max(5, round(hours * 60 / 5) * 5)} min'
    if hours < 6:
        whole = int(hours)
        rest = hours - whole
        if rest < 0.25:
            return f'{whole} t'
        if rest < 0.75:
            return f'{whole}½ t'
        return f'{whole + 1} t'
    return duration(round(hours))
