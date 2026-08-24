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
efter halvandet døgn.

**App og uden dækning.** Manifest, ikoner, service worker. Den seneste sejlplan
lægges i telefonen som ét selvstændigt dokument og kan læses uden forbindelse.

**Mine ruter, GPX, delelink, havneguide-links** (515 havne koblet til
havnelods.dk på position), **manual og hjælpebobler** fra ét sæt tekster.

---

## Hvad der mangler

### 1. Der er næsten ingen tests

`tests/test_dokumenter.py` er den eneste. Den findes, fordi den offline
sejlplan var brudt i stilhed: `warnings()` giver Note-objekter, ikke tekst, så
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

### 3. Dybgang bruges ikke

Bådregistret kender dybgangen. Ruten går uden om land, ikke uden om grunde. Det
eneste rene sikkerhedspunkt på listen.

### 4. Ingen konti og ingen betaling

Alt ligger i én browser. Gemte ruter findes ikke på telefonen, hvis de blev
lavet på computeren. Skippervurderingen har ingen forbrugsgrænse — nøglen er
serverens, og enhver kan trykke.

### 5. Data, der skal efterses

De 127 bådes mål er fabrikanternes nominelle tal, samlet af Claude ud fra egen
viden. Polardiagrammet er et skaleret gennemsnit, ikke en måling. Havneregistret
er OpenStreetMap: skæve navne, manglende pladstal, og enkelte punkter der ikke
er havne.

### 6. Det juridiske

Ingen betingelser, ingen privatlivspolitik. Skal på plads før den første
betaling. Og havnelods.dk bør have besked om, at vi linker til dem.

### 7. Motorbåde

Bådregistret er kun sejlbåde. Der mangler omkring hundrede motorbåde, før en
motorbådsfører kan finde sin egen.

### 8. Sprog

Dansk og tysk, 573 tekster, alle oversat: fladen, de 24 hjælpeemner, manualen,
sejlplanens egen tekst, den offline plan, vejrvagtens mails og
skippervurderingen. `python tools/check_translations.py` siger, hvad der
mangler, når en dansk sætning bliver rettet.

Oversat, ikke maskinoversat. Sejldøgn er Etmal, ikke Segeltag. Beauforts skala
har de navne, der står i en tysk farvandsudsigt. Sætninger er bygget hele, for
tysk bøjer efter køn og kasus: "halvvind" er "halber Wind" alene, men "bei
halbem Wind" inde i en sætning, og de to former slås op hver for sig.

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
