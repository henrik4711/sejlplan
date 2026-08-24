"""Dato- og klokkeslætsformater.

Python bruger serverens locale til %A og %B, og den er sjældent dansk på en
server. Derfor slår vi navnene op selv — så ser det ens ud alle steder.

Navnene slås op på brugerens sprog. Tysk skriver datoen anderledes end dansk:
"Dienstag, 18. August, 06:00 Uhr", ikke "tirsdag 18. august kl. 06:00". Så
formatet følger sproget, ikke kun ordene.
"""
from __future__ import annotations

from datetime import date, datetime

from .i18n import DE, lang, t

WEEKDAYS = ['mandag', 'tirsdag', 'onsdag', 'torsdag', 'fredag', 'lørdag', 'søndag']
WEEKDAYS_SHORT = ['man', 'tir', 'ons', 'tor', 'fre', 'lør', 'søn']
MONTHS = ['januar', 'februar', 'marts', 'april', 'maj', 'juni',
          'juli', 'august', 'september', 'oktober', 'november', 'december']
MONTHS_SHORT = ['jan', 'feb', 'mar', 'apr', 'maj', 'jun',
                'jul', 'aug', 'sep', 'okt', 'nov', 'dec']


def weekday(d: date | datetime, short: bool = False) -> str:
    return t((WEEKDAYS_SHORT if short else WEEKDAYS)[d.weekday()])


def month(d: date | datetime, short: bool = False) -> str:
    return t((MONTHS_SHORT if short else MONTHS)[d.month - 1])


def full(dt: datetime) -> str:
    """'tirsdag 18. august kl. 06:00' — på tysk med komma og Uhr."""
    if lang() == DE:
        return f'{weekday(dt)}, {dt.day}. {month(dt)}, {dt:%H:%M} Uhr'
    return f'{weekday(dt)} {dt.day}. {month(dt)} kl. {dt:%H:%M}'


def day_time(dt: datetime) -> str:
    """'tir 18/8 06:00'"""
    if lang() == DE:
        return f'{weekday(dt, short=True)} {dt.day}.{dt.month}. {dt:%H:%M}'
    return f'{weekday(dt, short=True)} {dt.day}/{dt.month} {dt:%H:%M}'


def day(dt: date | datetime, short: bool = True) -> str:
    """'tir 18. aug'"""
    return f'{weekday(dt, short)} {dt.day}. {month(dt, short=True)}'


def clock(dt: datetime) -> str:
    return f'{dt:%H:%M}'


def duration(hours: int) -> str:
    """'18 t' eller '1 d 6 t' når turen strækker sig over et døgn."""
    time_ = t('t')
    if hours < 24:
        return f'{hours} {time_}'
    d, h = divmod(hours, 24)
    dag = t('d')
    return f'{d} {dag} {h} {time_}' if h else f'{d} {dag}'


def spell(hours: float) -> str:
    """Et tidsrum sagt som man siger det: '40 min', '2½ t', '1 d 6 t'."""
    time_ = t('t')
    if hours < 1:
        return f'{max(5, round(hours * 60 / 5) * 5)} {t("min")}'
    if hours < 6:
        whole = int(hours)
        rest = hours - whole
        if rest < 0.25:
            return f'{whole} {time_}'
        if rest < 0.75:
            return f'{whole}½ {time_}'
        return f'{whole + 1} {time_}'
    return duration(round(hours))
