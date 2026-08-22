"""Designsystem: farver, typografi og komponentstil.

Ét sted at ændre udseendet. Alt bygger på CSS-variabler, der skifter værdi i
lyst og mørkt tema — Quasar sætter klassen `body--dark`, når mørk tilstand er
slået til, så vi behøver ikke at røre ved noget andet.
"""
from __future__ import annotations

from nicegui import ui

# Accentfarver deles af begge temaer.
GOLD = '#C8933B'
GOLD_DARK = '#E8B96A'
TEAL = '#0F9B8E'
TEAL_DARK = '#4ECDC4'

GREEN = '#1E9E52'
AMBER = '#D98324'
RED = '#D64545'

CSS = """
/* ═══ Farver og mål ══════════════════════════════════════════════ */
body {
  /* Sikkerhedsafstandene paa en iPhone: statuslinjen og urskiven foroven,
     hjemmestriben forneden. Uden for en installeret app er de nul, og saa
     regner alt herunder som foer. */
  --top-inset:    env(safe-area-inset-top, 0px);
  --bottom-inset: env(safe-area-inset-bottom, 0px);
  --header-h:     calc(56px + env(safe-area-inset-top, 0px));

  --sea-1:   #FFFFFF;   /* kort/paneler          */
  --sea-2:   #F4F1EC;   /* sidebaggrund          */
  --sea-3:   #E9E4DB;   /* indlejrede felter     */
  --line:    rgba(13,27,42,.10);
  --line-2:  rgba(13,27,42,.18);
  --txt-1:   #12212F;
  --txt-2:   rgba(18,33,47,.68);
  --txt-3:   rgba(18,33,47,.45);
  --accent:  #C8933B;
  --accent-soft: rgba(200,147,59,.14);
  --teal:    #0F9B8E;
  --go:      #1E9E52;
  --warn:    #D98324;
  --stop:    #D64545;
  --shadow:  0 1px 2px rgba(13,27,42,.06), 0 8px 24px rgba(13,27,42,.07);
  --shadow-lift: 0 2px 6px rgba(13,27,42,.10), 0 16px 40px rgba(13,27,42,.14);
  /* Flydende flader oven på kortet er halvgennemsigtige og slørede, så man kan
     ane havet bagved. Det er dét, der gør at knapperne hører til kortet i
     stedet for at ligge som et lag papir hen over det. */
  --glass:      rgba(255,255,255,.82);
  --glass-firm: rgba(255,255,255,.94);
  --glass-line: rgba(13,27,42,.09);
  --r:       16px;
  --r-sm:    11px;
  --r-lg:    22px;
}

body.body--dark {
  --sea-1:   #16232F;
  --sea-2:   #0D1B2A;
  --sea-3:   #1E2F42;
  --line:    rgba(240,237,232,.10);
  --line-2:  rgba(240,237,232,.20);
  --txt-1:   #F0EDE8;
  --txt-2:   rgba(240,237,232,.66);
  --txt-3:   rgba(240,237,232,.40);
  --accent:  #E8B96A;
  --accent-soft: rgba(232,185,106,.16);
  --teal:    #4ECDC4;
  --go:      #35B96A;
  --warn:    #E9963B;
  --stop:    #E4645C;
  --shadow:  0 1px 2px rgba(0,0,0,.30), 0 8px 24px rgba(0,0,0,.34);
  --shadow-lift: 0 2px 8px rgba(0,0,0,.38), 0 18px 44px rgba(0,0,0,.46);
  --glass:      rgba(22,35,47,.80);
  --glass-firm: rgba(22,35,47,.93);
  --glass-line: rgba(240,237,232,.12);
}

/* Siden bag app-skallen må hverken rulle eller vokse. */
html, body { height: 100%; overflow: hidden; }
/* App-skallen hænger fast på skærmen i stedet for at ligge i sidens
   almindelige flow.

   Grunden: Quasar lægger appen i et layout med inline `min-height` og en
   `padding-top`, der svarer til headerens højde. Højden dér er et minimum, ikke
   et loft, så et langt panel fik hele kæden til at vokse med sig. Så var der
   intet at rulle i — panelet var jo blevet lige så højt som sit indhold — og
   `overflow: hidden` klippede bunden af. Både sejlplanen og felterne nederst
   blev uopnåelige.

   `position: fixed` med `inset: 0` giver en højde, der altid er skærmens, og
   som ingen inline style kan skubbe til. Alt indeni kan så roligt regne i
   procent og flex. */
.app-shell {
  position: fixed; inset: 0;
  /* dvh følger med, når mobilens adresselinje glider op og ned. */
  height: 100dvh;
  display: flex; flex-direction: column;
  overflow: hidden;
  background: var(--sea-2);
}
/* ═══ Bundskuffe på telefonen ════════════════════════════════════ */
/* På en stor skærm er panelet en spalte. På en telefon er der ikke plads til
   at dele skærmen i to, og kortet er alligevel dét, man peger på — så bliver
   panelet en skuffe, der ligger oven på og kan trækkes op og ned. */
.sheet-grip { display: none; }

/* Kortet skal danne sin egen stak. Leaflet lægger sine lag på z-index 200 til
   1000, og så længe `.mapwrap` står med `z-index: auto`, danner den ikke en
   stak — så konkurrerer kortets lag med resten af siden i stedet for at blive
   inde i kortet. På telefonen ligger skuffen oven på kortet med z-index 20, og
   den tabte til Leaflets 400: man så intet andet end kortet, og der var hverken
   trin, søgefelt eller knap at trykke på. Med en stak her kan kortets tal ikke
   slippe ud, og nul holder hele kortet under skuffen. */
.mapwrap { z-index: 0; }

@media (max-width: 767px) {
  .work { position: relative; }
  .mapwrap { position: absolute; inset: 0; }
  aside.sheet {
    position: absolute; left: 0; right: 0; bottom: 0;
    height: calc(var(--sheet, .58) * (100dvh - var(--header-h)));
    border-radius: 20px 20px 0 0;
    border: 0; border-top: 1px solid var(--line);
    box-shadow: 0 -2px 6px rgba(13,27,42,.06), 0 -14px 40px rgba(13,27,42,.18);
    transition: height .34s cubic-bezier(.22,.9,.3,1);
    z-index: 20;
    /* Skuffen går helt ned til kanten, og på en iPhone ligger hjemmestriben
       dér. Uden det her lå knappen "Find bedste afgangstider" under den. */
    padding-bottom: var(--bottom-inset);
  }
  body.body--dark aside.sheet {
    box-shadow: 0 -2px 8px rgba(0,0,0,.4), 0 -16px 44px rgba(0,0,0,.5);
  }
  /* Mens man trækker, skal skuffen følge fingeren — ikke glide bagefter. */
  .sheet-dragging aside.sheet { transition: none; }

  .sheet-grip {
    display: flex; justify-content: center; align-items: center;
    height: 22px; flex: none;
    cursor: grab; touch-action: none;
  }
  .sheet-grip:active { cursor: grabbing; }
  .sheet-grip i {
    display: block; width: 38px; height: 5px; border-radius: 3px;
    background: var(--line-2);
    transition: background .15s, width .15s;
  }
  .sheet-grip:hover i, .sheet-dragging .sheet-grip i {
    background: var(--txt-3); width: 46px;
  }

  /* Trækker man skuffen næsten helt op, er kortet dækket alligevel. Så skal
     kortknapperne ikke blive stående og stikke halvt op bag skuffekanten —
     halve knapper ser i stykker ud. De træder af og kommer igen, når man
     trækker skuffen ned. */
  .map-tools, .leaflet-control-zoom {
    transition: opacity .22s ease, transform .22s ease;
  }
  .sheet-tall .map-tools, .sheet-tall .leaflet-control-zoom {
    opacity: 0; pointer-events: none; transform: translateY(-8px);
  }

  /* Sejlplanen er et dokument, man læser — på en telefon fylder den skærmen,
     og så har skuffen ingen rolle imens. Den skal væk, ikke ligge bagved: den
     bor inde i kortets stak og kan derfor ikke komme over den. Tilbage til
     afgangene kommer man med Kortet-knappen øverst i planen. */
  .work:has(.plan-view) aside.sheet { display: none; }
}

/* ═══ Skift mellem trin ══════════════════════════════════════════ */
/* Panelet glider den vej, man går. Så kan man mærke om man er på vej frem
   eller tilbage, i stedet for at indholdet bliver skiftet ud under næsen. */
.swap--fwd  { animation: swap-fwd .26s cubic-bezier(.22,.9,.3,1); }
.swap--back { animation: swap-back .26s cubic-bezier(.22,.9,.3,1); }
@keyframes swap-fwd {
  from { opacity: 0; transform: translateX(16px); }
  to   { opacity: 1; transform: none; }
}
@keyframes swap-back {
  from { opacity: 0; transform: translateX(-16px); }
  to   { opacity: 1; transform: none; }
}

.app-header {
  flex: 0 0 auto; height: var(--header-h);
  padding-top: var(--top-inset);
  display: flex; align-items: center; gap: 8px;
  padding: 0 10px;
  background: var(--sea-1);
  border-bottom: 1px solid var(--line);
}
@media (min-width: 768px) { .app-header { padding: 0 16px; } }

.nicegui-content {
  padding: 0 !important; gap: 0 !important; max-width: none !important;
}

body {
  background: var(--sea-2);
  color: var(--txt-1);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  font-feature-settings: 'cv05', 'ss01';
  -webkit-font-smoothing: antialiased;
}

/* Tal skal stå i kolonne, ikke hoppe. */
.tnum, .metric-val, .wx-table td { font-variant-numeric: tabular-nums; }

/* ═══ Grundformer ════════════════════════════════════════════════ */
.card {
  background: var(--sea-1);
  border: 1px solid var(--line);
  border-radius: var(--r);
  box-shadow: var(--shadow);
}
.hairline { border-top: 1px solid var(--line); }

.section-label {
  font-size: 11px; font-weight: 700; letter-spacing: .09em;
  text-transform: uppercase; color: var(--txt-3);
}

/* Flydende boble over kortet — samme glas som knapperne. */
.float {
  background: var(--glass); border: 1px solid var(--glass-line);
  border-radius: 999px; box-shadow: var(--shadow-lift);
  backdrop-filter: blur(18px) saturate(170%);
  -webkit-backdrop-filter: blur(18px) saturate(170%);
}

/* ═══ Søgefelt ═══════════════════════════════════════════════════ */
/* Fyldt frem for kantet. Et søgefelt skal invitere, ikke ligne en formular. */
.q-field--outlined .q-field__control:before { border-color: transparent; }
.search .q-field__control {
  background: var(--sea-3); border-radius: 12px; height: 42px;
}
.search .q-field__control:hover:before { border-color: transparent; }
.search.q-field--focused .q-field__control {
  background: var(--sea-1);
  box-shadow: 0 0 0 2px color-mix(in srgb, var(--accent) 55%, transparent);
}

/* ═══ Trinviser ══════════════════════════════════════════════════ */
.stepbar { display: flex; align-items: center; gap: 4px; }
.step {
  display: flex; align-items: center; gap: 7px;
  padding: 6px 13px 6px 9px; border-radius: 999px;
  font-size: 12.5px; font-weight: 600; color: var(--txt-3);
  border: 1px solid transparent; cursor: pointer;
  transition: background .18s, color .18s, border-color .18s;
  white-space: nowrap;
}
.step:hover:not(.step--locked) { background: var(--sea-3); color: var(--txt-2); }
.step--locked { cursor: not-allowed; opacity: .5; }
.step--done { color: var(--txt-2); }
.step--active {
  background: var(--accent-soft); color: var(--accent);
  border-color: color-mix(in srgb, var(--accent) 38%, transparent);
}
.step-num {
  width: 19px; height: 19px; border-radius: 50%; flex: none;
  display: grid; place-items: center;
  font-size: 10.5px; font-weight: 800;
  background: var(--sea-3); color: var(--txt-3);
}
.step--active .step-num { background: var(--accent); color: var(--sea-1); }
.step--done .step-num { background: var(--go); color: #fff; }
.step-rule { width: 14px; height: 1px; background: var(--line-2); flex: none; }

/* ═══ Waypoint-liste ═════════════════════════════════════════════ */
.wp {
  display: flex; align-items: center; gap: 11px;
  padding: 9px 10px; border-radius: var(--r-sm);
  transition: background .15s;
}
.wp:hover { background: var(--sea-3); }
.wp-pin {
  width: 27px; height: 27px; border-radius: 50%; flex: none;
  display: grid; place-items: center;
  font-size: 11.5px; font-weight: 800; color: #fff;
  box-shadow: 0 1px 4px rgba(0,0,0,.22);
}
.wp-pin--start { background: var(--go); }
.wp-pin--end   { background: var(--stop); }
.wp-pin--via   { background: var(--accent); color: var(--sea-1); }
.wp-name { font-size: 14px; font-weight: 600; line-height: 1.25; }

/* Knapperne i rækken dæmpes kun dér, hvor der er en mus at pege med. På en
   telefon findes hover ikke, og en halvgennemsigtig knap ligner en slukket. */
.wp-tools { opacity: 1; transition: opacity .15s; }
@media (hover: hover) {
  .wp-tools { opacity: .35; }
  .wp:hover .wp-tools { opacity: 1; }
}

/* Ringen der viser hvor et sted i listen ligger på kortet. */
.spot-ring { pointer-events: none; transition: opacity .18s, fill-opacity .18s; }
.wp-meta { font-size: 11.5px; color: var(--txt-3); line-height: 1.35; }

.leg {
  display: flex; align-items: center; gap: 9px;
  margin-left: 23px; padding: 3px 0;
  font-size: 11.5px; color: var(--txt-3);
}
.leg-rule {
  width: 1px; height: 17px; flex: none;
  background: repeating-linear-gradient(to bottom,
    var(--line-2) 0 3px, transparent 3px 6px);
}

/* ═══ Afgangskort ════════════════════════════════════════════════ */
.win {
  position: relative; text-align: left; width: 100%;
  padding: 13px 14px; border-radius: var(--r);
  background: var(--sea-1); border: 1px solid var(--line);
  cursor: pointer; transition: border-color .18s, box-shadow .18s, transform .18s;
}
.win:hover { box-shadow: var(--shadow); transform: translateY(-1px); }
.win--sel {
  border-color: var(--accent);
  box-shadow: 0 0 0 1px var(--accent), var(--shadow-lift);
}
.win-rank {
  position: absolute; top: -7px; left: 13px;
  padding: 1px 8px; border-radius: 999px;
  font-size: 10px; font-weight: 800; letter-spacing: .05em;
  background: var(--accent); color: var(--sea-1);
}
.win--sel .win-rank { background: var(--accent); }
.win-day { font-size: 11.5px; font-weight: 700; color: var(--txt-3);
           text-transform: uppercase; letter-spacing: .05em; }
.win-time { font-size: 27px; font-weight: 700; line-height: 1.05; letter-spacing: -.02em; }
.win-arrive { font-size: 11.5px; color: var(--txt-3); }

/* Overnatninger på afgangskortet. */
.win-stops {
  display: flex; align-items: center; gap: 5px; margin-top: 7px;
  font-size: 11.5px; color: var(--txt-2);
}
.win-stops .material-icons { color: #6C5CE7; }

/* Timestribe: én celle pr. sejltime, farvet efter vejrstatus.
   Timerne uden for sejldøgnet skraveres, så mørket kan ses i stribet. */
.hourbar { display: flex; gap: 1.5px; height: 7px; border-radius: 4px; overflow: hidden; }
.hourbar > i { flex: 1 1 0; min-width: 0; display: block; }
.hourbar > i.night {
  background-image: repeating-linear-gradient(
    45deg, rgba(0,0,0,.42) 0 2px, transparent 2px 4px);
}
.hourbar--tall { height: 11px; }

.chip-ico { font-size: 13px; opacity: .62; }
.chip {
  display: inline-flex; align-items: center; gap: 4px;
  padding: 2px 8px; border-radius: 7px;
  font-size: 11px; font-weight: 600;
  background: var(--sea-3); color: var(--txt-2);
}
.chip--go   { background: color-mix(in srgb, var(--go) 16%, transparent);   color: var(--go); }
.chip--warn { background: color-mix(in srgb, var(--warn) 18%, transparent); color: var(--warn); }
.chip--stop { background: color-mix(in srgb, var(--stop) 16%, transparent); color: var(--stop); }

/* ═══ Sejlplanen ═════════════════════════════════════════════════ */
/* Planen lægger sig hen over kortet. På en telefon er kortfeltet kun godt
   fire tiendedele af skærmen, og et dokument kan ikke læses der — så dækker
   den hele fladen under headeren i stedet. */
.plan-view {
  position: fixed; top: var(--header-h); left: 0; right: 0; bottom: 0;
  /* Over Leaflets egne lag, som gaar til 1000. Planen bor inde i kortets stak,
     saa zoomknapperne laa oven paa dokumentet med 600 herinde. */
  z-index: 1100; background: var(--sea-2);
  animation: plan-in .34s cubic-bezier(.22,.9,.3,1);
}
@keyframes plan-in {
  from { opacity: 0; transform: translateY(10px); }
  to   { opacity: 1; transform: none; }
}
@media (min-width: 768px) {
  .plan-view { position: absolute; top: 0; }
}

.plan-legs { display: grid; grid-template-columns: 1fr; gap: 8px; }
@media (min-width: 1100px) {
  .plan-legs { grid-template-columns: 1fr 1fr; }
}

/* ═══ Dag for dag ════════════════════════════════════════════════ */
/* Sejldøgnene under hinanden, forbundet af en tynd linje — turen læses
   ovenfra og ned, som man sejler den. */
.daylist { display: flex; flex-direction: column; gap: 8px; position: relative; }
.daynum {
  display: inline-grid; place-items: center; flex: none;
  width: 20px; height: 20px; border-radius: 50%;
  font-size: 11px; font-weight: 800;
  background: var(--accent); color: var(--sea-1);
}

/* ═══ Havnene på kortet ══════════════════════════════════════════ */
/* Ikonet er et punkt uden størrelse. Prikken og navnet placeres i forhold til
   det, så etiketten kan stå ved siden af uden at flytte selve positionen. */
.hb-icon { background: none; border: 0; }
.hb { position: relative; display: block; cursor: pointer; }
.hb i {
  position: absolute; left: -4px; top: -4px;
  width: 8px; height: 8px; border-radius: 50%;
  background: #2C7FB8; border: 1.5px solid #fff;
  box-shadow: 0 1px 3px rgba(0,0,0,.45);
  transition: transform .12s;
}
.hb--big i { left: -5px; top: -5px; width: 10px; height: 10px; border-width: 2px; }
.hb:hover i { transform: scale(1.35); }
.hb b {
  position: absolute; left: 9px; top: -8px;
  white-space: nowrap; font-size: 11px; font-weight: 650;
  letter-spacing: -.005em; color: #0D1B2A;
  /* Halo i stedet for en boks: navnet kan læses over både lyst og mørkt kort,
     uden at der ligger en firkant og dækker for søkortet. */
  text-shadow: 0 0 3px #fff, 0 0 3px #fff, 0 0 5px #fff, 0 0 8px #fff;
  pointer-events: none;
}
.hb--big b { font-size: 12px; left: 11px; top: -9px; }
/* Etiketten retter sig efter kortet, ikke efter appen. Havkortet er lyst også i
   mørk tilstand, så dér skal navnene blive ved med at være mørke — kun på det
   mørke landkort vender de om. */
.map-dark .hb b {
  color: #F2F6FA;
  text-shadow: 0 0 3px #0B1622, 0 0 3px #0B1622, 0 0 6px #0B1622, 0 0 9px #0B1622;
}
.hb-tip.leaflet-tooltip {
  background: var(--glass); color: var(--txt-1);
  border: 1px solid var(--line); border-radius: 8px;
  backdrop-filter: blur(14px) saturate(160%);
  box-shadow: var(--shadow);
  font-size: 11.5px; font-weight: 600; padding: 3px 8px;
}
.hb-tip.leaflet-tooltip-top::before { border-top-color: var(--line); }

/* Lille roterende prik til "vi regner på det" uden en hel spinner. */
.spinner-dot {
  width: 12px; height: 12px; flex: none; border-radius: 50%;
  border: 2px solid var(--line-2); border-top-color: var(--accent);
  animation: spin .7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* ═══ Nøgletal ═══════════════════════════════════════════════════ */
.metrics { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1px;
           background: var(--line); border-radius: var(--r); overflow: hidden; }
@media (min-width: 700px) {
  .metrics--wide { grid-template-columns: repeat(6, 1fr); }
}
.metric { background: var(--sea-1); padding: 12px 10px; text-align: center; }
.metric-val { font-size: 19px; font-weight: 700; letter-spacing: -.02em; line-height: 1.15; }
.metric-lbl { font-size: 10.5px; color: var(--txt-3); margin-top: 2px;
              text-transform: uppercase; letter-spacing: .05em; }
.val--go { color: var(--go); } .val--warn { color: var(--warn); } .val--stop { color: var(--stop); }

/* ═══ Vejrtabel ══════════════════════════════════════════════════ */
.wx-table { width: 100%; border-collapse: collapse; font-size: 12.5px; }
.wx-table th {
  position: sticky; top: 0; z-index: 1;
  background: var(--sea-2); color: var(--txt-3);
  font-size: 10.5px; font-weight: 700; letter-spacing: .05em; text-transform: uppercase;
  text-align: left; padding: 7px 8px; border-bottom: 1px solid var(--line);
}
.wx-table td { padding: 6px 8px; border-bottom: 1px solid var(--line); color: var(--txt-2); }
.wx-table tr:hover td { background: var(--sea-3); }
.wx-table .num { font-weight: 650; color: var(--txt-1); }
.wx-day td {
  background: var(--sea-3); font-weight: 700; color: var(--txt-2);
  font-size: 11px; letter-spacing: .05em; text-transform: uppercase;
}
.dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; }

/* ═══ Kort ═══════════════════════════════════════════════════════ */
/* NiceGUI giver kortelementet en fast standardhøjde på 16rem. Den vinder over
   `inset-0`, fordi højde og top/bund tilsammen overbestemmer boksen — så
   kortet blev ved med kun at fylde en stribe. Her tvinges det til at fylde
   sin beholder ud. */
.nicegui-leaflet { height: 100% !important; width: 100% !important; }

.leaflet-container { background: #C3D6E6; font: inherit; }
body.body--dark .leaflet-container { background: #0B1D2C; }
.leaflet-control-attribution { font-size: 10px; opacity: .7; }
.leaflet-control-attribution a { color: inherit; }
body.body--dark .leaflet-control-attribution {
  background: rgba(13,27,42,.72); color: var(--txt-3);
}
/* Søkortsymbolerne fra OpenSeaMap er tegnet til lys bund – løft dem lidt
   i mørk tilstand, så bøjer og fyr stadig kan læses. */
body.body--dark .seamark-tiles { filter: brightness(1.35) saturate(1.15); }

/* Havkortet er lyst af natur. I mørk tilstand dæmpes det til dybblåt, så det
   passer til resten af fladen uden at miste dybdekurverne. */
body.body--dark .chart-tiles { filter: brightness(.74) saturate(1.1) contrast(1.04); }

/* Leaflets egne zoomknapper er hvide firkanter med skarpe hjørner. De stak af
   fra alt andet på kortet, så de får samme glas og samme runding. */
.leaflet-control-zoom {
  border: 1px solid var(--glass-line) !important;
  border-radius: var(--r-sm) !important;
  overflow: hidden; box-shadow: var(--shadow) !important;
  backdrop-filter: blur(18px) saturate(170%);
  -webkit-backdrop-filter: blur(18px) saturate(170%);
}
.leaflet-control-zoom a {
  background: var(--glass); color: var(--txt-2);
  border-color: var(--glass-line);
  width: 32px; height: 32px; line-height: 30px; font-size: 17px;
}
.leaflet-control-zoom a:hover { background: var(--sea-3); }

/* Knapper der svæver over kortet. */
/* Knapper der svæver over kortet. Glasset gør dem lette; skyggen holder dem
   læselige over både et hvidt isbjerg og et mørkeblåt dyb. */
.map-btn {
  background: var(--glass); border: 1px solid var(--glass-line);
  border-radius: var(--r-sm);
  backdrop-filter: blur(18px) saturate(170%);
  -webkit-backdrop-filter: blur(18px) saturate(170%);
  box-shadow: var(--shadow);
  color: var(--txt-2);
  transition: background .16s, color .16s, transform .12s;
}
.map-btn:hover { background: var(--glass-firm); color: var(--txt-1); }
.map-btn:active { transform: scale(.94); }
.map-btn--on { color: var(--accent); background: var(--glass-firm); }
/* Knapperne står i én flade med skillelinjer imellem — som et enkelt stykke
   glas, ikke tre løse klodser der svæver hver for sig. */
.map-stack {
  display: flex; flex-direction: column;
  border-radius: var(--r-sm); overflow: hidden;
  background: var(--glass); border: 1px solid var(--glass-line);
  backdrop-filter: blur(18px) saturate(170%);
  -webkit-backdrop-filter: blur(18px) saturate(170%);
  box-shadow: var(--shadow);
}
.map-stack .map-btn {
  background: none; border: 0; border-radius: 0; box-shadow: none;
  backdrop-filter: none; -webkit-backdrop-filter: none;
}
.map-stack .map-btn + .map-btn { border-top: 1px solid var(--glass-line); }
.map-stack .map-btn:active { transform: none; }
.map-btn--tall { width: 76px; height: 54px; padding: 0; }
.map-btn-label {
  font-size: 9.5px; font-weight: 650; letter-spacing: .01em;
  line-height: 1; white-space: nowrap;
}

/* Den store handlingsknap. Quasar farver den selv efter `primary`, men teksten
   skal være mørk. Hvid på guld giver et kontrastforhold på under 3:1 — det er
   under grænsen for læsbar tekst, og knappen er guld i begge temaer, så farven
   må ikke følge temaet. */
/* Farven sættes på knappens indhold, ikke på knappen. Quasar lægger selv
   `text-white` på selve knappen, og den kamp er ikke værd at tage: en direkte
   regel på indholdet slår altid en nedarvet farve, uanset hvem der råber
   højest med !important. */
.btn-primary.q-btn { font-weight: 700; }
.btn-primary .q-btn__content { color: #12212F !important; }

/* ═══ Segmentvælger ══════════════════════════════════════════════ */
/* To valg, ét spor, og en markør der glider. Den fylder mindre end to knapper
   og siger tydeligere, at man vælger mellem dem — ikke trykker på dem begge. */
.seg {
  display: inline-flex; padding: 3px; gap: 2px;
  background: var(--glass); border: 1px solid var(--glass-line);
  border-radius: 999px; box-shadow: var(--shadow);
  backdrop-filter: blur(18px) saturate(170%);
  -webkit-backdrop-filter: blur(18px) saturate(170%);
}
.seg-item {
  padding: 5px 13px; border-radius: 999px;
  font-size: 12px; font-weight: 600; color: var(--txt-3);
  cursor: pointer; user-select: none; white-space: nowrap;
  transition: background .18s, color .18s;
}
.seg-item:hover { color: var(--txt-1); }
.seg-item--on {
  background: var(--sea-1); color: var(--txt-1);
  box-shadow: 0 1px 3px rgba(13,27,42,.14);
}
body.body--dark .seg-item--on { box-shadow: 0 1px 3px rgba(0,0,0,.5); }

.wp-marker {
  display: grid; place-items: center;
  width: 30px; height: 30px; border-radius: 50%;
  font-size: 12px; font-weight: 800; color: #fff;
  border: 2.5px solid rgba(255,255,255,.92);
  box-shadow: 0 2px 10px rgba(0,0,0,.42);
  transition: transform .15s;
}
.wp-marker:hover { transform: scale(1.14); }
.wp-marker--start { background: #1E9E52; }
.wp-marker--end   { background: #D64545; }
.wp-marker--via   { background: #C8933B; }

/* ═══ AI-analyse ═════════════════════════════════════════════════ */
.ai-text { font-size: 14px; line-height: 1.68; color: var(--txt-2); }
.ai-text h2 {
  font-size: 12px; font-weight: 700; letter-spacing: .07em; text-transform: uppercase;
  color: var(--accent); margin: 22px 0 7px;
}
.ai-text h2:first-child { margin-top: 0; }
.ai-text p { margin: 0 0 11px; }
.ai-text strong { color: var(--txt-1); font-weight: 650; }
.ai-text ul { margin: 0 0 11px; padding-left: 19px; }
.ai-text li { margin-bottom: 4px; }
/* Blinkende markør mens svaret streames ind. */
.ai-text.is-streaming > *:last-child::after {
  content: ''; display: inline-block; width: 7px; height: 1.05em;
  margin-left: 2px; vertical-align: text-bottom;
  background: var(--accent); animation: blink 1.05s step-end infinite;
}
@keyframes blink { 50% { opacity: 0; } }

/* ═══ Tomme tilstande ════════════════════════════════════════════ */
.empty { text-align: center; padding: 34px 22px; }
.empty-title { font-size: 15px; font-weight: 650; margin-bottom: 5px; }
.empty-sub { font-size: 13px; color: var(--txt-3); line-height: 1.55; max-width: 30ch;
             margin: 0 auto; }

/* ═══ Diverse ════════════════════════════════════════════════════ */
/* `overflow-x: clip` fordi glide-animationen ellers kan blinke med en
   vandret rullebjælke, mens indholdet står 16 px ude til siden. */
.scroll-y { overflow-y: auto; overflow-x: clip; overscroll-behavior: contain; }
.scroll-y::-webkit-scrollbar { width: 9px; height: 9px; }
.scroll-y::-webkit-scrollbar-thumb {
  background: var(--line-2); border-radius: 5px;
  border: 2px solid transparent; background-clip: content-box;
}
.scroll-y::-webkit-scrollbar-track { background: transparent; }

.q-field--outlined .q-field__control { border-radius: var(--r-sm); }
.q-btn { text-transform: none; font-weight: 600; letter-spacing: 0; }

/* Reducér bevægelse for dem, der har bedt om det. */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: .01ms !important; transition-duration: .01ms !important; }
}
"""


def palette(dark: bool = False) -> None:
    """Giv Quasar appens egne farver.

    Quasars hjælpeklasser — `bg-primary`, `text-primary` — er sat med
    `!important`, så en klasse udefra kan ikke overtrumfe dem. Resultatet var,
    at hver eneste knap, kontakt, skyder og spinner stod i Quasars standardblå
    midt i en flade, der ellers var guld og hav. Vi sætter farverne dér, hvor
    Quasar selv henter dem, i stedet for at kæmpe med dem bagefter.
    """
    ui.colors(primary=GOLD_DARK if dark else GOLD,
              secondary=TEAL_DARK if dark else TEAL,
              accent=GOLD_DARK if dark else GOLD,
              positive=GREEN, negative=RED, warning=AMBER)


def apply() -> None:
    """Indlæs skrifttype og stilark. Kaldes én gang pr. side."""
    palette()
    ui.add_head_html(
        '<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link rel="stylesheet" '
        'href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap">')
    ui.add_css(CSS)
