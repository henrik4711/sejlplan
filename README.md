# Sejlplan

Vejrbaseret ruteplanlægning for lystsejlere og motorbådsfolk. Læg en rute i
danske og skandinaviske farvande, og få at vide hvornår du bør kaste los — og
hvor du skal ligge undervejs, hvis turen ikke kan nås på én dag.

Appen lægger ruten **udenom land**, henter vind- og bølgeprognoser for hvert
ben, sejler turen igennem time for time for hvert muligt afgangstidspunkt, og
rangerer resultatet efter hvad der faktisk gør en sejlads ubehagelig: timer over
dine komfortgrænser, mørkesejlads, overnatninger undervejs og samlet varighed.

## Kom i gang

```bash
pip install -r requirements.txt
cp .env.example .env      # udfyld ANTHROPIC_API_KEY hvis AI-analysen skal med
python main.py
```

Åbn derefter <http://localhost:8090>.

Appen kører fint uden `.env` — så er alt med undtagelse af AI-analysen aktivt.
Der er ingen datafiler at hente: kystlinjer og havneregister ligger i repoet.

## Sådan bruges den

Tre trin, i den rækkefølge man planlægger i:

1. **Rute** — søg efter en havn, klik på kortet, eller slå havnelaget til og vælg
   blandt godt 3.000 lystbådehavne. Markørerne kan trækkes rundt, og et nyt
   punkt lægger sig selv dér i ruten, hvor det koster mindst omvej. Ruten lægges
   automatisk udenom land, og du kan se hvor mange sømil det koster.
2. **Afgang** — de ti bedste afgangstidspunkter, hver med en farvet timestribe
   der viser vejret undervejs, og de overnatninger turen kræver. Vælg det, der
   passer.
3. **Sejlplan** — dag for dag, stræk for stræk, time for time, nøgletal og en
   skippervurdering skrevet af Claude.

Ruten kan deles som link og hentes som GPX til kortplotteren — med alle de knæk,
ruteberegningen har lagt ind for at komme udenom land.

## De tre ting der bærer appen

### Ruten holder sig i vandet

`app/data/landmask.bin` er et gitter over skandinaviske farvande med én bit pr.
celle på ca. 200 × 125 meter, bygget af GSHHG's kystlinjer i fuld opløsning.
`searoute.py` finder vejen i tre trin: en grovsøgning der finder det rigtige
farvand, en udglatning der skærer trappemønsteret væk, og en finsøgning der
lægger de sidste knæk om, hvor grovsøgningen skar et hjørne. En tur over
Kattegat regnes på under et sekund.

Alt vand, der ikke hænger sammen med havet, er lukket i gitteret. Det lyder
teknisk, men det er dét, der gør at ruteberegningen kan lægge til i Rønne: uden
det ville havnebassinet bag molerne være en lille sø, man aldrig kunne nå.

### Sejldøgnet, ikke afgangstidspunktet

Siger du, at du vil være i havn senest kl. 20, er det ikke et ønske om at afgå
senest kl. 20. Det er et krav om at ligge fortøjet kl. 20. Rækker turen ikke,
deler `sailing.sail()` den op og finder en havn undervejs at overnatte i — den
man kommer længst med og stadig kan nå inden dagen er omme. Kan ingen havn nås,
siger planen det ligeud i stedet for at lade som om.

Vil du hele vejen i én stræk, slår du mørkesejlads til, og så lægges der ingen
ophold ind.

### Planen gælder dér, hvor du styrer

Sætter du Køge og Præstø ind, er det ét ben — men det sejles mod sydøst, så mod
syd og til sidst mod vest. Derfor deles ruten op efter **kursskift**, ikke efter
hvor du satte et kryds, og hvert stræk får sin egen kurs, sejlføring og
søretning. Det er dét, der gør forskellen på "kurs 126°, læns" og virkeligheden,
hvor du efter Stevns ligger i skarp bidevind.

Vejrudsigten hentes tilsvarende for punkter langs den rute, der faktisk sejles —
ét for hver ~18 sømil — ikke for rutens midtpunkt.

### Motorbåd og sejlbåd regnes ikke ens

En sejlbåd får sin fart fra polardiagrammet: vindvinkel og vindstyrke. En
motorbåd har en marchfart, og det afgørende er søen. En planende båd, der gør 24
knob i smult vande, gør 10 i halvanden meters modsø — og det er dét, planen
regner med. Bølgehøjden vejes efter hvor søen kommer fra, så modsø tæller
hårdere end medsø, både for farten og for komforten.

Motorbådsplanen fortæller også hvad turen koster i brændstof, og hvordan den
kommer til at føles.

## Konfiguration

Alt sættes i `.env` — se `.env.example` for den fulde liste.

| Variabel | Betydning |
|---|---|
| `ANTHROPIC_API_KEY` | Slår AI-analysen til. Uden den skjuler fanen sig pænt. |
| `SEJLPLAN_AI_MODEL` | Standard `claude-opus-5`. |
| `SEJLPLAN_STORAGE_SECRET` | Signerer brugersessioner. Sæt en lang tilfældig streng i drift. |
| `SEJLPLAN_PORT` | Standard `8090`. Er den ikke sat, bruges `PORT` — det er den, Railway og lignende platforme sætter. |
| `SEJLPLAN_CONTACT` | Mail der sendes med i User-Agent til de eksterne tjenester. |

## Drift

`railway.toml` starter appen med `python main.py`, og porten kommer fra `PORT`.
Sæt `SEJLPLAN_STORAGE_SECRET` og `ANTHROPIC_API_KEY` som miljøvariabler på
platformen — ikke i repoet. Uden et fast `SEJLPLAN_STORAGE_SECRET` får serveren
en ny hemmelighed ved hver udrulning, og så mister alle deres gemte rute.

## Flere brugere

Alle der åbner adressen får deres eget arbejdsområde. Der er ingen login:
`@ui.page` kører én gang pr. besøgende, så hver `Planner` og `Session` tilhører
netop den ene browser. Rute, båd og grænser gemmes i browserens session og
overlever en genindlæsning.

Vejrsvar caches på serveren i 30 minutter pr. område, så mange samtidige
brugere deler de samme kald til Open-Meteo. Kystlinjegitteret og havneregisteret
læses én gang og deles af alle.

Sætter du appen på det åbne internet, så husk et rigtigt
`SEJLPLAN_STORAGE_SECRET` og en omvendt proxy med HTTPS foran.

## Opbygning

```
main.py              opstart
app/
  config.py          indstillinger fra .env
  boats.py           sejlbåde med polardiagram, motorbåde med marchfart
  landmask.py        land/vand-gitteret: er der vand her, og er linjen fri?
  searoute.py        ruten udenom land
  harbours.py        havneregisteret: søgning, kortudsnit og overnatninger
  sailing.py         navigation, fart, sejldøgn og rangering af afgange
  weather.py         Open-Meteo, punkter langs ruten, med cache
  geocode.py         stedsøgning oven på havneregisteret
  ai.py              skippervurdering via Claude, streamet
  dates.py           danske dato- og klokkeslætsformater
  narrative.py       planen skrevet ud i klar tekst
  share.py           delelink og GPX-eksport
  state.py           tilstand pr. bruger
  theme.py           designsystem
  data/
    landmask.bin     kystlinjer som bitgitter
    harbours.json.gz havneregisteret
  ui/
    page.py          sidedefinition
    planner.py       de tre trin
    mapview.py       kortet, ruten, havnene og markørerne
    settings.py      båd, grænser og sejldøgn
tools/
  build_landmask.py  bygger data/landmask.bin af GSHHG
  build_harbours.py  bygger data/harbours.json.gz af OpenStreetMap
```

## Datafilerne

De to filer i `app/data/` følger med i repoet og opdateres sjældent. Skal de
bygges om:

```bash
# Kystlinjer: hent gshhg-bin-2.3.7.zip, pak gshhs_f.b ud
python tools/build_landmask.py ~/Downloads/gshhs_f.b

# Havne: hent marinaer fra Overpass i tern, og Natural Earths landegrænser
python tools/build_harbours.py marinas.json countries.geojson
```

`build_landmask.py` bruger også `scipy`; appen selv nøjes med `numpy`.

## Eksterne tjenester

Ingen af dem kræver en nøgle, og ingen af dem bruges til ruteberegningen —
den kører helt lokalt.

- **Open-Meteo** — vind, vindstød, bølgehøjde og bølgeretning, samt stedsøgning
- **Esri Ocean / GEBCO / NOAA** — havkort med dybdeforhold
- **CARTO / OpenStreetMap** — landkort
- **OpenSeaMap** — bøjer, fyr og sejlløb

## Datakilder

- Kystlinjer: [GSHHG](https://www.soest.hawaii.edu/pwessel/gshhg/) 2.3.7, LGPL
- Havne: [OpenStreetMap](https://www.openstreetmap.org/copyright), ODbL
- Landegrænser: [Natural Earth](https://www.naturalearthdata.com/), public domain

## Forbehold

Prognoser er prognoser, og et kystlinjegitter er ikke et søkort. Appen lægger
ruten udenom land, men den kender hverken dybder, sejlløb, broåbningstider,
strøm, tidevand eller afmærkning. Den erstatter ikke søkort, farvandsudsigt
eller almindelig sømandskab. Ansvaret for turen er skipperens.
