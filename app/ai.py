"""AI-sejlanalyse via Anthropics Claude.

Kaldet sker på serveren med serverens egen nøgle, så brugerne aldrig skal skaffe
en API-nøgle — og nøglen når aldrig ud i browseren. Svaret streames, så teksten
skriver sig frem i UI'et i stedet for at brugeren stirrer på en spinner.

Briefingen indeholder det, planlæggeren allerede har regnet ud: havvejen, ikke
luftlinjen; sejldøgnet og de overnatninger det tvinger frem; og for en motorbåd
hvad søen gør ved farten. Modellen skal vurdere planen, ikke gætte den.
"""
from __future__ import annotations

from collections.abc import AsyncIterator

import anthropic

from .i18n import t
from .boats import Boat
from .config import settings
from .dates import day_time, full
from .narrative import stretch_briefs
from .sailing import Limits, Plan, Route, compass

MAX_TOKENS = 8000

SYSTEM_PROMPT = """Du er en erfaren dansk sejlkonsulent og navigatør med mange års \
erfaring i danske og skandinaviske farvande.

Du får en konkret ruteplan med time-for-time prognoser og skal give en praktisk \
vurdering til skipperen. Skriv på dansk med korrekte søfartsudtryk.

Ruten er allerede lagt uden om land, og afstandene er sejlbare afstande. Er der \
lagt overnatninger ind, er det fordi turen ikke kan nås inden for skipperens \
sejldøgn — forhold dig til om de stop er velvalgte, og foreslå bedre havne hvis \
du kender nogen.

Er båden en motorbåd, handler turen om søen og om farten: hvornår skal der tages \
fart af, hvor bliver det hårdt, hvad koster det i brændstof, og hvad betyder det \
for besætningen. Er den en sejlbåd, handler den om vind, sejlføring og krydsben.

Svar altid i præcis denne struktur med markdown-overskrifter:

## Overordnet vurdering
## Stræk for stræk
## Anbefalet afgang
## Risici og forbehold
## Sejlstrategi

Vær konkret og handlingsanvisende — nævn klokkeslæt, vindretninger, sejlføring og \
hvor der er nødhavne undervejs. Sig det ligeud, hvis turen bør udskydes. Undlad \
generelle forbehold om at tjekke vejrudsigten; skipperen ved det godt. \
Maksimalt 600 ord."""


# Sproglaget lægges ovenpå. Selve prompten bliver stående på dansk: den er
# skrevet med præcise søfartsudtryk, og en oversat prompt ville koste netop
# den præcision, som er hele grunden til at spørge.
SPROG_TILLAEG = {
    'de': """

VIGTIGT — SPROG: Skipperen læser tysk. Skriv hele svaret på tysk med korrekte
tyske søfartsudtryk (Etmal, am Wind, raumer Wind, Gegensee, reffen, Nothafen).
Brug disse overskrifter i stedet:

## Gesamteinschätzung
## Abschnitt für Abschnitt
## Empfohlene Abfahrt
## Risiken und Vorbehalte
## Segelstrategie""",
}


def _system_prompt() -> str:
    """Prompten på dansk, med en sprogbesked ovenpå, hvis der er brug for en."""
    from .i18n import lang
    return SYSTEM_PROMPT + SPROG_TILLAEG.get(lang(), '')



class AIUnavailable(RuntimeError):
    """Serveren har ingen brugbar API-nøgle, eller tjenesten svarer ikke."""


def _client() -> anthropic.AsyncAnthropic:
    if not settings.ai_available:
        raise AIUnavailable(
            t('AI-analysen er ikke slået til på denne server. '
              'Sæt ANTHROPIC_API_KEY i .env og genstart.'))
    return anthropic.AsyncAnthropic(api_key=settings.anthropic_key)


def _boat_block(boat: Boat) -> str:
    if boat.is_motor:
        return (f'  {boat.name} — motorbåd, {boat.length_m} m, {boat.hull} skrog.\n'
                f'  Marchfart {boat.cruise_kn:.0f} kn i smult vande, '
                f'forbrug {boat.fuel_lph:.0f} l/t ved den fart.\n'
                f'  Komfortgrænser: {boat.max_wind_kn:.0f} kn vind, '
                f'{boat.max_wave_m:.1f} m bølger.')
    return (f'  {boat.name} — sejlbåd, {boat.length_m} m, '
            f'skrogfart {boat.hull_speed_kn} kn, motorfart {boat.motor_speed_kn} kn.\n'
            f'  Komfortgrænser: {boat.max_wind_kn:.0f} kn vind, '
            f'{boat.max_wave_m:.1f} m bølger.')


def build_prompt(boat: Boat, route: Route, plan: Plan, alternatives: list[Plan],
                 limits: Limits, has_waves: bool) -> str:
    """Saml rutens fakta til én kompakt briefing."""
    legs = []
    for i, wp in enumerate(route.waypoints[:-1]):
        nxt = route.waypoints[i + 1]
        steps = [s for s in route.steps if s.leg == i]
        crs = steps[0].course if steps else 0
        legs.append(f'  Ben {i + 1}: {wp.name} → {nxt.name} — '
                    f'{route.leg_nm(i):.1f} sømil ad havvejen, '
                    f'indledende kurs {crs:.0f}° ({compass(crs)})')

    stretches = [
        f'  {st.number}. {st.frm} → {st.to} — {st.distance_nm:.1f} sm, '
        f'kurs {st.course}° ({compass(st.course)}), {st.starts} → {st.ends}'
        for st in stretch_briefs(route, plan, boat)]

    days = [f'  Dag {i}: {d.frm} → {d.to}, {d.nm:.1f} sm, '
            f'{day_time(d.depart)} → {day_time(d.arrive)}'
            for i, d in enumerate(plan.days, 1)]

    stops = [f'  {s.name} ({s.detail}) — i havn {day_time(s.arrive)}, '
             f'videre {day_time(s.depart)}, {s.detour_nm:.1f} sm ind fra ruten'
             + ('  [NÅET FOR SENT]' if s.late else '')
             for s in plan.stops]

    # Hver anden time holder detaljeringsgraden nede uden at miste billedet.
    hours = []
    for s in plan.segments[::2][:40]:
        mode = 'motor' if s.motoring else 'sejl'
        hours.append(
            f'  {day_time(s.time)} ben{s.leg} kurs{s.course}° TWA{s.twa}° — '
            f'{s.wind_kn:.0f} kn fra {compass(s.wind_dir)} (kast {s.gust_kn:.0f}), '
            f'bølger {s.wave_m:.1f} m {s.sea}, fart {s.speed_kn:.1f} kn [{mode}]')

    alts = []
    for i, a in enumerate(alternatives[:5], 1):
        nights = f', {a.nights} overnatning(er)' if a.stops else ''
        alts.append(f'  {i}. {day_time(a.depart)} → {day_time(a.arrival)} '
                    f'({a.hours} t med fart i, snit {a.avg_speed_kn} kn, '
                    f'top {a.worst_wind_kn:.0f} kn / {a.worst_wave_m:.1f} m, '
                    f'{a.red_hours} t frarådet{nights})')

    wave_note = ('' if has_waves else
                 '\nBEMÆRK: Der findes ingen bølgeprognose for denne rute '
                 '(typisk indre farvande og fjorde). Bølgehøjderne står som 0 og '
                 'skal ikke tolkes som havblik — vurdér søgangen ud fra vind og stræk.')

    fuel = (f'\n  Brændstof i alt ca. {plan.fuel_l:.0f} liter.'
            if boat.is_motor else '')
    late = ('\n  ADVARSEL: skipperen er først i havn efter sejldøgnets slut.'
            if plan.late_arrival else '')

    return f"""BÅD
{_boat_block(boat)}

SKIPPERENS SEJLDØGN
  Ud af havn tidligst {limits.day_start:02d}:00, fortøjet igen senest {limits.day_end:02d}:00.
  Mørkesejlads: {'accepteret' if limits.night_ok else 'fravalgt'}.

RUTE
  {' → '.join(w.name for w in route.waypoints)}
{chr(10).join(legs)}
  I alt {plan.total_nm} sømil ad havvejen, fordelt på {len(route.waypoints) - 1} ben.

STRÆK MED SAMME KURS
  Benene deles op dér, hvor kursen reelt skifter. Det er de her stræk, en
  vurdering skal gælde for — ikke benet som helhed.
{chr(10).join(stretches)}

VALGT AFGANG
  Afgang {full(plan.depart)} → ankomst {full(plan.arrival)}
  {plan.hours} timer med fart i, gennemsnitsfart {plan.avg_speed_kn} kn.
  Kraftigste vind {plan.worst_wind_kn:.0f} kn, højeste bølger {plan.worst_wave_m:.1f} m.
  {plan.red_hours} timer frarådes, {plan.yellow_hours} timer med skærpet opmærksomhed,
  {plan.night_hours} timer i mørke, {plan.motor_hours} timer for motor.{fuel}{late}{wave_note}

DAGE
{chr(10).join(days)}

OVERNATNINGER UNDERVEJS
{chr(10).join(stops) if stops else '  Ingen — turen nås i ét stræk.'}

VEJR UNDERVEJS (hver anden time)
{chr(10).join(hours)}

ANDRE MULIGE AFGANGE
{chr(10).join(alts) if alts else '  Ingen alternativer beregnet.'}
"""


async def stream_analysis(boat: Boat, route: Route, plan: Plan,
                          alternatives: list[Plan], limits: Limits,
                          has_waves: bool = True) -> AsyncIterator[str]:
    """Stream analysen tekststump for tekststump."""
    client = _client()
    prompt = build_prompt(boat, route, plan, alternatives, limits, has_waves)

    try:
        async with client.messages.stream(
            model=settings.ai_model,
            max_tokens=MAX_TOKENS,
            system=_system_prompt(),
            thinking={'type': 'adaptive'},
            output_config={'effort': 'medium'},
            messages=[{'role': 'user', 'content': prompt}],
        ) as stream:
            async for text in stream.text_stream:
                yield text
    except anthropic.AuthenticationError as exc:
        raise AIUnavailable(
            t('Serverens API-nøgle blev afvist. Tjek '
              'ANTHROPIC_API_KEY.')) from exc
    except anthropic.RateLimitError as exc:
        raise AIUnavailable(
            t('For mange forespørgsler lige nu. Prøv igen om et '
              'øjeblik.')) from exc
    except anthropic.APIStatusError as exc:
        raise AIUnavailable(
            t('AI-tjenesten svarede med fejl {kode}.',
              kode=exc.status_code)) from exc
    except anthropic.APIConnectionError as exc:
        raise AIUnavailable(
            t('Kunne ikke få forbindelse til AI-tjenesten.')) from exc
