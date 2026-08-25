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
    'Rute':
        'Rutt',
    'Afgangstid':
        'Avgångstid',
    'Sejlplan':
        'Seglingsplan',
    'Find bedste afgangstider':
        'Hitta bästa avgångstider',
    'Se sejlplanen':
        'Se seglingsplanen',
    'Kortet':
        'Kartan',
    'Udskriv':
        'Skriv ut',
    'Kopiér':
        'Kopiera',
    'Gem':
        'Spara',
    'Fortryd':
        'Ångra',
    'Annullér':
        'Avbryt',
    'Færdig':
        'Klar',
    'Luk':
        'Stäng',
    'Nulstil':
        'Nollställ',
    'Ret':
        'Ändra',
    'Slet':
        'Radera',
    'Omdøb':
        'Byt namn',
    'Behold':
        'Behåll',
    'Ryd':
        'Rensa',
    'Se alle':
        'Se alla',
    'Installér':
        'Installera',
    'Hent':
        'Hämta',
    'Stop':
        'Stoppa',
    'Tilbage til ruten':
        'Tillbaka till rutten',
    'Søg havn, ø eller position…':
        'Sök hamn, ö eller position…',
    'Ruten':
        'Rutten',
    'Turen':
        'Resan',
    'Afgang':
        'Avgång',
    'Destination':
        'Destination',
    'Mellemstop':
        'Mellanstopp',
    'Læg din rute':
        'Lägg din rutt',
    'Kom hurtigt i gang':
        'Kom snabbt igång',
    'Vis på kortet':
        'Visa på kartan',
    'Søkort':
        'Sjökort',
    'Landkort':
        'Landkarta',
    'Havne':
        'Hamnar',
    'Sømærker':
        'Sjömärken',
    'Hele ruten':
        'Hela rutten',
    'Søg efter en havn foroven, klik direkte på kortet, eller slå '
        'havnelaget til og vælg en havn. Du skal bruge mindst to punkter.':
        'Sök efter en hamn ovan, klicka direkt på kartan, eller slå på '
        'hamnlagret och välj en hamn. Du behöver minst två punkter.',
    'Tilføj mindst ét punkt mere for at kunne beregne afgangstider.':
        'Lägg till minst en punkt till för att kunna räkna ut '
        'avgångstider.',
    'Båd':
        'Båt',
    'Din båd':
        'Din båt',
    'Sejlbåd':
        'Segelbåt',
    'Motorbåd':
        'Motorbåt',
    'Navn':
        'Namn',
    'Type':
        'Typ',
    'Længde overalt':
        'Längd överallt',
    'Marchfart i smult vande':
        'Marschfart i lugnt vatten',
    'Skrogtype':
        'Skrovtyp',
    'Fortrængning':
        'Deplacement',
    'Halvplanende':
        'Halvplanande',
    'Planende':
        'Planande',
    'Forbrug ved marchfart':
        'Förbrukning vid marschfart',
    'Forbrug for motor':
        'Förbrukning för motor',
    'Fart for motor':
        'Fart för motor',
    'Fart for halvvind i 10 knobs vind':
        'Fart för halvvind i 10 knops vind',
    'Find din båd':
        'Hitta din båt',
    'Læg din egen båd ind':
        'Lägg in din egen båt',
    'Gem båden':
        'Spara båten',
    'Eller et eksempel':
        'Eller ett exempel',
    'Sejlbåde':
        'Segelbåtar',
    'Motorbåde':
        'Motorbåtar',
    'Hvad du kan holde til':
        'Vad du tål',
    'Højeste vind':
        'Högsta vind',
    'Højeste bølger':
        'Högsta vågor',
    'Komfortgrænser':
        'Komfortgränser',
    'Grænser':
        'Gränser',
    'Giv båden et navn':
        'Ge båten ett namn',
    'Hvornår':
        'När',
    'Sejldøgn':
        'Etmål',
    'Hvornår kan du afgå':
        'När kan du avgå',
    'Tidligst afgang':
        'Tidigast avgång',
    'Senest afgang':
        'Senast avgång',
    'Tidligst':
        'Tidigast',
    'Senest':
        'Senast',
    'Sejlads':
        'Segling',
    'Sejl også om natten':
        'Segla även på natten',
    'Brug motor i svag vind':
        'Använd motor i svag vind',
    'Overblik':
        'Överblick',
    'Vær opmærksom på':
        'Var uppmärksam på',
    'Nøgletal':
        'Nyckeltal',
    'Dag for dag':
        'Dag för dag',
    'Stræk for stræk':
        'Sträcka för sträcka',
    'Time for time':
        'Timme för timme',
    'Skippervurdering':
        'Skepparbedömning',
    'Havne undervejs':
        'Hamnar längs vägen',
    'Sejltid':
        'Seglingstid',
    'Gns. fart':
        'Snittfart',
    'Distance':
        'Distans',
    'Frarådet':
        'Avrådes',
    'Brændstof':
        'Bränsle',
    'God':
        'Bra',
    'Skærpet':
        'Skärpt',
    'Frarådes':
        'Avrådes',
    'Tid':
        'Tid',
    'Vind':
        'Vind',
    'Fra':
        'Från',
    'Bølger':
        'Vågor',
    'Fart':
        'Fart',
    'Strøm':
        'Ström',
    'Sejlføring':
        'Segelföring',
    'Søen':
        'Sjön',
    'Ingen beregning endnu':
        'Ingen beräkning ännu',
    'Steder du kan søge ind, hvis vejret skifter. Klik for at lægge '
        'en ind som mellemstop.':
        'Ställen du kan söka skydd i om vädret slår om. Klicka för att '
        'lägga in ett som mellanstopp.',
    'Havneguide ↗':
        'Hamnguide ↗',
    'Ruten er delt op efter kursskift, så hvert stykke gælder præcis '
        'dér, hvor du styrer den kurs.':
        'Rutten är delad efter kursändringar, så varje stycke gäller '
        'precis där du styr den kursen.',
    'Mine ruter':
        'Mina rutter',
    'Mine gemte ruter':
        'Mina sparade rutter',
    'Gem ruten':
        'Spara rutten',
    'Gem ændringer':
        'Spara ändringar',
    'Gem som ny':
        'Spara som ny',
    'Slet ruten?':
        'Radera rutten?',
    'Ingen gemte ruter endnu':
        'Inga sparade rutter ännu',
    'Omdøb ruten':
        'Byt namn på rutten',
    'Ruten er slettet':
        'Rutten är raderad',
    'Ruten er ryddet':
        'Rutten är rensad',
    'Ryd hele ruten?':
        'Rensa hela rutten?',
    'Ryd hele ruten':
        'Rensa hela rutten',
    'Vend ruten om':
        'Vänd rutten',
    'Kopiér delelink':
        'Kopiera delningslänk',
    'Hent GPX til kortplotter':
        'Hämta GPX till kartplotter',
    'Del eller eksportér ruten':
        'Dela eller exportera rutten',
    'Appen':
        'Appen',
    'Manual':
        'Handbok',
    'Manual og hjælp':
        'Handbok och hjälp',
    'Indstillinger':
        'Inställningar',
    'Båd, grænser og sejldøgn':
        'Båt, gränser och etmål',
    'Skift mellem lyst og mørkt':
        'Växla mellan ljust och mörkt',
    'Sprog':
        'Språk',
    'Læg på hjemmeskærmen':
        'Lägg på hemskärmen',
    'Sejlplan kører allerede som app.':
        'Seglingsplan körs redan som app.',
    'Tryk på Del nederst i Safari, og vælg "Føj til hjemmeskærm".':
        'Tryck på Dela längst ned i Safari och välj "Lägg till på '
        'hemskärmen".',
    'Er der plads?':
        'Finns det plats?',
    'Meld plads':
        'Rapportera plats',
    'God plads':
        'Gott om plats',
    'Få pladser':
        'Få platser',
    'Fuld':
        'Fullt',
    'lige nu':
        'just nu',
    'for en time siden':
        'för en timme sedan',
    'i går':
        'i går',
    'Vejrvagt':
        'Vädervakt',
    'Hold øje med vejret':
        'Håll koll på vädret',
    'Hold øje':
        'Håll koll',
    'Dit navn (valgfrit)':
        'Ditt namn (frivilligt)',
    'Din mailadresse':
        'Din e-postadress',
    'Hvornår kan I komme afsted?':
        'När kan ni ge er av?',
    'Hvor godt skal det være?':
        'Hur bra ska det vara?',
    'Kun gode forhold':
        'Bara bra förhållanden',
    'Også skærpede':
        'Även skärpta',
    'Vagten er i gang':
        'Vakten är igång',
    'Vagten er stoppet':
        'Vakten är stoppad',
    'Vagten findes ikke':
        'Vakten finns inte',
    'Stop vagten':
        'Stoppa vakten',
    'Åbn Sejlplan':
        'Öppna Seglingsplan',
    'Undervejs':
        'Till sjöss',
    'Jeg er undervejs':
        'Jag är till sjöss',
    'Følg med i, om du er foran eller bagud.':
        'Följ med i om du ligger före eller efter.',
    'Leder efter positionen…':
        'Letar efter positionen…',
    'Du følger planen':
        'Du följer planen',
    'foran':
        'före',
    'bagud':
        'efter',
    'Du er fremme. God tur — og velkommen i havn.':
        'Du är framme. God tur — och välkommen i hamn.',
    'Turen er ikke begyndt endnu — afgangen ligger frem i tiden. Når '
        'du har kastet los, står der her, om du er foran eller bagud.':
        'Resan har inte börjat ännu — avgången ligger fram i tiden. När '
        'du har kastat loss står det här om du ligger före eller efter.',
    'Positionen bliver på din telefon. Den gemmes ikke, og ingen '
        'andre kan se den.':
        'Positionen stannar i din telefon. Den sparas inte, och ingen '
        'annan kan se den.',
    'Vis din båd på kortet':
        'Visa din båt på kartan',
    'Vis min båd for andre':
        'Visa min båt för andra',
    'Bådens navn':
        'Båtens namn',
    'Vis mig':
        'Visa mig',
    'Skjul mig':
        'Dölj mig',
    'Du er synlig som':
        'Du syns som',
    'Ingen andre både i nærheden lige nu.':
        'Inga andra båtar i närheten just nu.',
    '{n} andre både i nærheden.':
        '{n} andra båtar i närheten.',
    'Giv båden et navn, de andre kan se':
        'Ge båten ett namn som de andra kan se',
    'Så kan andre, der også er synlige, se hvor du er — og du kan se '
        'dem. Kun jer, der har slået det til.':
        'Då kan andra som också syns se var du är — och du kan se dem. '
        'Bara ni som har slagit på det.',
    'Skriv bådens navn, ikke dit eget. Det er dét, de andre ser.':
        'Skriv båtens namn, inte ditt eget. Det är det de andra ser.',
    'Du er usynlig, indtil du selv tænder — og du forsvinder igen i '
        'samme øjeblik, du slukker.':
        'Du är osynlig tills du själv slår på det — och du försvinner '
        'igen i samma stund du slår av.',
    'Positionen udløber af sig selv efter en halv time uden '
        'opdatering.':
        'Positionen går ut av sig själv efter en halvtimme utan '
        'uppdatering.',
    'Der gemmes ingen historik. Hver ny position skriver den forrige '
        'over, så ingen kan slå op, hvor du var i går.':
        'Ingen historik sparas. Varje ny position skriver över den förra, '
        'så ingen kan slå upp var du var i går.',
    'Du ser kun andre, mens du selv er synlig. Ingen kan kigge uden '
        'at være der selv.':
        'Du ser bara andra medan du själv syns. Ingen kan titta utan att '
        'vara där själv.',
    'Din båd er nu synlig for andre, der også er det.':
        'Din båt syns nu för andra som också gör det.',
    'Du er ikke længere synlig, og din position er slettet.':
        'Du syns inte längre, och din position är raderad.',
    'Beskeder':
        'Meddelanden',
    'Skriv en kort besked…':
        'Skriv ett kort meddelande…',
    'Send':
        'Skicka',
    'Anmeld':
        'Anmäl',
    'Bloker':
        'Blockera',
    'Bloker denne båd':
        'Blockera den här båten',
    'er blokeret':
        'är blockerad',
    'Ingen beskeder':
        'Inga meddelanden',
    'Ingen beskeder endnu. Skriv den første.':
        'Inga meddelanden ännu. Skriv det första.',
    'Beskeder forsvinder efter et døgn.':
        'Meddelanden försvinner efter ett dygn.',
    'Tryk på en båd på kortet for at skrive til den.':
        'Tryck på en båt på kartan för att skriva till den.',
    'I kan ikke længere skrive til hinanden, og I kan ikke se '
        'hinanden på kortet. Det gælder begge veje.':
        'Ni kan inte längre skriva till varandra, och ni kan inte se '
        'varandra på kartan. Det gäller åt båda håll.',
    'Beskeden er anmeldt. Vi gemmer den, så den kan ses efter.':
        'Meddelandet är anmält. Vi sparar det så att det kan granskas.',
    'Venter på din position…':
        'Väntar på din position…',
    'Du er ikke synlig for andre, før telefonen har fundet dig. Sig '
        'ja til position, hvis browseren spørger.':
        'Du syns inte för andra förrän telefonen har hittat dig. Säg ja '
        'till position om webbläsaren frågar.',
    'Havnene omkring dig, nærmeste først. Vælg den, du ligger i.':
        'Hamnarna omkring dig, närmaste först. Välj den du ligger i.',
    'sømil':
        'distansminuter',
    'knob':
        'knop',
    'meter':
        'meter',
    'timer':
        'timmar',
    'time':
        'timme',
    'døgn':
        'dygn',
    'nat':
        'natt',
    'nætter':
        'nätter',
    'overnatning':
        'övernattning',
    'overnatninger':
        'övernattningar',
    'punkter':
        'punkter',
    'motor':
        'motor',
    'i alt':
        'totalt',
    'Hentet':
        'Hämtad',
    'Sprog / Sprache / Språk':
        'Språk',
    'Find den bedste afgang, og tag sejlplanen med til søs. Her står, '
        'hvad tallene betyder, og hvad du selv skal tage stilling til.':
        'Hitta den bästa avgången och ta seglingsplanen med till sjöss. '
        'Här står vad siffrorna betyder och vad du själv måste ta '
        'ställning till.',
    'sejldøgn':
        'etmål',
    'ben':
        'etapp',
    'Ingen havne i nærheden':
        'Inga hamnar i närheten',
    'Vi ved ikke, hvor du er. Slå "Jeg er undervejs" til, eller læg '
        'en rute først.':
        'Vi vet inte var du är. Slå på ”Jag är till sjöss”, eller lägg '
        'en rutt först.',
    'Beskeden findes ikke længere.':
        'Meddelandet finns inte längre.',
    'Kunne ikke sendes':
        'Kunde inte skickas',
    'mandag':
        'måndag',
    'tirsdag':
        'tisdag',
    'onsdag':
        'onsdag',
    'torsdag':
        'torsdag',
    'fredag':
        'fredag',
    'lørdag':
        'lördag',
    'søndag':
        'söndag',
    'man':
        'mån',
    'tir':
        'tis',
    'ons':
        'ons',
    'tor':
        'tors',
    'fre':
        'fre',
    'lør':
        'lör',
    'søn':
        'sön',
    'januar':
        'januari',
    'februar':
        'februari',
    'marts':
        'mars',
    'april':
        'april',
    'maj':
        'maj',
    'juni':
        'juni',
    'juli':
        'juli',
    'august':
        'augusti',
    'september':
        'september',
    'oktober':
        'oktober',
    'november':
        'november',
    'december':
        'december',
    'jan':
        'jan',
    'feb':
        'feb',
    'mar':
        'mar',
    'apr':
        'apr',
    'jun':
        'jun',
    'jul':
        'jul',
    'aug':
        'aug',
    'sep':
        'sep',
    'okt':
        'okt',
    'nov':
        'nov',
    'dec':
        'dec',
    't':
        'tim',
    'd':
        'd',
    'min':
        'min',
    'NNØ':
        'NNO',
    'NØ':
        'NO',
    'ØNØ':
        'ONO',
    'Ø':
        'O',
    'ØSØ':
        'OSO',
    'SØ':
        'SO',
    'SSØ':
        'SSO',
    'SSV':
        'SSV',
    'SV':
        'SV',
    'VSV':
        'VSV',
    'V':
        'V',
    'VNV':
        'VNV',
    'NV':
        'NV',
    'NNV':
        'NNV',
    'Stille':
        'Lugnt',
    'Svag vind':
        'Svag vind',
    'Let vind':
        'Svag vind',
    'Let brise':
        'Måttlig vind',
    'Jævn vind':
        'Måttlig vind',
    'Frisk vind':
        'Frisk vind',
    'Kuling':
        'Frisk vind',
    'Hård kuling':
        'Styv kuling',
    'Stormende kuling':
        'Hård kuling',
    'Storm':
        'Halv storm',
    'Orkan':
        'Storm',
    'i vindøjet':
        'i vindögat',
    'skarp bidevind':
        'skarp bidevind',
    'bidevind':
        'bidevind',
    'halvvind':
        'halvvind',
    'rumskøds':
        'slör',
    'læns':
        'läns',
    'styrbords halse':
        'styrbords halsar',
    'bagbords halse':
        'babords halsar',
    'lige forfra':
        'rakt förifrån',
    'lige agterfra':
        'rakt akterifrån',
    'modsø':
        'motsjö',
    'tværsø':
        'tvärsjö',
    'medsø':
        'medsjö',
    'smult vande':
        'lugnt vatten',
    'sejldøgn|flertal':
        'etmål',
    'ben|flertal':
        'etapper',
    'døgn|flertal':
        'dygn',
    'timer|flertal':
        'timmar',
    'i vindøjet|sætning':
        'i vindögat',
    'skarp bidevind|sætning':
        'skarp bidevind',
    'bidevind|sætning':
        'bidevind',
    'halvvind|sætning':
        'halvvind',
    'rumskøds|sætning':
        'slör',
    'læns|sætning':
        'läns',
    'fortrængning':
        'deplacement',
    'halvplanende':
        'halvplanande',
    'planende':
        'planande',
}
