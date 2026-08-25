"""Se andre både på kortet — og lade dem se dig.

Reglerne er ikke pynt, de er konstruktionen:

**Usynlig som udgangspunkt.** Ingen bliver delt ved et uheld. Man tænder selv,
og man vælger et bådnavn — ikke sit eget.

**Man ser kun andre, hvis man selv er synlig.** Ingen kan ligge og kigge uden
at være der selv. Slukker man, forsvinder man fra andres kort, og de fra ens.

**Positionen udløber.** Kommer der ingen ny inden for en halv time, er båden
væk. Der findes ingen historik — hver position skriver den forrige over.

Om det tekniske: NiceGUI giver hver browser sin egen session, så de kan ikke
se hinandens. Positionerne ligger derfor i databasen på volumet, som alle
sessioner læser fra. Og fordi ingen session får besked, når en anden flytter
sig, kigger hver enkelt efter med jævne mellemrum. Det er ikke elegant, men det
er robust: der er ingen forbindelse mellem to browsere, der kan gå i stykker.
"""
from __future__ import annotations

import asyncio
import secrets

from nicegui import app, ui

from .. import chat, fleetmap, postbud
from ..i18n import t

# Hvor tit sikkerhedsnettet kigger efter. Det er ikke længere det, der bærer —
# postbuddet siger til, når der sker noget — så det må gerne være sjældent. To
# minutter er nok til at samle op, hvis en hændelse er gået tabt, og lidt nok
# til at ti åbne browsere ikke laver tredive opslag i minuttet om ingenting.
POLL_S = 120

MARK_KEY = 'sejlplan_baad'
NAME_KEY = 'sejlplan_baadnavn'


def mark() -> str:
    """Bådens mærke. Ikke en konto — et tilfældigt navn på den her browser."""
    try:
        m = app.storage.user.get(MARK_KEY)
        if not m:
            m = secrets.token_urlsafe(12)
            app.storage.user[MARK_KEY] = m
        return str(m)
    except (RuntimeError, KeyError):
        return ''


def saved_name() -> str:
    try:
        return str(app.storage.user.get(NAME_KEY) or '')
    except (RuntimeError, KeyError):
        return ''


def remember_name(name: str) -> None:
    try:
        app.storage.user[NAME_KEY] = name.strip()[:fleetmap.NAME_MAX]
    except (RuntimeError, KeyError):
        pass


def available() -> bool:
    return fleetmap.available()


# Hvad browseren selv siger om sig selv. En computer har ingen GPS: dens
# position kommer fra nettet, og den kan være kilometer ved siden af. Det skal
# man vide, før man tænder — ellers står man som en båd midt i en by.
PROBE_JS = """
(async () => {
  const ua = navigator.userAgent || '';
  const mobil = (navigator.userAgentData && navigator.userAgentData.mobile)
    || (navigator.maxTouchPoints > 1 && /Mobi|Android|iPhone|iPad/i.test(ua));
  let tilladelse = null;
  try {
    if (navigator.permissions) {
      const p = await navigator.permissions.query({name: 'geolocation'});
      tilladelse = p.state;
    }
  } catch (e) {}
  return {mobil: !!mobil, tilladelse: tilladelse,
          findes: !!navigator.geolocation};
})()
"""


async def _probe(planner) -> dict:
    """Spørg browseren, hvad den kan. Svarer den ikke, går vi ud fra det bedste
    — en advarsel, vi ikke er sikre på, er værre end ingen."""
    try:
        svar = await planner.client.run_javascript(PROBE_JS, timeout=4.0)
    except Exception:
        return {}
    return svar if isinstance(svar, dict) else {}


def _position_advarsel(probe: dict) -> tuple[str, str, str] | None:
    """(ikon, overskrift, forklaring) — eller ingenting, hvis alt er fint."""
    if probe.get('findes') is False:
        return ('location_disabled', t('Browseren giver ikke adgang til '
                                       'position'),
                t('Uden en position er der ingen båd at vise. Prøv i en '
                  'anden browser, eller på telefonen.'))
    if probe.get('tilladelse') == 'denied':
        return ('block', t('Du har sagt nej til position for den her side'),
                t('Browseren spørger ikke igen af sig selv. Slå det til i '
                  'indstillingerne for siden — i Chrome ligger det bag '
                  'hængelåsen i adresselinjen.'))
    if probe.get('mobil') is False:
        return ('desktop_windows', t('Du sidder ved en computer'),
                t('En computer har ingen GPS. Den gætter positionen ud fra '
                  'wifi og netværk, og det kan være kilometer ved siden af — '
                  'de andre ser din båd et sted, du ikke er. På telefonen er '
                  'den på få meter. Vil du vises rigtigt undervejs, så åbn '
                  'Sejlplan på telefonen.'))
    return None


# ── Til- og fravalg ──────────────────────────────────────────────────────────
async def ask(planner) -> None:
    """Første gang: forklar hvad der deles, og bed om et bådnavn."""
    probe = await _probe(planner)
    advarsel = _position_advarsel(probe)
    navn = {'v': saved_name() or (planner.s.boat.name if planner.s.has_custom
                                  else '')}

    with ui.dialog() as dlg, ui.card().classes(
            'w-full max-w-[440px] p-0 bg-[var(--sea-1)] rounded-[var(--r)]'):

        with ui.element('div').classes('px-5 pt-5 pb-1'):
            ui.label(t('Vis din båd på kortet')).classes(
                'text-[16px] font-bold block')
            ui.label(t('Så kan andre, der også er synlige, se hvor du er — og '
                       'du kan se dem. Kun jer, der har slået det til.')) \
                .classes('text-[12.5px] text-[var(--txt-2)] leading-snug '
                         'mt-1 block')

        if advarsel:
            ikon, hoved, forklaring = advarsel
            with ui.element('div').classes(
                    'mx-5 mt-3 px-3.5 py-3 rounded-[10px] flex items-start '
                    'gap-2.5 bg-[var(--warn-soft)] '
                    'border border-[var(--warn)]'):
                ui.icon(ikon).classes(
                    'text-[18px] text-[var(--warn)] shrink-0 mt-0.5')
                with ui.element('div').classes('min-w-0'):
                    ui.label(hoved).classes(
                        'text-[12.5px] font-semibold block leading-snug')
                    ui.label(forklaring).classes(
                        'text-[11.5px] text-[var(--txt-2)] leading-snug '
                        'mt-0.5 block')

        with ui.element('div').classes('px-5 pt-4'):
            felt = ui.input(t('Bådens navn'),
                            value=navn['v'],
                            placeholder='Havfruen') \
                .props('outlined dense autofocus maxlength='
                       f'{fleetmap.NAME_MAX}').classes('w-full')
            ui.label(t('Skriv bådens navn, ikke dit eget. Det er dét, de '
                       'andre ser.')) \
                .classes('text-[11px] text-[var(--txt-3)] leading-snug '
                         'mt-1 block')

            ui.html('<div class="hairline mt-4 mb-3"></div>')
            for icon, text in (
                    ('visibility_off',
                     t('Du er usynlig, indtil du selv tænder — og du '
                       'forsvinder igen i samme øjeblik, du slukker.')),
                    ('schedule',
                     t('Positionen udløber af sig selv efter en halv time '
                       'uden opdatering.')),
                    ('history_toggle_off',
                     t('Der gemmes ingen historik. Hver ny position skriver '
                       'den forrige over, så ingen kan slå op, hvor du var '
                       'i går.')),
                    ('swap_horiz',
                     t('Du ser kun andre, mens du selv er synlig. Ingen kan '
                       'kigge uden at være der selv.'))):
                with ui.element('div').classes('flex items-start gap-2.5 mb-2'):
                    ui.icon(icon).classes(
                        'text-[16px] text-[var(--accent)] shrink-0 mt-0.5')
                    ui.label(text).classes(
                        'text-[11.5px] text-[var(--txt-2)] leading-snug')

        with ui.row().classes('w-full items-center gap-2 px-5 py-4 no-wrap'):
            ui.element('div').classes('flex-1')
            ui.button(t('Fortryd'), on_click=dlg.close) \
                .props('flat no-caps').classes('text-[var(--txt-2)]')
            ui.button(t('Vis mig'), icon='visibility',
                      on_click=lambda: _accept(planner, felt.value, dlg)) \
                .props('unelevated no-caps').classes('btn-primary px-4')

    dlg.open()


def _accept(planner, name: str, dlg) -> None:
    name = (name or '').strip()
    if len(name) < 2:
        ui.notify(t('Giv båden et navn, de andre kan se'),
                  type='warning', position='bottom')
        return
    remember_name(name)
    dlg.close()
    turn_on(planner)


def turn_on(planner) -> None:
    planner.sharing = True
    planner.fleet = []
    # Positionen kommer fra den samme lytter som "Jeg er undervejs". Er den
    # ikke i gang, startes den nu.
    from . import underway
    if not planner.underway:
        underway.start(planner)
    # Har vi allerede en position, skal den ud med det samme — ellers står man
    # og venter på næste GPS-svar, før man findes for de andre. Det samme
    # gælder et nyt bådnavn: skifter man det uden at flytte sig, ville de andre
    # blive ved med at se det gamle, til båden bevægede sig.
    if planner.last_pos:
        fleetmap.show(mark(), saved_name() or 'Båd', *planner.last_pos)
    planner.header_inbox.refresh()
    ui.notify(t('Din båd er nu synlig for andre, der også er det.'),
              type='positive', position='bottom')
    planner.refresh()


def turn_off(planner) -> None:
    """Sluk. Rækken slettes med det samme — den skjules ikke."""
    planner.sharing = False
    planner.fleet = []
    fleetmap.hide(mark())
    if planner.map:
        planner.map.show_fleet([])
    planner.header_inbox.refresh()
    ui.notify(t('Du er ikke længere synlig, og din position er slettet.'),
              position='bottom')
    planner.refresh()


# ── Undervejs ────────────────────────────────────────────────────────────────
def report_position(planner, lat: float, lon: float,
                    course=None, speed=None) -> None:
    """Læg vores egen position ind, hvis vi deler."""
    if not planner.sharing or not available():
        return
    fleetmap.show(mark(), saved_name() or 'Båd', lat, lon, course, speed)
    planner.last_pos = (lat, lon)
    refresh(planner)


def tick(planner) -> None:
    """Sikkerhedsnettets slag. Den kører altid — den gør bare ingenting, når
    man ikke deler.

    Første udgave lavede måleren, når man tændte for delingen. Men det skete
    inde i dialogen, og da den forsvandt, forsvandt måleren med. Kortet blev
    aldrig opdateret, og de andre både dukkede aldrig op.

    Nu er den ikke længere den, der bærer: postbuddet siger til, når der sker
    noget. Måleren er dét, der ville bære, hvis vi en dag kører flere
    processer, og den kører derfor meget sjældnere end før.
    """
    if planner.sharing:
        refresh(planner)


async def listen(planner) -> None:
    """Lyt efter hændelser og tegn om, når der sker noget.

    Det her er det, der gør, at en besked kommer frem med det samme i stedet
    for at vente på næste opslag. Opgaven lever, så længe browseren gør.
    """
    a = postbud.subscribe(mark())
    if a is None:
        return
    planner.postbud_abonnent = a
    try:
        while True:
            h = await a.kø.get()
            if planner.client is None:
                return
            with planner.client:
                if h.slags == postbud.BESKED:
                    _ny_besked(planner, h)
                elif planner.sharing:
                    refresh(planner)
    except asyncio.CancelledError:
        raise
    except Exception:
        # En lytter, der dør, må ikke tage fladen med sig. Sikkerhedsnettet
        # henter stadig, det er bare langsommere.
        pass
    finally:
        postbud.unsubscribe(a)
        planner.postbud_abonnent = None


def _ny_besked(planner, h) -> None:
    """Der er kommet en besked. Sig det, hvor man kigger.

    Vi åbner ikke samtalen af sig selv. Man kan stå med hænderne i en fald,
    og en dialog, der springer op, er værre end en prik, man kan tage, når
    man har tid.
    """
    planner.header_inbox.refresh()
    planner.fleet_line.refresh()
    if planner.sharing:
        refresh(planner)
    navn = (h.fra_navn or '').strip() or t('En anden båd')
    ui.notify(t('{navn} har skrevet til dig', navn=navn),
              position='bottom', type='info',
              on_dismiss=None)


def refresh(planner) -> None:
    """Hent de andres positioner og tegn dem."""
    if not planner.sharing or not available():
        return
    here = planner.last_pos or (None, None)
    mine = mark()
    try:
        boats = fleetmap.others(mine, here[0], here[1])
    except Exception:
        return

    # Blokerede både findes ikke — hverken på kortet eller i beskederne. Det
    # gælder begge veje: har han blokeret mig, ser jeg ham heller ikke.
    try:
        if chat.available():
            spaerret = chat.blocked_list(mine)
            boats = [b for b in boats if b.mark not in spaerret]
            # En båd, der har skrevet og venter på svar, får en prik.
            venter = {m.from_mark for m in chat.inbox(mine) if not m.seen}
            for b in boats:
                b.unread = 1 if b.mark in venter else 0
    except Exception:
        pass

    planner.fleet = boats
    if planner.map:
        planner.map.show_fleet(boats)
        planner._draw_me()
    planner.fleet_line.refresh()
    planner.header_inbox.refresh()


def line(planner) -> None:
    """Linjen i panelet: er jeg synlig, og hvor mange andre er der?"""
    if not available():
        return

    if not planner.sharing:
        with ui.element('div').classes('flex items-center gap-2 mt-3'):
            ui.button(t('Vis min båd for andre'), icon='visibility',
                      on_click=lambda: ask(planner)) \
                .props('flat dense no-caps size=sm') \
                .classes('text-[var(--txt-3)] hover:text-[var(--accent)]')
        return

    n = len(planner.fleet)
    ulaest = chat.unread(mark()) if chat.available() else 0

    # Uden position er man ikke synlig for nogen, uanset hvad der står. Første
    # udgave skrev "Du er synlig" og "ingen andre både i nærheden", også når
    # telefonen aldrig havde svaret — og så tror man, funktionen virker.
    if not planner.last_pos:
        with ui.element('div').classes(
                'card px-3.5 py-2.5 mt-3 flex items-center gap-3'):
            ui.icon('location_searching').classes(
                'text-[18px] text-[var(--accent)] shrink-0')
            with ui.element('div').classes('min-w-0 flex-1'):
                if planner.pos_error:
                    ui.label(planner.pos_error).classes(
                        'text-[12px] text-[var(--stop)] leading-snug block')
                else:
                    ui.label(t('Venter på din position…')).classes(
                        'text-[12.5px] font-medium block')
                    ui.label(t('Du er ikke synlig for andre, før browseren '
                               'har fundet dig. Sig ja til position, hvis '
                               'den spørger.'))                         .classes('text-[11px] text-[var(--txt-3)] '
                                 'leading-snug block')
            # Beskederne skal med her. Uden dem kunne man ikke se, at
            # nogen havde skrevet, så længe browseren ikke havde fundet en
            # position — og på en computer sker det tit aldrig. Beskeden var
            # kommet, knappen fandtes bare ikke.
            if ulaest:
                ui.button(str(ulaest), icon='forum',
                          on_click=planner.open_inbox)                     .props('unelevated dense no-caps size=sm')                     .classes('btn-primary shrink-0')
            ui.button(t('Skjul mig'), icon='visibility_off',
                      on_click=lambda: turn_off(planner))                 .props('flat dense no-caps size=sm')                 .classes('text-[var(--txt-3)] shrink-0')
        return

    with ui.element('div').classes(
            'card px-3.5 py-2.5 mt-3 flex items-center gap-3'):
        ui.icon('sailing').classes('text-[18px] text-[var(--accent)] shrink-0')
        with ui.element('div').classes('min-w-0 flex-1'):
            ui.label(f'{t("Du er synlig som")} {saved_name() or "Båd"}') \
                .classes('text-[12.5px] font-medium block truncate')
            ui.label(t('Ingen andre både i nærheden lige nu.') if not n
                     else t('{n} andre både i nærheden.', n=n)) \
                .classes('text-[11px] text-[var(--txt-3)] block')
        # Har nogen skrevet, skal det stå her — ikke gemt bag et ikon, man
        # skal vide findes i forvejen.
        if ulaest:
            ui.button(str(ulaest), icon='forum',
                      on_click=planner.open_inbox) \
                .props('unelevated dense no-caps size=sm') \
                .classes('btn-primary shrink-0')
        ui.button(t('Skjul mig'), icon='visibility_off',
                  on_click=lambda: turn_off(planner)) \
            .props('flat dense no-caps size=sm') \
            .classes('text-[var(--txt-3)] shrink-0')

    unøjagtig(planner)

    if n:
        with ui.element('div').classes('flex items-center gap-2 mt-1.5'):
            # Tallet er ikke nok. Man skal kunne se hvem, og hvor de ligger —
            # en trekant på et zoomet kort er svær at finde, og umulig at
            # overskue, når man leder efter nogen at skrive til.
            ui.button(t('Se hvem der er i nærheden'), icon='groups',
                      on_click=planner.open_nearby)                 .props('flat dense no-caps size=sm')                 .classes('text-[var(--accent)]')


# Under det her er positionen god nok til at vise en båd. Derover er den et
# gæt fra nettet, ikke en måling — og så skal det stå der.
GOD_NOK_M = 300


def unøjagtig(planner) -> None:
    """Sig det, hvis positionen er et gæt.

    En prik på et kort ser lige sikker ud, hvad enten den er på ti meter eller
    tre kilometer. På en computer er den som regel det sidste, og så ligger ens
    båd et sted, man ikke er — for alle andre at se.
    """
    m = getattr(planner, 'pos_accuracy_m', None)
    if not m or m <= GOD_NOK_M:
        return
    afstand = (t('{km} km', km=f'{m / 1000:.1f}'.replace('.', ','))
               if m >= 1000 else t('{m} meter', m=f'{m:.0f}'))
    with ui.element('div').classes('flex items-start gap-2 mt-1.5'):
        ui.icon('gps_not_fixed').classes(
            'text-[14px] text-[var(--warn)] shrink-0 mt-0.5')
        ui.label(t('Din position er kun kendt på ±{afstand}. Det er et gæt '
                   'fra nettet, ikke GPS — på telefonen er den på få meter.',
                   afstand=afstand))             .classes('text-[10.5px] text-[var(--txt-3)] leading-snug')
