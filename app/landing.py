"""Forsiden — den, Google læser, og den, en fremmed lander på.

Hvorfor den ikke er bygget i NiceGUI som resten: NiceGUI tegner fladen på
serveren og sender den ned over en websocket. Det, en crawler får udleveret på
`/`, er derfor en tom Vue-skal uden ét ord i. Der stod ingen beskrivelse, ingen
overskrift, ingen brødtekst — og der fandtes hverken robots.txt eller sitemap.
Sejlplan var i praksis usynlig for Google.

Forsiden her er almindelig HTML, skrevet færdig på serveren og sendt i ét svar.
Ingen JavaScript skal køre, før der står noget. Det er også hurtigere for et
menneske: siden er læsbar, før planlæggeren overhovedet er hentet.

Planlæggeren bor på `/planlaeg`. Delelinks og gamle bogmærker til `/?rute=…`
sendes videre dertil, så intet, nogen har liggende, holder op med at virke.
"""
from __future__ import annotations

import html
from datetime import date

from fastapi import Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from nicegui import app

from .config import settings
from .i18n import DA, DE, SV

# Planlæggerens sti. Ét sted, så et skifte ikke skal jages gennem fem filer.
APP_PATH = '/planlaeg'

# Sprogene og deres sti. Dansk ligger på roden — det er hovedsproget, og det
# er dér, links udefra peger hen.
PATHS = {DA: '/', DE: '/de', SV: '/sv'}


def _esc(s: str) -> str:
    return html.escape(s, quote=True)


# ── Teksten, sprog for sprog ──────────────────────────────────────────────────
# Forsiden har sin egen tekst. Den skal sælge, og den skal kunne læses af en,
# der aldrig har set systemet — det er en anden opgave end knapperne inde i
# appen, og den skal kunne rettes uden at røre dem.
TEXT: dict[str, dict] = {
    DA: {
        'lang': 'da',
        'title': 'Sejlplan — find den bedste afgang til din sejltur',
        'description': (
            'Sejlplan regner hver mulig afgangstime igennem med vind, bølger '
            'og strøm, lægger ruten uden om land og giver dig en sejlplan '
            'stræk for stræk. Til sejlbåd og motorbåd i danske farvande.'),
        'kicker': 'Til sejlbåd og motorbåd i danske farvande',
        'h1': 'Hvornår skal du kaste los?',
        'lead': (
            'Du kender ruten. Sejlplan regner hver eneste afgangstime i dit '
            'datovindue igennem — med vind, bølger, strøm og din båds egne '
            'tal — og siger, hvilken afgang der giver den bedste tur. '
            'Og hvorfor.'),
        'cta': 'Læg din sejlplan',
        'cta_note': 'Gratis at prøve. Ingen oprettelse, ingen app at hente.',
        'how_title': 'Sådan virker det',
        'how': [
            ('Læg ruten',
             'Søg efter havne, øer eller en position — eller klik direkte på '
             'søkortet. Sejlplan lægger stregen uden om land efter rigtige '
             'kystlinjedata, ikke i luftlinje. Hele det danske havneregister '
             'er med, og sømærkerne kan lægges oven på kortet.'),
            ('Vælg afgang',
             'Vi gennemsejler hver afgangstime i dit vindue og rangerer dem. '
             'Hver afgang står med sin grund: tidligst hjemme, roligste sø, '
             'eller hvad den koster i forhold til den bedste. Rækkefølgen er '
             'vores anbefaling — valget er dit.'),
            ('Tag planen med',
             'Sejlplanen står stræk for stræk med kurs, sejlføring og '
             'sejltrim, time for time med vind, bølger, strøm og fart, og '
             'med en skippervurdering af, hvor turen er svær. Den kan '
             'printes, deles og læses uden dækning.'),
        ],
        'why_title': 'Hvad Sejlplan gør, som en vejrudsigt ikke gør',
        'why': [
            ('Din båd, ikke en gennemsnitsbåd',
             'Sejlbåd og motorbåd er to forskellige ting. En sejlbåd regnes '
             'på sit polardiagram — farten afhænger af vindens vinkel — og en '
             'motorbåd på marchfart og brændstof. Du kan taste din egen båd '
             'ind.'),
            ('Vejret dér, hvor du er, når du er der',
             'En vejrudsigt gælder et sted. En sejlads flytter sig. Sejlplan '
             'følger båden hen ad ruten time for time og henter vejret for '
             'det punkt, den faktisk er nået til.'),
            ('Grænser, du selv sætter',
             'Maks vind, maks bølger, sejldøgnets længde, om natten tæller '
             'med, om motoren må bruges. Afgange, der bryder dine grænser, '
             'bliver ikke skjult — de bliver mærket, så du selv kan vælge.'),
            ('Overnatninger undervejs',
             'Kan turen ikke nås på ét sejldøgn, finder Sejlplan havnene '
             'langs ruten og lægger overnatningerne ind — med afstikker og '
             'ankomsttid, så du ved, om du kommer frem før kajen lukker.'),
            ('Strøm regnet med',
             'Farten er over grunden. Strømmen står i sin egen søjle, og vi '
             'skriver rent ud, at tallene kommer fra en global havmodel, der '
             'ikke opløser de danske bælter helt.'),
            ('Med til søs',
             'Planen lægges ned i telefonen som sit eget dokument. Går '
             'dækningen midt i Kattegat, står den der stadig.'),
        ],
        'faq_title': 'Ofte stillede spørgsmål',
        'faq': [
            ('Hvad koster Sejlplan?',
             'Du kan lægge en rute og få en sejlplan uden at oprette dig. '
             'Prøv den på din næste tur og se, om tallene passer med din '
             'egen erfaring.'),
            ('Hvilke farvande dækker Sejlplan?',
             'Danske farvande og de tilstødende — Kattegat, Bælterne, '
             'Øresund, Smålandsfarvandet, Sydfynske Øhav og den vestlige '
             'Østersø. Havneregisteret dækker også svenske og tyske havne '
             'langs de ruter, danske sejlere bruger.'),
            ('Hvor kommer vejrdataene fra?',
             'Vind, bølger og strøm hentes fra Open-Meteos vejr- og '
             'havmodeller. Prognosen rækker omkring ti døgn frem, og '
             'bølgemodellen er den, der sætter loftet. Sejlplan skriver, '
             'når et tal er svagere, end det ser ud.'),
            ('Erstatter Sejlplan søkort og sund fornuft?',
             'Nej. Sejlplan er et planlægningsværktøj. Ruten skal '
             'kontrolleres på søkortet, og ansvaret for sejladsen er '
             'skipperens. Det siger vi hellere en gang for meget.'),
            ('Kan jeg bruge Sejlplan til motorbåd?',
             'Ja. Vælg motorbåd, så regnes farten på marchfart og '
             'søtilstand, og brændstofforbruget står i nøgletallene.'),
            ('Virker Sejlplan på telefonen?',
             'Ja. Fladen er bygget til at kunne betjenes med én hånd på '
             'vandet, og den kan lægges på hjemmeskærmen som en app.'),
        ],
        'closing_title': 'Turen, du selv har valgt — regnet ordentligt igennem',
        'closing': (
            'Sejlplan finder ikke turen for dig. Du bestemmer, hvor du skal '
            'hen; vi regner på, hvornår det er bedst at komme af sted.'),
        'nav_app': 'Åbn Sejlplan',
        'foot': 'Sejlplan · planlægning for sejlbåd og motorbåd',
        'disclaimer': (
            'Sejlplan er et planlægningsværktøj og erstatter ikke søkort, '
            'officielle vejrudsigter eller skipperens eget skøn. '
            'Ansvaret for sejladsen er altid skipperens.'),
    },
    DE: {
        'lang': 'de',
        'title': 'Sejlplan — die beste Abfahrtszeit für deinen Törn',
        'description': (
            'Sejlplan rechnet jede mögliche Abfahrtsstunde mit Wind, Wellen '
            'und Strom durch, führt die Route um Land herum und liefert einen '
            'Törnplan Abschnitt für Abschnitt. Für Segel- und Motorboot in '
            'dänischen Gewässern.'),
        'kicker': 'Für Segel- und Motorboot in dänischen Gewässern',
        'h1': 'Wann solltest du ablegen?',
        'lead': (
            'Du kennst die Route. Sejlplan rechnet jede Abfahrtsstunde in '
            'deinem Zeitfenster durch — mit Wind, Wellen, Strom und den '
            'Daten deines Bootes — und sagt dir, welche Abfahrt den besten '
            'Törn ergibt. Und warum.'),
        'cta': 'Törnplan erstellen',
        'cta_note': 'Kostenlos testen. Keine Anmeldung, keine App.',
        'how_title': 'So funktioniert es',
        'how': [
            ('Route legen',
             'Suche Häfen, Inseln oder eine Position — oder klicke direkt in '
             'die Seekarte. Sejlplan führt die Linie anhand echter '
             'Küstendaten um Land herum, nicht in Luftlinie.'),
            ('Abfahrt wählen',
             'Wir simulieren jede Abfahrtsstunde und sortieren sie. Jede '
             'Abfahrt steht mit ihrem Grund da. Die Reihenfolge ist unsere '
             'Empfehlung — die Wahl ist deine.'),
            ('Plan mitnehmen',
             'Der Törnplan steht Abschnitt für Abschnitt mit Kurs, '
             'Segelstellung und Trimm, Stunde für Stunde mit Wind, Wellen, '
             'Strom und Fahrt. Druckbar, teilbar und offline lesbar.'),
        ],
        'why_title': 'Was Sejlplan kann, was eine Wettervorhersage nicht kann',
        'why': [
            ('Dein Boot, kein Durchschnittsboot',
             'Segelboot und Motorboot sind zweierlei. Ein Segelboot wird über '
             'sein Polardiagramm gerechnet, ein Motorboot über Marschfahrt '
             'und Verbrauch. Du kannst dein eigenes Boot eintragen.'),
            ('Wetter dort, wo du dann bist',
             'Eine Vorhersage gilt für einen Ort. Ein Törn bewegt sich. '
             'Sejlplan folgt dem Boot Stunde für Stunde entlang der Route.'),
            ('Grenzen, die du selbst setzt',
             'Max. Wind, max. Welle, Länge des Segeltages, Nachtfahrt, '
             'Motoreinsatz. Abfahrten, die deine Grenzen überschreiten, '
             'werden markiert — nicht versteckt.'),
            ('Übernachtungen unterwegs',
             'Reicht ein Segeltag nicht, findet Sejlplan die Häfen entlang '
             'der Route und plant die Übernachtungen ein.'),
            ('Strom eingerechnet',
             'Die Fahrt ist über Grund. Der Strom steht in einer eigenen '
             'Spalte — samt Hinweis, wo das Modell ungenau wird.'),
            ('Mit an Bord',
             'Der Plan wird im Telefon als eigenes Dokument abgelegt und ist '
             'auch ohne Empfang lesbar.'),
        ],
        'faq_title': 'Häufige Fragen',
        'faq': [
            ('Was kostet Sejlplan?',
             'Du kannst eine Route legen und einen Törnplan bekommen, ohne '
             'dich anzumelden.'),
            ('Welche Gewässer deckt Sejlplan ab?',
             'Dänische und angrenzende Gewässer — Kattegat, die Belte, der '
             'Öresund, die südfünische Inselsee und die westliche Ostsee.'),
            ('Woher kommen die Wetterdaten?',
             'Wind, Wellen und Strom kommen von den Wetter- und Meeresmodellen '
             'von Open-Meteo. Die Vorhersage reicht rund zehn Tage.'),
            ('Ersetzt Sejlplan Seekarte und Seemannschaft?',
             'Nein. Sejlplan ist ein Planungswerkzeug. Die Verantwortung für '
             'die Fahrt trägt immer der Skipper.'),
            ('Kann ich Sejlplan für ein Motorboot nutzen?',
             'Ja. Bei Motorboot wird über Marschfahrt und Seegang gerechnet, '
             'der Verbrauch steht in den Kennzahlen.'),
            ('Funktioniert Sejlplan auf dem Handy?',
             'Ja, und es lässt sich als App auf den Startbildschirm legen.'),
        ],
        'closing_title': 'Dein Törn — ordentlich durchgerechnet',
        'closing': (
            'Sejlplan sucht dir keinen Törn aus. Du bestimmst das Ziel; wir '
            'rechnen aus, wann du am besten losfährst.'),
        'nav_app': 'Sejlplan öffnen',
        'foot': 'Sejlplan · Törnplanung für Segel- und Motorboot',
        'disclaimer': (
            'Sejlplan ist ein Planungswerkzeug und ersetzt weder Seekarte '
            'noch amtliche Vorhersagen noch das Urteil des Skippers.'),
    },
    SV: {
        'lang': 'sv',
        'title': 'Sejlplan — hitta bästa avgången för din segling',
        'description': (
            'Sejlplan räknar igenom varje möjlig avgångstimme med vind, vågor '
            'och ström, drar rutten runt land och ger dig en seglingsplan '
            'sträcka för sträcka. För segelbåt och motorbåt.'),
        'kicker': 'För segelbåt och motorbåt i danska och svenska farvatten',
        'h1': 'När ska du kasta loss?',
        'lead': (
            'Du kan rutten. Sejlplan räknar igenom varje avgångstimme i ditt '
            'datumfönster — med vind, vågor, ström och din båts egna tal — '
            'och säger vilken avgång som ger den bästa turen. Och varför.'),
        'cta': 'Gör din seglingsplan',
        'cta_note': 'Gratis att prova. Ingen registrering, ingen app.',
        'how_title': 'Så fungerar det',
        'how': [
            ('Lägg rutten',
             'Sök hamnar, öar eller en position — eller klicka direkt i '
             'sjökortet. Sejlplan drar linjen runt land efter riktiga '
             'kustdata, inte i fågelvägen.'),
            ('Välj avgång',
             'Vi seglar igenom varje avgångstimme och rangordnar dem. Varje '
             'avgång står med sitt skäl. Ordningen är vår rekommendation — '
             'valet är ditt.'),
            ('Ta planen med',
             'Seglingsplanen står sträcka för sträcka med kurs, segelföring '
             'och trim, timme för timme med vind, vågor, ström och fart. Kan '
             'skrivas ut, delas och läsas utan täckning.'),
        ],
        'why_title': 'Vad Sejlplan gör som en väderprognos inte gör',
        'why': [
            ('Din båt, inte en genomsnittsbåt',
             'Segelbåt och motorbåt är två olika saker. En segelbåt räknas på '
             'sitt polardiagram, en motorbåt på marschfart och bränsle.'),
            ('Vädret där du är när du är där',
             'En prognos gäller en plats. En segling flyttar sig. Sejlplan '
             'följer båten timme för timme längs rutten.'),
            ('Gränser du själv sätter',
             'Max vind, max våghöjd, seglingsdygnets längd, natt och motor. '
             'Avgångar som bryter dina gränser märks — de göms inte.'),
            ('Övernattningar på vägen',
             'Räcker inte ett dygn hittar Sejlplan hamnarna längs rutten och '
             'lägger in övernattningarna.'),
            ('Strömmen inräknad',
             'Farten är över grund. Strömmen står i en egen kolumn, med '
             'besked om var modellen är svag.'),
            ('Med till sjöss',
             'Planen läggs ned i telefonen som ett eget dokument och går att '
             'läsa utan täckning.'),
        ],
        'faq_title': 'Vanliga frågor',
        'faq': [
            ('Vad kostar Sejlplan?',
             'Du kan lägga en rutt och få en seglingsplan utan att '
             'registrera dig.'),
            ('Vilka farvatten täcker Sejlplan?',
             'Danska och angränsande farvatten — Kattegatt, Bälten, Öresund '
             'och västra Östersjön, med svenska hamnar längs de rutterna.'),
            ('Var kommer väderdata ifrån?',
             'Vind, vågor och ström kommer från Open-Meteos väder- och '
             'havsmodeller. Prognosen räcker omkring tio dygn.'),
            ('Ersätter Sejlplan sjökort och sjömanskap?',
             'Nej. Sejlplan är ett planeringsverktyg. Ansvaret för seglingen '
             'är alltid skepparens.'),
            ('Kan jag använda Sejlplan för motorbåt?',
             'Ja. Då räknas farten på marschfart och sjögång, och '
             'bränsleåtgången står i nyckeltalen.'),
            ('Fungerar Sejlplan i telefonen?',
             'Ja, och den kan läggas på hemskärmen som en app.'),
        ],
        'closing_title': 'Turen du själv valt — ordentligt genomräknad',
        'closing': (
            'Sejlplan väljer inte turen åt dig. Du bestämmer vart du ska; vi '
            'räknar ut när det är bäst att ge sig av.'),
        'nav_app': 'Öppna Sejlplan',
        'foot': 'Sejlplan · seglingsplanering för segelbåt och motorbåt',
        'disclaimer': (
            'Sejlplan är ett planeringsverktyg och ersätter varken sjökort, '
            'officiella prognoser eller skepparens eget omdöme.'),
    },
}

# ── Stilen ────────────────────────────────────────────────────────────────────
# Forsidens egen. Den skal kunne stå alene uden appens stilark, og den skal
# kunne læses, før en eneste byte JavaScript er kørt — derfor står den herinde
# og ikke i en fil, browseren skal hente bagefter.
STYLE = """
:root{
  --sea-1:#FFFDF9; --sea-2:#F4F1EA; --sea-3:#E9E4DB;
  --line:rgba(13,27,42,.12); --txt-1:#12212F; --txt-2:#43535F; --txt-3:#7A8791;
  --accent:#B07F26; --accent-soft:rgba(200,147,59,.14); --go:#1E9E52;
}
@media (prefers-color-scheme:dark){
  :root{
    --sea-1:#14212B; --sea-2:#0D1B2A; --sea-3:#1E2F42;
    --line:rgba(240,237,232,.14); --txt-1:#F0EDE8; --txt-2:#A9B4BC;
    --txt-3:#74838D; --accent:#E8B96A; --accent-soft:rgba(232,185,106,.16);
    --go:#35B96A;
  }
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{
  margin:0; background:var(--sea-2); color:var(--txt-1);
  font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
  font-size:16px; line-height:1.6; -webkit-font-smoothing:antialiased;
}
a{color:var(--accent)}
.wrap{max-width:960px; margin:0 auto; padding:0 22px}

header.top{
  border-bottom:1px solid var(--line); background:var(--sea-1);
  position:sticky; top:0; z-index:10;
}
.top .wrap{display:flex; align-items:center; gap:14px; height:58px}
.brand{display:flex; align-items:center; gap:9px; font-weight:800;
       font-size:17px; letter-spacing:-.01em; color:var(--txt-1);
       text-decoration:none}
.brand svg{width:21px; height:21px; fill:var(--accent); flex:none}
.langs{display:flex; gap:2px; margin-left:auto}
.langs a{
  font-size:11px; font-weight:700; letter-spacing:.05em; text-transform:uppercase;
  color:var(--txt-3); text-decoration:none; padding:5px 8px; border-radius:6px;
}
.langs a:hover{background:var(--sea-3); color:var(--txt-1)}
.langs a[aria-current]{color:var(--accent); background:var(--accent-soft)}
.top .btn{margin-left:10px}

.btn{
  display:inline-flex; align-items:center; gap:8px; justify-content:center;
  background:var(--accent); color:#12212F; font-weight:700; font-size:14.5px;
  padding:11px 20px; border-radius:10px; text-decoration:none;
  border:1px solid transparent;
}
.btn:hover{filter:brightness(1.06)}
.btn--sm{font-size:13px; padding:7px 14px; border-radius:8px}
.btn--big{font-size:16.5px; padding:15px 30px; border-radius:12px}

.hero{padding:64px 0 54px; border-bottom:1px solid var(--line)}
.kicker{
  font-size:11.5px; font-weight:700; letter-spacing:.11em; text-transform:uppercase;
  color:var(--accent); margin:0 0 14px;
}
h1{
  font-size:clamp(32px,6vw,52px); line-height:1.05; letter-spacing:-.025em;
  font-weight:800; margin:0 0 18px; max-width:16ch; text-wrap:balance;
}
.lead{font-size:clamp(16.5px,2.2vw,19px); color:var(--txt-2); max-width:58ch;
      margin:0 0 28px}
.cta-note{font-size:12.5px; color:var(--txt-3); margin:12px 0 0}

section{padding:54px 0; border-bottom:1px solid var(--line)}
h2{font-size:clamp(22px,3.4vw,30px); line-height:1.18; letter-spacing:-.018em;
   font-weight:800; margin:0 0 26px; text-wrap:balance}
h3{font-size:16px; font-weight:700; margin:0 0 6px; line-height:1.3}
p{margin:0}

/* De tre trin er et forløb — de er nummererede, fordi rækkefølgen betyder
   noget, ikke fordi tal pynter. */
ol.steps{list-style:none; margin:0; padding:0; display:grid; gap:26px}
@media(min-width:760px){ol.steps{grid-template-columns:repeat(3,1fr); gap:30px}}
ol.steps li{counter-increment:s; position:relative; padding-top:38px}
ol.steps li::before{
  content:counter(s); position:absolute; top:0; left:0;
  width:28px; height:28px; border-radius:50%; display:grid; place-items:center;
  background:var(--accent-soft); color:var(--accent);
  font-size:13px; font-weight:800;
}
ol.steps{counter-reset:s}
ol.steps p{color:var(--txt-2); font-size:14.5px}

/* Egenskaberne er en samling, ikke et forløb — ingen numre. */
ul.feats{list-style:none; margin:0; padding:0; display:grid; gap:1px;
         background:var(--line); border:1px solid var(--line); border-radius:12px;
         overflow:hidden}
@media(min-width:700px){ul.feats{grid-template-columns:1fr 1fr}}
ul.feats li{background:var(--sea-1); padding:20px 22px 22px}
ul.feats p{color:var(--txt-2); font-size:14px}

.faq{display:grid; gap:1px; background:var(--line); border:1px solid var(--line);
     border-radius:12px; overflow:hidden}
.faq details{background:var(--sea-1)}
.faq summary{
  cursor:pointer; padding:16px 22px; font-weight:600; font-size:15px;
  list-style:none; display:flex; align-items:center; gap:10px;
}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:'+'; margin-left:auto; color:var(--txt-3);
                    font-size:19px; font-weight:400; line-height:1}
.faq details[open] summary::after{content:'\\2212'}
.faq summary:hover{background:var(--sea-3)}
.faq .a{padding:0 22px 18px; color:var(--txt-2); font-size:14.5px; max-width:70ch}

.closing{text-align:center; padding:64px 0}
.closing h2{margin-bottom:14px}
.closing p{color:var(--txt-2); max-width:52ch; margin:0 auto 30px;
           font-size:16.5px}

footer{background:var(--sea-1); border-top:1px solid var(--line);
       padding:30px 0 40px}
footer .wrap{display:flex; flex-wrap:wrap; gap:10px 26px; align-items:baseline}
footer p{font-size:12.5px; color:var(--txt-3); margin:0}
.disclaimer{flex-basis:100%; max-width:68ch; line-height:1.55; margin-top:6px}

:focus-visible{outline:2px solid var(--accent); outline-offset:2px}
@media(prefers-reduced-motion:reduce){*{transition:none!important;
                                        animation:none!important}}
"""

LOGO = ('<svg viewBox="0 0 24 24" aria-hidden="true">'
        '<path d="M13 2v14h8L13 2zM11 6L4 16h7V6zM2 18h20l-2 4H4l-2-4z"/></svg>')


def _alternates(current: str) -> str:
    """hreflang for hvert sprog, så Google ved, at siderne er hinandens."""
    base = settings.site_url
    rows = [f'<link rel="alternate" hreflang="{code}" '
            f'href="{_esc(base + path)}">'
            for code, path in PATHS.items()]
    rows.append(f'<link rel="alternate" hreflang="x-default" '
                f'href="{_esc(base + PATHS[DA])}">')
    rows.append(f'<link rel="canonical" href="{_esc(base + PATHS[current])}">')
    return ''.join(rows)


def _structured(text: dict, current: str) -> str:
    """JSON-LD. Det er dét, der giver rige resultater og et FAQ-panel.

    Skrevet i hånden som én streng frem for gennem `json.dumps` af hensyn til
    læsbarheden — men hvert felt køres gennem `json.dumps`, så et citationstegn
    i teksten ikke kan brække dokumentet.
    """
    import json as _json

    def s(v: str) -> str:
        return _json.dumps(v, ensure_ascii=False)

    base = settings.site_url
    faq = ','.join(
        '{"@type":"Question","name":' + s(q) +
        ',"acceptedAnswer":{"@type":"Answer","text":' + s(a) + '}}'
        for q, a in text['faq'])

    return (
        '<script type="application/ld+json">'
        '{"@context":"https://schema.org","@graph":['
        '{"@type":"WebSite","@id":' + s(base + '/#website') +
        ',"url":' + s(base + PATHS[current]) +
        ',"name":"Sejlplan","description":' + s(text['description']) +
        ',"inLanguage":' + s(text['lang']) + '},'
        '{"@type":"SoftwareApplication","name":"Sejlplan"'
        ',"applicationCategory":"TravelApplication"'
        ',"operatingSystem":"Web, iOS, Android"'
        ',"url":' + s(base + APP_PATH) +
        ',"description":' + s(text['description']) +
        ',"inLanguage":["da","de","sv"]'
        ',"offers":{"@type":"Offer","price":"0","priceCurrency":"DKK"},'
        '"featureList":' + s('; '.join(h for h, _ in text['why'])) + '},'
        '{"@type":"FAQPage","mainEntity":[' + faq + ']}'
        ']}</script>')


def render(current: str) -> str:
    """Hele forsiden som ét færdigt HTML-dokument."""
    text = TEXT[current]
    base = settings.site_url
    og_image = base + '/static/icon-512.png'

    steps = ''.join(
        f'<li><h3>{_esc(h)}</h3><p>{_esc(b)}</p></li>'
        for h, b in text['how'])
    feats = ''.join(
        f'<li><h3>{_esc(h)}</h3><p>{_esc(b)}</p></li>'
        for h, b in text['why'])
    faq = ''.join(
        f'<details><summary>{_esc(q)}</summary>'
        f'<div class="a">{_esc(a)}</div></details>'
        for q, a in text['faq'])
    langs = ''.join(
        f'<a href="{_esc(path)}" hreflang="{code}"'
        + (' aria-current="page"' if code == current else '')
        + f'>{code}</a>'
        for code, path in PATHS.items())

    return f"""<!doctype html>
<html lang="{text['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{_esc(text['title'])}</title>
<meta name="description" content="{_esc(text['description'])}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#0D1B2A">
{_alternates(current)}
<meta property="og:type" content="website">
<meta property="og:site_name" content="Sejlplan">
<meta property="og:locale" content="{text['lang']}">
<meta property="og:title" content="{_esc(text['title'])}">
<meta property="og:description" content="{_esc(text['description'])}">
<meta property="og:url" content="{_esc(base + PATHS[current])}">
<meta property="og:image" content="{_esc(og_image)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{_esc(text['title'])}">
<meta name="twitter:description" content="{_esc(text['description'])}">
<meta name="twitter:image" content="{_esc(og_image)}">
<link rel="icon" type="image/png" sizes="32x32" href="/static/favicon-32.png">
<link rel="apple-touch-icon" href="/static/apple-touch-icon.png">
<link rel="manifest" href="/manifest.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet"
      href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap">
<style>{STYLE}</style>
{_structured(text, current)}
</head>
<body>
<header class="top">
  <div class="wrap">
    <a class="brand" href="{_esc(PATHS[current])}">{LOGO}<span>Sejlplan</span></a>
    <nav class="langs" aria-label="Sprog">{langs}</nav>
    <a class="btn btn--sm" href="{APP_PATH}">{_esc(text['nav_app'])}</a>
  </div>
</header>

<main>
  <div class="hero">
    <div class="wrap">
      <p class="kicker">{_esc(text['kicker'])}</p>
      <h1>{_esc(text['h1'])}</h1>
      <p class="lead">{_esc(text['lead'])}</p>
      <a class="btn btn--big" href="{APP_PATH}">{_esc(text['cta'])}</a>
      <p class="cta-note">{_esc(text['cta_note'])}</p>
    </div>
  </div>

  <section>
    <div class="wrap">
      <h2>{_esc(text['how_title'])}</h2>
      <ol class="steps">{steps}</ol>
    </div>
  </section>

  <section>
    <div class="wrap">
      <h2>{_esc(text['why_title'])}</h2>
      <ul class="feats">{feats}</ul>
    </div>
  </section>

  <section>
    <div class="wrap">
      <h2>{_esc(text['faq_title'])}</h2>
      <div class="faq">{faq}</div>
    </div>
  </section>

  <div class="closing">
    <div class="wrap">
      <h2>{_esc(text['closing_title'])}</h2>
      <p>{_esc(text['closing'])}</p>
      <a class="btn btn--big" href="{APP_PATH}">{_esc(text['cta'])}</a>
    </div>
  </div>
</main>

<footer>
  <div class="wrap">
    <p>{_esc(text['foot'])}</p>
    <p><a href="{APP_PATH}">{_esc(text['nav_app'])}</a></p>
    <p class="disclaimer">{_esc(text['disclaimer'])}</p>
  </div>
</footer>
</body>
</html>"""


def robots() -> str:
    return (
        'User-agent: *\n'
        'Allow: /\n'
        # Planlæggeren er en levende flade bag en websocket. Der er intet at
        # indeksere, og en crawler, der henter den, åbner en session pr. besøg.
        f'Disallow: {APP_PATH}\n'
        'Disallow: /_nicegui/\n'
        'Disallow: /offline-plan\n'
        '\n'
        f'Sitemap: {settings.site_url}/sitemap.xml\n')


def sitemap() -> str:
    i_dag = date.today().isoformat()
    urls = ''.join(
        '<url>'
        f'<loc>{_esc(settings.site_url + path)}</loc>'
        f'<lastmod>{i_dag}</lastmod>'
        '<changefreq>weekly</changefreq>'
        f'<priority>{"1.0" if code == DA else "0.8"}</priority>'
        + ''.join(f'<xhtml:link rel="alternate" hreflang="{c}" '
                  f'href="{_esc(settings.site_url + p)}"/>'
                  for c, p in PATHS.items())
        + '</url>'
        for code, path in PATHS.items())
    return ('<?xml version="1.0" encoding="UTF-8"?>'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
            'xmlns:xhtml="http://www.w3.org/1999/xhtml">'
            + urls + '</urlset>')


def register() -> None:
    """Læg forsiden, robots.txt og sitemap på. Kaldes én gang ved opstart."""

    def _page(code: str):
        def side(request: Request) -> Response:
            # Et gammelt bogmærke eller et delelink til `/?rute=…` skal
            # stadig virke. Det er brugerens rute — den må ikke forsvinde,
            # fordi vi har flyttet appen.
            rute = request.query_params.get('rute')
            if rute:
                return RedirectResponse(f'{APP_PATH}?rute={rute}',
                                        status_code=307)
            return HTMLResponse(render(code))
        return side

    for code, path in PATHS.items():
        app.get(path, include_in_schema=False)(_page(code))

    @app.get('/robots.txt', include_in_schema=False)
    def _robots() -> Response:
        return Response(robots(), media_type='text/plain; charset=utf-8')

    @app.get('/sitemap.xml', include_in_schema=False)
    def _sitemap() -> Response:
        return Response(sitemap(), media_type='application/xml')
