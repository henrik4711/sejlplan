"""Svensk.

Nøglen er den danske sætning, præcis som den står i koden. Mangler en, står
den danske i stedet — fladen virker, den er bare ikke oversat dér endnu.
`tools/check_translations.py --sprog sv` siger hvilke.

**Om sømil.** På svensk betyder *mil* ti kilometer, og "sjömil" er derfor
tvetydigt: en svensker kan læse 37 sjömil som 370 km. Søkortets og
Sjöfartsverkets ord er *distansminut*, forkortet M, og det er dét, der bruges
her — netop fordi tvetydigheden er farlig i en sejlplan.

Oversat, ikke maskinoversat. Dansk og svensk ligner hinanden nok til at gøre
det farligt: *slör* er ikke "rumskøds" oversat, det er dét, en svensker siger,
og *preventerlina* er det svenske ord for en bomholder.
"""

WORDS: dict[str, str] = {
    'Tryk Find bedste afgangstider først, og vælg en afgang. Så '
        'skriver vi sejlplanen.':
        'Tryck först på Hitta bästa avgångstider och välj en avgång. Då '
        'skriver vi seglingsplanen.',
    '{sm} sømil · kurs {grader}° {retning}':
        '{sm} distansminuter · kurs {grader}° {retning}',
    'Lægger ruten udenom land…':
        'Lägger rutten runt land…',
    'Klik på kortet, eller søg efter en havn, for at sætte '
        'afgangshavnen':
        'Klicka på kartan, eller sök efter en hamn, för att sätta '
        'avgångshamnen',
    'Klik igen for at sætte destinationen':
        'Klicka igen för att sätta destinationen',
    'Læg først en rute med mindst to punkter — så kan vi regne '
        'afgangstider ud.':
        'Lägg först en rutt med minst två punkter — då kan vi räkna ut '
        'avgångstider.',
    'Hele sejlplanen er kopieret':
        'Hela seglingsplanen är kopierad',
    'Punkt {nr} flyttet til {navn}':
        'Punkt {nr} flyttad till {navn}',
    'Ruten er vendt om':
        'Rutten är vänd',
    '"{navn}" er åbnet':
        '”{navn}” är öppnad',
    'Henter vejrudsigt for hvert ben…':
        'Hämtar väderprognos för varje etapp…',
    'Finder havne undervejs og gennemsejler alle afgangstider…':
        'Söker hamnar längs vägen och räknar igenom alla avgångstider…',
    'Claude læser vejrudsigten…':
        'Claude läser väderprognosen…',
    'Delelink kopieret — send det til gasterne':
        'Delningslänk kopierad — skicka den till gastarna',
    'Søkortsymboler vist':
        'Sjökortssymboler visas',
    'Søkortsymboler skjult':
        'Sjökortssymboler dolda',
    'Havnene vises, når du zoomer ind. Klik på en for at lægge den i '
        'ruten.':
        'Hamnarna visas när du zoomar in. Klicka på en för att lägga in '
        'den i rutten.',
    'Havnene er skjult':
        'Hamnarna är dolda',
    '{sm} sm udenom land':
        '{sm} M runt land',
    '{kn} kn vind · {m} m bølger':
        '{kn} kn vind · {m} m vågor',
    'Kunne ikke finde positionen.':
        'Kunde inte hitta positionen.',
    'Ruten er ændret — find afgangstiderne igen':
        'Rutten är ändrad — sök avgångstiderna igen',
    '{navn} tilføjet':
        '{navn} tillagd',
    '{navn} lagt ind som stop nr. {nr}':
        '{navn} inlagd som stopp nr {nr}',
    'Som ny destination, efter {navn}':
        'Som ny destination, efter {navn}',
    'Som ny afgang, før {navn}':
        'Som ny avgång, före {navn}',
    'Ruten kunne ikke åbnes':
        'Rutten kunde inte öppnas',
    'Tilføj mindst to punkter først':
        'Lägg till minst två punkter först',
    'Ingen afgange passer til dine grænser. Prøv et bredere '
        'datointerval, et længere sejldøgn eller en højere vindgrænse.':
        'Ingen avgång passar dina gränser. Prova ett bredare '
        'datumintervall, ett längre etmål eller en högre vindgräns.',
    'Turen kan ikke nås inden kl. {tid}:00. Se forslagene — de fleste '
        'kræver en overnatning undervejs.':
        'Resan går inte att hinna före kl. {tid}:00. Se förslagen — de '
        'flesta kräver en övernattning längs vägen.',
    'Der er ingen rute at dele endnu':
        'Det finns ingen rutt att dela ännu',
    'Der er ingen rute at eksportere endnu':
        'Det finns ingen rutt att exportera ännu',
    'Ingen steder hedder "{navn}". Prøv et andet navn, eller tast en '
        'position som 55.69, 12.60.':
        'Ingen plats heter ”{navn}”. Prova ett annat namn, eller skriv en '
        'position som 55.69, 12.60.',
    '{afgange} at vælge imellem, fordelt på {dage}. Vi vil pege på '
        '<b>{bedste}</b> — men vælg selv.':
        '{afgange} att välja mellan, fördelat på {dage}. Vi pekar på '
        '<b>{bedste}</b> — men välj själv.',
    'stræk':
        'sträckor',
    'Kraftigst omkring {tid}: {kn} kn ({styrke}) fra {retning}, kast '
        'op til {kast} kn.':
        'Kraftigast omkring {tid}: {kn} kn ({styrke}) från {retning}, '
        'byar upp till {kast} kn.',
    'Der er land her. Vælg et sted i vandet, eller søg efter en havn.':
        'Här är land. Välj en plats i vattnet, eller sök efter en hamn.',
    'Som nyt punkt':
        'Som ny punkt',
    'Mellem {a} og {b}':
        'Mellan {a} och {b}',
    '{afgange} fundet. Turen kræver {overnatninger} undervejs — '
        'første stop i {havn}.':
        '{afgange} hittade. Resan kräver {overnatninger} längs vägen — '
        'första stoppet i {havn}.',
    '{n} afgangstider fundet':
        '{n} avgångstider hittade',
    'Havkort med dybdeforhold':
        'Sjökort med djupförhållanden',
    'Almindeligt kort med veje og byer':
        'Vanlig karta med vägar och orter',
    'Vis alle lystbådehavne — klik på en for at lægge den i ruten':
        'Visa alla småbåtshamnar — klicka på en för att lägga in den i '
        'rutten',
    'Bøjer, fyr og sejlløb fra OpenSeaMap':
        'Bojar, fyrar och farleder från OpenSeaMap',
    'Zoom ud, så hele ruten er i billedet':
        'Zooma ut så att hela rutten syns',
    'Fremme efter sejldøgnet':
        'Framme efter etmålet',
    '{n} t frarådes':
        '{n} tim avrådes',
    '{n} t skærpet':
        '{n} tim skärpt',
    'Planen står til højre. Vælg en anden afgang her, så skrives den '
        'om med det samme.':
        'Planen står till höger. Välj en annan avgång här, så skrivs den '
        'om med detsamma.',
    'sm':
        'M',
    'Farten er over grunden — strømmen er regnet med, og står i '
        'søjlen Strøm: {kn} knob {retning} i snit. Tallene kommer fra en '
        'global havmodel, der ikke opløser de danske bælter helt. I '
        'Storebælt og Grønsund kan der løbe mere, end den viser.':
        'Farten är över grund — strömmen är inräknad och står i kolumnen '
        'Ström: {kn} knop {retning} i snitt. Siffrorna kommer från en '
        'global havsmodell som inte löser upp de danska bälten helt. I '
        'Stora Bält och Grönsund kan det löpa mer än den visar.',
    'Meld om der er plads i en havn omkring dig':
        'Rapportera om det finns plats i en hamn omkring dig',
    'Søger…':
        'Söker…',
    'Et ben kunne ikke lægges sikkert udenom land — kontrollér det '
        'selv på søkortet.':
        'En etapp kunde inte läggas säkert runt land — kontrollera den '
        'själv på sjökortet.',
    'også nat':
        'även natt',
    'Gå tilbage til Rute og tryk "Find bedste afgangstider".':
        'Gå tillbaka till Rutt och tryck på ”Hitta bästa avgångstider”.',
    'afgang':
        'avgång',
    'afgange':
        'avgångar',
    'dag':
        'dag',
    'dage':
        'dagar',
    '{n} t mørke':
        '{n} tim mörker',
    'når {nået} af {ialt} sømil':
        'når {nået} av {ialt} distansminuter',
    'ankomst {tid}':
        'ankomst {tid}',
    'l':
        'l',
    'Ingen bølgeprognose for dette farvand — vurder søgangen ud fra '
        'vind og stræk.':
        'Ingen vågprognos för det här farvattnet — bedöm sjögången '
        'utifrån vind och stryklängd.',
    'Få en skippervurdering':
        'Få en skepparbedömning',
    'En erfaren sejlkonsulent gennemgår ruten ben for ben og '
        'anbefaler, hvornår du bør kaste los.':
        'En erfaren seglingskonsult går igenom rutten etapp för etapp '
        'och rekommenderar när du bör kasta loss.',
    '{punkter} og den beregnede plan forsvinder. Det kan ikke '
        'fortrydes.':
        '{punkter} och den beräknade planen försvinner. Det går inte att '
        'ångra.',
    '{n} t motor':
        '{n} tim motor',
    'under vejs':
        'till sjöss',
    '{båd} · afgang {tid} · {hale}':
        '{båd} · avgång {tid} · {hale}',
    'Overnatning i {havn}, {sted}. {sm} sømil ind fra ruten. Videre '
        '{tid} næste morgen.':
        'Övernattning i {havn}, {sted}. {sm} distansminuter in från '
        'rutten. Vidare {tid} nästa morgon.',
    'med':
        'med',
    'imod':
        'mot',
    'punkt':
        'punkt',
    '{sm} sømil ekstra':
        '{sm} distansminuter extra',
    'Vælg en anden afgang':
        'Välj en annan avgång',
    'Læs om havnen i havnelods.dk →':
        'Läs om hamnen på havnelods.dk →',
    'Tak — {havn} står nu som "{svar}".':
        'Tack — {havn} står nu som ”{svar}”.',
    'Du har meldt rigeligt i dag. Prøv igen i morgen.':
        'Du har rapporterat tillräckligt i dag. Försök igen i morgon.',
    '{havn} — din melding hjælper den, der kommer i eftermiddag. Den '
        'står i halvandet døgn og forsvinder så af sig selv.':
        '{havn} — din rapport hjälper den som kommer i eftermiddag. Den '
        'står i ett och ett halvt dygn och försvinner sedan av sig själv.',
    'Meldingen er anonym, og der er ikke andet at skrive: kun havnen, '
        'svaret og hvornår. Så findes der ikke et sted i Sejlplan, hvor '
        'nogen kan skrive noget til nogen — og dermed heller ikke noget '
        'at moderere.':
        'Rapporten är anonym, och det finns inget annat att skriva: bara '
        'hamnen, svaret och när. Då finns det inte någon plats i '
        'Seglingsplan där någon kan skriva något till någon — och därmed '
        'inte heller något att moderera.',
    'Sejlplan fra ende til anden. Det samme står i boblerne ude i '
        'programmet — her er det bare samlet.':
        'Seglingsplan från början till slut. Detsamma står i bubblorna '
        'ute i programmet — här är det bara samlat.',
    '{navn} er gemt og valgt':
        '{navn} är sparad och vald',
    'Anslået {kn} knob for halvvind i 10 knobs vind, regnet af '
        'sejlareal, deplacement og vandlinje. Kender du din båds rigtige '
        'tal, så ret det nedenfor.':
        'Uppskattat {kn} knop för halvvind i 10 knops vind, räknat från '
        'segelyta, deplacement och vattenlinje. Känner du din båts '
        'riktiga siffra, ändra den nedan.',
    'Længde, fart og forbrug. Så regner planen på din båd i stedet '
        'for på et eksempel.':
        'Längd, fart och förbrukning. Då räknar planen på din båt i '
        'stället för på ett exempel.',
    'Over de her værdier markerer planen timerne som skærpede.':
        'Över de här värdena markerar planen timmarna som skärpta.',
    'Skroget afgør, hvor meget søen tager af farten. En planende båd '
        'taber mest.':
        'Skrovet avgör hur mycket sjön tar av farten. En planande båt '
        'förlorar mest.',
    'Det ene tal skalerer et almindeligt polardiagram, så farten '
        'passer til din båd. Ved du det ikke, så gæt på en god dag med '
        'fuld sejlføring.':
        'Den enda siffran skalar ett vanligt polardiagram så att farten '
        'passar din båt. Vet du den inte, gissa på en bra dag med full '
        'segelföring.',
    'Ingen båd med det navn i registret. Tast målene ind nedenfor i '
        'stedet.':
        'Ingen båt med det namnet i registret. Skriv in måtten nedan i '
        'stället.',
    'i dag':
        'i dag',
    'Der er ingen rute at gemme':
        'Det finns ingen rutt att spara',
    'tidligere':
        'tidigare',
    '"{navn}" er gemt':
        '”{navn}” är sparad',
    '{punkter} · {sm} sømil':
        '{punkter} · {sm} distansminuter',
    'Læg en rute, og tryk Gem. Så ligger den her næste gang — også '
        'hvis du lukker fanen.':
        'Lägg en rutt och tryck på Spara. Då ligger den här nästa gång — '
        'även om du stänger fliken.',
    '{punkter} · {sm} sømil · gemt {hvornår}':
        '{punkter} · {sm} distansminuter · sparad {hvornår}',
    '"{navn}" forsvinder. Det kan ikke fortrydes.':
        '”{navn}” försvinner. Det går inte att ångra.',
    'Uden navn':
        'Utan namn',
    'Sejlplan – find den bedste afgang':
        'Seglingsplan – hitta den bästa avgången',
    'Rute åbnet: {fra} → {til}':
        'Rutt öppnad: {fra} → {til}',
    'Delelinket kunne ikke læses':
        'Delningslänken kunde inte läsas',
    'Indstillingerne er sat tilbage til standard':
        'Inställningarna är återställda till standard',
    'Browseren kunne ikke installere appen herfra.':
        'Webbläsaren kunde inte installera appen härifrån.',
    'Slået til lægges der ingen overnatninger ind — turen sejles i ét '
        'stræk, og mørketimerne tælles for sig.':
        'Med det påslaget läggs inga övernattningar in — resan seglas i '
        'ett sträck, och mörkertimmarna räknas för sig.',
    'Under 3 knobs fart tændes motoren i beregningen.':
        'Under tre knops fart startas motorn i beräkningen.',
    'Tidligst ud af havn':
        'Tidigast ut ur hamn',
    'Senest i havn igen':
        'Senast i hamn igen',
    'Farten kommer fra polardiagrammet.':
        'Farten kommer från polardiagrammet.',
    'Farten er marchfarten, minus det søen tager.':
        'Farten är marschfarten, minus det sjön tar.',
    'Over disse værdier markeres timerne som skærpede, og et stykke '
        'over dem som frarådede. Bølgehøjden vejes efter hvor søen kommer '
        'fra — modsø tæller hårdere end medsø.':
        'Över de här värdena markeras timmarna som skärpta, och en bit '
        'över dem som avrådda. Våghöjden vägs efter var sjön kommer ifrån '
        '— motsjö räknas hårdare än medsjö.',
    'Vejrudsigten rækker til og med {dato}.':
        'Väderprognosen räcker till och med {dato}.',
    'Det tidsrum, du vil ligge og sejle i. Slutklokkeslættet er ikke '
        'et ønske om at afgå senest da — det er hvornår du vil ligge '
        'fortøjet. Rækker turen ikke, deler planlæggeren den og finder en '
        'havn undervejs at overnatte i.':
        'Den tid du vill ligga och segla i. Sluttiden är inte ett '
        'önskemål om att avgå senast då — det är när du vill ligga '
        'förtöjd. Räcker resan inte delar planeraren den och hittar en '
        'hamn längs vägen att övernatta i.',
    'Vælg den, der ligner din mest, hvis du ikke vil taste din egen '
        'ind.':
        'Välj den som liknar din mest, om du inte vill skriva in din '
        'egen.',
    'Det giver {n} timers sejlads i døgnet.':
        'Det ger {n} timmars segling per dygn.',
    'Så åbner Sejlplan i sit eget vindue — og den seneste sejlplan '
        'kan læses uden dækning.':
        'Då öppnas Seglingsplan i ett eget fönster — och den senaste '
        'seglingsplanen går att läsa utan täckning.',
    '{sm} sømil sejlet':
        '{sm} distansminuter seglade',
    '{sm} tilbage':
        '{sm} kvar',
    '{kn} knob i snit':
        '{kn} knop i snitt',
    'Du er {n} minutter {dom}':
        'Du ligger {n} minuter {dom}',
    'Du er {n} timer {dom}':
        'Du ligger {n} timmar {dom}',
    'Med den fart er du fremme {tid}.':
        'Med den farten är du framme {tid}.',
    'Du er {sm} sømil fra ruten. Så længe det er sådan, kan vi ikke '
        'sige, om du er foran eller bagud.':
        'Du är {sm} distansminuter från rutten. Så länge det är så kan vi '
        'inte säga om du ligger före eller efter.',
    'Læg først en rute med mindst to punkter':
        'Lägg först en rutt med minst två punkter',
    'Skriv en mailadresse, vi kan skrive til':
        'Skriv en e-postadress vi kan skriva till',
    'Vinduet ligger i fortiden':
        'Fönstret har redan passerat',
    'Vi har skrevet til {adresse}. Bekræft i mailen, så går vagten i '
        'gang.':
        'Vi har skrivit till {adresse}. Bekräfta i mejlet, så går vakten '
        'igång.',
    'Mailen kunne ikke sendes. Prøv igen om lidt.':
        'Mejlet kunde inte skickas. Försök igen om en stund.',
    'Vælg to datoer':
        'Välj två datum',
    'Vi holder øje med {rute} og skriver til dig, når der er et '
        'vindue, du kan sejle i. Én mail — ikke en strøm af dem.':
        'Vi håller koll på {rute} och skriver till dig när det finns ett '
        'fönster du kan segla i. Ett mejl — inte en ström av dem.',
    'Prognosen rækker {døgn} døgn frem — til og med {dato}. Ligger '
        'dit vindue længere ude, venter vagten, til prognosen når derhen.':
        'Prognosen räcker {døgn} dygn fram — till och med {dato}. Ligger '
        'ditt fönster längre bort väntar vakten tills prognosen når dit.',
    'Målt mod dine egne grænser: {kn} knob og {m} meter, sejldøgn '
        '{fra}–{til}. Vi skriver kun, hvis du også kan komme hjem igen.':
        'Mätt mot dina egna gränser: {kn} knop och {m} meter, etmål '
        '{fra}–{til}. Vi skriver bara om du också kan komma hem igen.',
    'Vi bruger din adresse til denne ene besked og sletter vagten '
        'bagefter. Du kan stoppe den når som helst med linket i mailen.':
        'Vi använder din adress till det här enda meddelandet och raderar '
        'vakten efteråt. Du kan stoppa den när som helst med länken i '
        'mejlet.',
    'Vejrvagt er ikke slået til':
        'Vädervakten är inte påslagen',
    'Serveren har ingen postkasse at skrive fra endnu. Når den har, '
        'kan du bede Sejlplan holde øje med vejret til en tur og skrive, '
        'når der er et vindue.':
        'Servern har ingen brevlåda att skriva från ännu. När den har det '
        'kan du be Seglingsplan hålla koll på vädret för en resa och '
        'skriva när det finns ett fönster.',
    'Vi holder øje med {rute} mellem {fra} og {til}. Du hører fra os, '
        'når der er et vindue, du kan sejle i — og kun den ene gang.':
        'Vi håller koll på {rute} mellan {fra} och {til}. Du hör från oss '
        'när det finns ett fönster du kan segla i — och bara den enda '
        'gången.',
    'Vi holder ikke længere øje med {rute}, og vi skriver ikke til '
        'dig om den igen.':
        'Vi håller inte längre koll på {rute}, och vi skriver inte till '
        'dig om den igen.',
    'Linket er forkert, eller vagten er allerede stoppet.':
        'Länken är fel, eller så är vakten redan stoppad.',
    'AI-analysen er ikke slået til på denne server. Sæt '
        'ANTHROPIC_API_KEY i .env og genstart.':
        'AI-analysen är inte påslagen på den här servern. Sätt '
        'ANTHROPIC_API_KEY i .env och starta om.',
    'Serverens API-nøgle blev afvist. Tjek ANTHROPIC_API_KEY.':
        'Serverns API-nyckel avvisades. Kontrollera ANTHROPIC_API_KEY.',
    'For mange forespørgsler lige nu. Prøv igen om et øjeblik.':
        'För många förfrågningar just nu. Försök igen om ett ögonblick.',
    'AI-tjenesten svarede med fejl {kode}.':
        'AI-tjänsten svarade med fel {kode}.',
    'Kunne ikke få forbindelse til AI-tjenesten.':
        'Kunde inte få kontakt med AI-tjänsten.',
    'sejl':
        'segel',
    'dybgang':
        'djupgående',
    '{n} pladser':
        '{n} platser',
    '{detalje} · ved {sted}':
        '{detalje} · vid {sted}',
    'Lystbådehavn':
        'Småbåtshamn',
    'Position':
        'Position',
    'Ud for {sted}':
        'Utanför {sted}',
    'Ukendt område':
        'Okänt område',
    '{hilsen}\n\nNu er der vejr til {rute}.\n\nAfgang     '
        '{afgang}\nAnkomst    {ankomst}\nDistance   {sm} sømil\nUnder vejs '
        '{timer} timer, snit {snit} knob\nVind       op til {vind} '
        'knob\nBølger     op til {boelger} meter{ophold}\n\nÅbn turen i '
        'Sejlplan, så kan du se hele planen — dag for dag, stræk for '
        'stræk\nog time for time:\n{link}\n\nPrognosen kan nå at flytte sig. '
        'Se den efter igen dagen før, du kaster los.\n\nVagten er hermed '
        'brugt. Vil du holde øje med en ny tur, så læg en ny vagt.\nVil du '
        'stoppe den her med det samme: {stop}\n\nGod tur.\nSejlplan\n':
        '{hilsen}\n\nNu finns det väder för {rute}.\n\nAvgång     '
        '{afgang}\nAnkomst    {ankomst}\nDistans    {sm} '
        'distansminuter\nTill sjöss {timer} timmar, snitt {snit} '
        'knop\nVind       upp till {vind} knop\nVågor      upp till '
        '{boelger} meter{ophold}\n\nÖppna resan i Seglingsplan, så ser du '
        'hela planen — dag för dag, sträcka för\nsträcka och timme för '
        'timme:\n{link}\n\nPrognosen kan hinna flytta sig. Se över den igen '
        'dagen innan du kastar loss.\n\nDärmed är vakten förbrukad. Vill du '
        'hålla koll på en ny resa, lägg en ny vakt.\nVill du stoppa den '
        'här med detsamma: {stop}\n\nGod tur.\nSeglingsplan\n',
    'Nu er der vejr til {rute}':
        'Nu finns det väder för {rute}',
    '{hilsen}\n\nDu har bedt Sejlplan holde øje med vejret til '
        '{rute}\nmellem {fra} og {til}.\n\nBekræft, at adressen er din, så '
        'går vagten i gang:\n{ja}\n\nVi skriver én gang — når der er et '
        'vindue, du kan sejle i. Ikke oftere.\n\nVar det ikke dig, skal du '
        'ingenting gøre. Så bliver vagten aldrig aktiv, og\nden ryger af '
        'sig selv. Vil du være sikker: {stop}\n\nSejlplan\n':
        '{hilsen}\n\nDu har bett Seglingsplan hålla koll på vädret för '
        '{rute}\nmellan {fra} och {til}.\n\nBekräfta att adressen är din, så '
        'går vakten igång:\n{ja}\n\nVi skriver en enda gång — när det finns '
        'ett fönster du kan segla i. Inte\noftare.\n\nVar det inte du '
        'behöver du inte göra något. Då blir vakten aldrig aktiv '
        'och\nfaller bort av sig själv. Vill du vara säker: '
        '{stop}\n\nSeglingsplan\n',
    'Bekræft vejrvagt: {rute}':
        'Bekräfta vädervakt: {rute}',
    'Hej {navn}':
        'Hej {navn}',
    'Hej':
        'Hej',
    'Undervejs ligger du i {havne}.':
        'Längs vägen ligger du i {havne}.',
    'Noget gik galt her — det er ikke dig. Prøv igen, og skriv fejl '
        '{ref}, hvis det bliver ved.':
        'Något gick fel här — det är inte ditt fel. Försök igen, och '
        'uppge fel {ref} om det håller i sig.',
    'Under vejs':
        'Till sjöss',
    'Gemt om bord {tid} · virker uden dækning':
        'Sparad ombord {tid} · fungerar utan täckning',
    'Hentet {tid} og gemt i telefonen. Åbn Sejlplan med dækning for '
        'at regne den om.':
        'Hämtad {tid} och sparad i telefonen. Öppna Seglingsplan med '
        'täckning för att räkna om den.',
    'for {n} dage siden':
        'för {n} dagar sedan',
    'for {n} timer siden':
        'för {n} timmar sedan',
    'Knæk {nr}':
        'Brytpunkt {nr}',
    'Vejrtjenesten svarer ikke. Prøv igen om lidt.':
        'Vädertjänsten svarar inte. Försök igen om en stund.',
    'Vejrtjenesten returnerede ingen data for ruten.':
        'Vädertjänsten returnerade inga data för rutten.',
    'Kunne ikke hente vejrdata: {fejl}':
        'Kunde inte hämta väderdata: {fejl}',
    'Familiekrydser':
        'Familjekryssare',
    'Klassisk krydser':
        'Klassisk kryssare',
    'Fortrængningsbåd':
        'Deplacementsbåt',
    'Langturssejler':
        'Långfärdsseglare',
    'Lille krydser':
        'Liten kryssare',
    'Stor planende':
        'Stor planande',
    'Weekendbåd':
        'Weekendbåt',
    'den brede middelvej':
        'den breda medelvägen',
    'hurtig i smult vande, hård i sø':
        'snabb i lugnt vatten, hård i sjö',
    'komfort og rækkevidde':
        'komfort och räckvidd',
    'langsom, men uanfægtet':
        'långsam, men obekymrad',
    'lille, men sødygtig':
        'liten, men sjöduglig',
    'nem at have med at gøre':
        'lätt att ha att göra med',
    'rolig og tilgivende':
        'lugn och förlåtande',
    'rummelig og hurtig nok':
        'rymlig och snabb nog',
    'tåler mest af dem alle':
        'tål mest av alla',
    'tung':
        'tung',
    'solid':
        'solid',
    'moderat':
        'måttlig',
    'let':
        'lätt',
    'rigeligt sejl':
        'riklig segelyta',
    'godt sejlført':
        'god segelyta',
    'almindeligt sejlført':
        'normal segelyta',
    'beskedent sejlført':
        'sparsam segelyta',
    'Min båd':
        'Min båt',
    'Din egen':
        'Din egen',
    'Tur':
        'Resa',
    'Havne omkring dig':
        'Hamnar omkring dig',
    'Søgeresultater':
        'Sökresultat',
    'Søg havnen frem, eller vælg en af dem omkring dig.':
        'Sök fram hamnen, eller välj en av dem omkring dig.',
    'Ingen havne med det navn. Prøv en anden stavemåde.':
        'Ingen hamn med det namnet. Prova en annan stavning.',
    'Vi ved ikke, hvor du er. Søg havnen frem foroven — eller slå '
        '"Jeg er undervejs" til.':
        'Vi vet inte var du är. Sök fram hamnen ovan — eller slå på ”Jag '
        'är till sjöss”.',
    'Søg efter en havn…':
        'Sök efter en hamn…',
    '{km} km':
        '{km} km',
    '{m} meter':
        '{m} meter',
    'Din båd':
        'Din båt',
    'Browseren giver ikke adgang til position':
        'Webbläsaren ger inte tillgång till position',
    'Uden en position er der ingen båd at vise. Prøv i en anden '
        'browser, eller på telefonen.':
        'Utan en position finns det ingen båt att visa. Prova i en annan '
        'webbläsare, eller på telefonen.',
    'Du har sagt nej til position for den her side':
        'Du har nekat position för den här sidan',
    'Browseren spørger ikke igen af sig selv. Slå det til i '
        'indstillingerne for siden — i Chrome ligger det bag hængelåsen i '
        'adresselinjen.':
        'Webbläsaren frågar inte igen av sig själv. Slå på det i '
        'inställningarna för sidan — i Chrome ligger det bakom hänglåset '
        'i adressfältet.',
    'Du sidder ved en computer':
        'Du sitter vid en dator',
    'En computer har ingen GPS. Den gætter positionen ud fra wifi og '
        'netværk, og det kan være kilometer ved siden af — de andre ser '
        'din båd et sted, du ikke er. På telefonen er den på få meter. '
        'Vil du vises rigtigt undervejs, så åbn Sejlplan på telefonen.':
        'En dator har ingen GPS. Den gissar positionen utifrån wifi och '
        'nätverk, och det kan vara kilometer fel — de andra ser din båt '
        'på en plats där du inte är. På telefonen är den på några meter. '
        'Vill du visas rätt till sjöss, öppna Seglingsplan på telefonen.',
    'Din position er kun kendt på ±{afstand}. Det er et gæt fra '
        'nettet, ikke GPS — på telefonen er den på få meter.':
        'Din position är bara känd på ±{afstand}. Det är en gissning från '
        'nätet, inte GPS — på telefonen är den på några meter.',
    'Du er ikke synlig for andre, før browseren har fundet dig. Sig '
        'ja til position, hvis den spørger.':
        'Du syns inte för andra förrän webbläsaren har hittat dig. Säg ja '
        'till position om den frågar.',
    'Beskeder fra andre både':
        'Meddelanden från andra båtar',
    'Gode forhold':
        'Bra förhållanden',
    '{svar} — meldt {hvornår}':
        '{svar} — rapporterat {hvornår}',
    'efter {sm} sm · {omvej} sm ind fra ruten':
        'efter {sm} M · {omvej} M in från rutten',
    'Både i nærheden':
        'Båtar i närheten',
    'Se hvem der er i nærheden':
        'Se vilka som är i närheten',
    'En anden båd':
        'En annan båt',
    '{navn} har skrevet til dig':
        '{navn} har skrivit till dig',
    'har skrevet':
        'har skrivit',
    'båd':
        'båt',
    'både':
        'båtar',
    'både|flertal':
        'båtar',
    'båd her':
        'båt här',
    'både her':
        'båtar här',
    'både her|flertal':
        'båtar här',
    '{sm} sm mod {retning}':
        '{sm} M mot {retning}',
    'Ingen andre både i nærheden':
        'Inga andra båtar i närheten',
    'Der er ingen inden for tres sømil, der har gjort sig synlig lige '
        'nu.':
        'Det finns ingen inom sextio distansminuter som har gjort sig '
        'synlig just nu.',
    'Du ser kun både, der også har gjort sig synlige.':
        'Du ser bara båtar som också har gjort sig synliga.',
    'Vi ved ikke, hvor du er endnu':
        'Vi vet inte var du är ännu',
    'Uden en position kan vi ikke sige, hvem der er i nærheden. Sig '
        'ja til position, hvis browseren spørger.':
        'Utan en position kan vi inte säga vem som är i närheten. Säg ja '
        'till position om webbläsaren frågar.',
    # ── forside, rangering og "hvad nu" ──
    'Ruten {navne} er på {sm} sømil fordelt på {ben} mellem dine punkter. ':
        'Rutten {navne} är {sm} sjömil fördelat på {ben} mellan dina punkter. ',
    'Ruter':
        'Rutter',
    'Hjælp':
        'Hjälp',
    'Indstil':
        'Inställ',
    'Tema':
        'Tema',
    'Vi skriver, hvis prognosen ændrer anbefalingen inden afgang':
        'Vi hör av oss om prognosen ändrar rekommendationen före avgång',
    'Del med besætningen':
        'Dela med besättningen',
    'Et link, der åbner den samme rute hos dem':
        'En länk som öppnar samma rutt hos dem',
    'Ruten er gemt':
        'Rutten är sparad',
    'Gem denne rute':
        'Spara den här rutten',
    'Ligger på hylden under Mine ruter':
        'Ligger under Mina rutter',
    'Så kan du hente den frem igen uden at lægge den om':
        'Då kan du ta fram den igen utan att lägga om den',
    'Hvad nu':
        'Vad nu',
    'Din gemte plan begyndte {dato}. Prognosen rækker kun fra i dag, så vi er startet der — ret den under Hvornår, hvis du vil noget andet.':
        'Din sparade plan började {dato}. Prognosen räcker bara från i dag, så vi har börjat där — ändra under När om du vill något annat.',
    'når kun {nået} af {ialt} sømil, før prognosen slipper op':
        'når bara {nået} av {ialt} sjömil innan prognosen tar slut',
    'fremme efter sejldøgnet er omme':
        'framme efter att seglingsdygnet är slut',
    '{n} t i forhold, der frarådes':
        '{n} tim i förhållanden som avråds',
    '{n} t i skærpede forhold':
        '{n} tim i skärpta förhållanden',
    'topper {kn} kn — over din grænse':
        'toppar {kn} kn — över din gräns',
    'bølger op til {m} m — over din grænse':
        'vågor upp till {m} m — över din gräns',
    'kræver {n} overnatninger undervejs':
        'kräver {n} övernattningar på vägen',
    '{t} t længere undervejs end den bedste':
        '{t} tim längre på vägen än den bästa',
    '{kn} knob langsommere i snit':
        '{kn} knop långsammare i snitt',
    'roligste vejr og hurtigst fremme':
        'lugnaste vädret och snabbast framme',
    'tidlig afgang — hele dagen i baghånden':
        'tidig avgång — hela dagen i reserv',
    'samme vejr, men senere af sted':
        'samma väder, men senare i väg',
    'i luftlinje — vejen udenom land regnes stadig':
        'fågelvägen — vägen runt land räknas fortfarande',
    'Skipperen læser vejrudsigten igennem…':
        'Skepparen läser igenom prognosen…',
    'Den tager en halv til hel minut. Resten af planen står klar nedenunder imens.':
        'Det tar en halv till hel minut. Resten av planen står klar nedanför under tiden.',
    'Lav vurderingen om':
        'Gör om bedömningen',
    'Hent skippervurderingen':
        'Hämta skepparbedömningen',
    'dagens bedste er nr. {n}':
        'dagens bästa är nr {n}',
    'bedste dag':
        'bästa dagen',
}
