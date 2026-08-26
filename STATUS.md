# Sejlplan — status

Sidst opdateret 24. august 2026.

Kører på <https://sejlplan-production.up.railway.app>. Udrulning sker
automatisk ved push til `main`.

---

## Hvad systemet kan

**Rute over vand.** Man sætter punkter ved at søge, klikke på kortet eller
vælge en havn, og ruten lægges uden om land med en bitpakket landmaske bygget
af GSHHG-kystlinjer. A\* med blød landomkostning, snoretræk og lokal
finjustering. Ét ben ad gangen, i en baggrundstråd.

**Vejr sammen med ruten.** Vind, vindstød, bølgehøjde, bølgeretning og
strøm hentes fra Open-Meteo i op til tolv punkter langs ruten. Prognosen
rækker ti døgn — bølgerne er loftet, ikke vinden.

**Sejldøgnet som bærende begreb.** Sluttidspunktet er, hvornår man vil ligge
fortøjet, ikke hvornår man må afgå. Rækker turen ikke, deles den, og der findes
en havn undervejs at overnatte i.

**Afgangstider.** Hver time i vinduet regnes igennem. De, der ender forskelligt,
vises alle — og hver dag, man overhovedet kan sejle, er repræsenteret.
Rækkefølgen er en anbefaling, ikke en afgørelse.

**Sejlplanen** i syv afsnit, der kan klappes sammen: overblik, advarsler i tre
alvorsgrader, nøgletal, dag for dag, stræk for stræk delt efter kursskift, time
for time, og en AI-skrevet skippervurdering.

**Både.** Syv eksempler, egen båd, og et register på 127 sejlbåde fra danske og
nordiske havne. Farten anslås af sejlareal, deplacement og vandlinje.

**Blæst inde.** Fra ankomsten og til prognosen slipper op tælles det efter, om
der er et sejlbart døgn tilbage på destinationen.

**Vejrvagt.** Læg en tur og et datovindue, og få én mail når vejret er der —
også hvis vinduet ligger længere ude, end prognosen rækker i dag.

**Er der plads i havnen.** Tre knapper, anonymt, ingen fritekst. Meldinger dør
efter halvandet døgn. **Lukket lige nu** — se Fællesskabet nedenfor.

**Fællesskabet — bygget, men lukket.** Tre funktioner kræver, at der er andre
derude: pladsmeldingerne, bådene på kortet ("Vis min båd for andre" og listen
over dem i nærheden), og beskederne mellem både. De er færdige og prøvet af,
men de står lukkede, til der er brugere nok. En flåde med én båd i er ikke en
halv flåde — den fortæller den første bruger, at han er alene, og det er det
indtryk, han tager med sig.

Lukket betyder væk, ikke gråt: ingen knapper, intet kortlag, og ingen afsnit i
manualen om noget, man ikke kan finde. Teksterne bliver stående i koden og i
begge oversættelser, så de er klar den dag, kontakten bliver sat.

De åbnes hver for sig, for tærsklen er ikke den samme. En pladsmelding hjælper
den næste, der kommer til havnen, allerede når vi er få; bådene på kortet
giver først mening, når der er nogen at se. Beskederne kan ikke åbnes alene —
samtalen begynder ved at trykke på en båd på kortet.

```
SEJLPLAN_PLADSMELDING=til     # lavest tærskel — åbn den først
SEJLPLAN_FLAADE=til           # både på kortet
SEJLPLAN_BESKEDER=til         # kræver at flåden er åben
```

Alt andet end et tydeligt ja er et nej — også en stavefejl. Serveren skriver i
opstartslinjen, hvad der er åbent og lukket, og `/api/status` siger det samme,
så en lukket funktion aldrig kommer til at ligne en, der er i stykker.

**App og uden dækning.** Manifest, ikoner, service worker. Den seneste sejlplan
lægges i telefonen som ét selvstændigt dokument og kan læses uden forbindelse.

**Mine ruter, GPX, delelink, havneguide-links** (515 havne koblet til
havnelods.dk på position), **manual og hjælpebobler** fra ét sæt tekster.

---

## Hvad der mangler

### 1. Der er få tests

`tests/` har syv filer og 648 prøver. Det er langtfra nok, men de fleste findes,
fordi de fanger noget, der faktisk gik galt.

`test_dokumenter.py` findes, fordi den offline sejlplan var brudt i stilhed:
`warnings()` giver Note-objekter, ikke tekst, så
hver plan med en advarsel rejste AttributeError, når den skulle lægges i
telefonen — og planlæggeren sluger den fejl med vilje. Knappen virkede,
dokumentet blev bare aldrig gemt. Hele grunden til at have en PWA var væk, og
ingen kunne se det.

Det er stadig den største risiko i projektet. Seks talfejl er fundet og rettet
undervejs — snitfarten talte timer to gange, båden sejlede fem knob lige op i
vinden, sejltiden passede ikke med farten, planen påstod en ankomst den ikke
havde, havnetjekket kasserede de nærmeste havne, og en dom blev slået op i en
tabel med en oversat nøgle, så fladen ville vælte på ethvert andet sprog end
dansk. Alle seks sad i kode, der så rigtig ud.

### 2. Strømmen er for svag

Open-Meteos globale havmodel opløser ikke de danske bælter. Målt over syv døgn:
højst 0,9 knob i Storebælt og 1,0 i Grønsund, hvor der i virkeligheden løber
to-tre. Retningen er rigtig, styrken er for lav — det står i fladen og i
hjælpen. Den rigtige kilde er DMI's DKSS-model. Hentningen ligger samlet i
`weather.py`, så et skifte rører ikke resten.

### 3. Dybgang og grunde

Bådregistret kender dybgangen. Ruten går uden om land, ikke uden om grunde. Det
eneste rene sikkerhedspunkt på listen.

Sømærkeopslaget siger nu udtrykkeligt, at vi ikke advarer om grunde, og
hvorfor: masken kender kysten, ikke dybderne, og en advarsel, der ser rigtig ud
og er forkert, er farligere end ingen. Det er den ærlige udgave, ikke en
løsning. Løsningen er dybdedata fra et rigtigt søkort.

### 4. Ingen konti og ingen betaling

Alt ligger i én browser. Gemte ruter findes ikke på telefonen, hvis de blev
lavet på computeren. Skippervurderingen har ingen forbrugsgrænse — nøglen er
serverens, og enhver kan trykke.

### 5. Data, der skal efterses

De 127 bådes mål er fabrikanternes nominelle tal, samlet af Claude ud fra egen
viden. Polardiagrammet er et skaleret gennemsnit, ikke en måling. Havneregistret
er OpenStreetMap: skæve navne, manglende pladstal, og enkelte punkter der ikke
er havne.

### 6. Afhængigheder — låst nu

`requirements.txt` sagde `nicegui>=2.10`, så Railway installerede den nyeste
ved hver udrulning. Produktionen kørte 3.16, mens prøverne kørte 3.13 — koden
blev altså aldrig afprøvet i den udgave, brugerne fik, og en ny udgivelse kunne
vælte fladen uden at nogen havde rørt en linje. Alle fem pakker er nu låst til
det, prøverne kører imod. En opdatering er en ændring for sig.

### 7. Det juridiske

Ingen betingelser, ingen privatlivspolitik. Skal på plads før den første
betaling. Og havnelods.dk bør have besked om, at vi linker til dem.

### 8. Motorbåde

Bådregistret er kun sejlbåde. Der mangler omkring hundrede motorbåde, før en
motorbådsfører kan finde sin egen.

### 9. Sprog

Dansk, tysk og svensk, 939 tekster, alle oversat på begge fremmedsprog: fladen,
hjælpeemnerne, manualen, sømærkerne og VHF-guiden, sejlplanens egen tekst, den
offline plan, vejrvagtens mails og skippervurderingen.
`python tools/check_translations.py` gennemgår hvert sprog for sig og siger,
hvad der mangler, når en dansk sætning bliver rettet.

Oversat, ikke maskinoversat. Sejldøgn er Etmal, ikke Segeltag. Beauforts skala
har de navne, der står i en tysk farvandsudsigt. Sætninger er bygget hele, for
tysk bøjer efter køn og kasus: "halvvind" er "halber Wind" alene, men "bei
halbem Wind" inde i en sætning, og de to former slås op hver for sig.

Svensk er farligere end tysk, netop fordi det ligner: *mil* er ti kilometer på
svensk, så en distance i "sjömil" kan læses ti gange for stor. Søkortets ord
er *distansminut* (M), og det er dét, der står. *Slör* er ikke "rumskøds"
oversat, det er dét, en svensker siger, og bomholderen hedder
*preventerlina*.

Vindskalaen er svensk, ikke oversat. Til søs hedder Beaufort 7–9 kuling, storm
begynder først ved 10, og orkan ved 12 — altså over 63 knob. Skalaen er derfor
forskudt et trin i forhold til den danske: hvor der står "Storm" på dansk ved
45 knob, står der *halv storm* på svensk, og "Orkan" ved 50 er *storm*. Et
tal, der hedder orkan på svensk, er noget andet end et tal, der hedder orkan
på dansk, og en svensk sejler kender forskellen.

Tre danske ord dækker hver især to ting, som svensk skiller ad. *Undervejs* er
tiden fra kaj til kaj (*till sjöss*), det der ligger langs ruten (*längs
vägen*), og det at være i gang (*till sjöss*). *Ben* er fra punkt til punkt
(*etapp*), *stræk* er det stykke, kursen holder (*sträcka*) — blev begge til
"sträcka", stod der i manualen, at en sträcka deles op i sträckor. Og *meld
plads* er en *rapport*; *anmäla* er dét, man gør ved en, der har opført sig
dårligt, og det ord hører til på knappen ved siden af en besked.

Prøverne henter sproglisten fra `i18n.LANGUAGES`, ikke fra en håndskrevet
liste: siden, de tre dokumenter, sømærkerne, VHF-guiden og manualen bygges på
hvert sprog, der står i vælgeren. Et fjerde sprog er dækket fra den dag, det
lægges ind.

Det, der ikke oversættes: punkternes navne. Lægger man "Ud for Køge" ind på
dansk og skifter til tysk, står der stadig "Ud for Køge" — det er gemt tekst,
ikke en etikette. Et nyt punkt får sit tyske navn.

Et tredje sprog koster nu kun ordene: `app/lang/` og en linje i `LANGUAGES`.

---

## Opsætning i skyen

Sat op: volume `sejlplan-volume` på `/data`, `SEJLPLAN_DATA_DIR`,
`SEJLPLAN_SITE_URL`, `SEJLPLAN_STORAGE_SECRET`, `ANTHROPIC_API_KEY`.

**Mangler:** SMTP. Uden disse er vejrvagten slået fra, og fladen siger det.

```
SEJLPLAN_SMTP_HOST=
SEJLPLAN_SMTP_PORT=587
SEJLPLAN_SMTP_USER=
SEJLPLAN_SMTP_PASSWORD=
SEJLPLAN_MAIL_FROM=sejlplan@dit-domæne.dk
```

Brug et domæne, du selv styrer. Mails fra en fremmed afsender ender i spam, og
en vejrvagt i spamfilteret er ingen vejrvagt.

---

## Værktøjer

Datafilerne bygges af scripts i `tools/` og er lagt i repoet, så serveren ikke
skal hente noget ved opstart.

| Script | Bygger |
|---|---|
| `build_landmask.py` | `app/data/landmask.bin` — kyster fra GSHHG |
| `build_harbours.py` | `app/data/harbours.json.gz` — 3318 havne fra OSM |
| `build_harbour_links.py` | `app/data/harbour_links.json` — kobling til havnelods.dk |
| `build_icons.py` | `app/static/*.png` — app-ikoner |

`app/data/sailboats.json` er håndholdt. En rettelse er én linje.
