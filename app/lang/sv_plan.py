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
    'vendepunktet':
        'vändpunkten',
    '{sm} sømil · ca. {tid} {hvordan}':
        '{sm} distansminuter · ca {tid} {hvordan}',
    'Kræver {sejldøgn} — altså {overnatninger} undervejs, medmindre '
        'du slår mørkesejlads til.':
        'Kräver {sejldøgn} — alltså {overnatninger} längs vägen, om du '
        'inte slår på nattsegling.',
    'Ruten {navne} er på {sm} sømil fordelt på {ben}. ':
        'Rutten {navne} är {sm} distansminuter, fördelat på {ben}. ',
    'Vinden ligger mellem {fra} og {til} knob ({styrke} på det '
        'kraftigste)':
        'Vinden ligger mellan {fra} och {til} knop ({styrke} som mest)',
    'ud for {sted}':
        'utanför {sted}',
    'kurs {grader}° {retning}':
        'kurs {grader}° {retning}',
    'ved marchfart':
        'vid marschfart',
    'i jævn vind':
        'i måttlig vind',
    'Kan nås inden for ét sejldøgn ({fra}–{til}).':
        'Går att klara inom ett etmål ({fra}–{til}).',
    'Søen er til at leve med, og turen bør være behagelig.':
        'Sjön går att leva med, och resan bör bli behaglig.',
    'Marchfarten er {kn} knob, men søen tager omkring {tab} knob af '
        'den — du kommer frem med {snit} i snit':
        'Marschfarten är {kn} knop, men sjön tar omkring {tab} knop av '
        'den — du kommer fram med {snit} i snitt',
    'Marchfarten er {kn} knob, og den kan holdes stort set hele vejen '
        '({snit} i snit)':
        'Marschfarten är {kn} knop, och den går att hålla nästan hela '
        'vägen ({snit} i snitt)',
    'Vandet er så småt, at turen bliver stille og hurtig.':
        'Vattnet är så slätt att resan blir lugn och snabb.',
    ' — med {overnatninger} undervejs i {havne}.':
        ' — med {overnatninger} längs vägen i {havne}.',
    ' og drejer fra {fra} til {til} undervejs.':
        ' och vrider från {fra} till {til} under resan.',
    ' fra {retning} hele vejen.':
        ' från {retning} hela vägen.',
    ' Bølgerne når op på {m} meter.':
        ' Vågorna når upp till {m} meter.',
    ' Der er ingen nævneværdig søgang i prognosen.':
        ' Det finns ingen nämnvärd sjögång i prognosen.',
    'Du bliver formentlig blæst inde i {sted}. Efter ankomsten viser '
        'prognosen {døgn} i træk uden et vindue, du kan sejle i — op til '
        '{kn} knobs vind og {m} meter sø. ':
        'Du blir troligen vindfast i {sted}. Efter ankomsten visar '
        'prognosen {døgn} i rad utan ett fönster du kan segla i — upp '
        'till {kn} knops vind och {m} meter sjö. ',
    'Du bliver formentlig blæst inde i {sted}. Efter ankomsten viser '
        'prognosen {døgn} i træk uden et vindue, du kan sejle i — op til '
        '{kn} knobs vind. ':
        'Du blir troligen vindfast i {sted}. Efter ankomsten visar '
        'prognosen {døgn} i rad utan ett fönster du kan segla i — upp '
        'till {kn} knops vind. ',
    'Først {tidspunkt} er der noget at sejle i igen. Skal du på '
        'arbejde inden da, så vælg en anden afgang — eller en havn, du '
        'kommer hjem fra.':
        'Först {tidspunkt} finns det något att segla i igen. Ska du på '
        'jobb före dess, välj en annan avgång — eller en hamn du kommer '
        'hem från.',
    'Ankomst':
        'Ankomst',
    'Varighed':
        'Varaktighet',
    'Ophold':
        'Uppehåll',
    'OVERBLIK':
        'ÖVERBLICK',
    'VÆR OPMÆRKSOM PÅ':
        'VAR UPPMÄRKSAM PÅ',
    'STRÆK FOR STRÆK':
        'STRÄCKA FÖR STRÄCKA',
    'TIME FOR TIME':
        'TIMME FÖR TIMME',
    'Tid            Vind        Bølger  Fart   Sejlføring':
        'Tid            Vind        Vågor   Fart   Segelföring',
    'kn':
        'kn',
    'm':
        'm',
    'Prognoser er prognoser. Planen erstatter ikke søkort, '
        'farvandsudsigt eller almindelig sømandskab.':
        'Prognoser är prognoser. Planen ersätter inte sjökort, '
        'sjöväderrapport eller vanligt sjömanskap.',
    '{sm} sømil, {tid} undervejs.':
        '{sm} distansminuter, {tid} till sjöss.',
    'Der er næsten ingen sø. Det bliver en behagelig tur.':
        'Det är nästan ingen sjö. Det blir en behaglig resa.',
    'Søen kommer ind forfra det meste af vejen. Båden stamper, og der '
        'bliver vådt på fordækket — hold godt fast under skiftene.':
        'Sjön kommer in förifrån största delen av vägen. Båten stampar, '
        'och det blir vått på fördäck — håll i dig ordentligt vid '
        'skiftena.',
    'Der er sø nok til at man mærker den. Sørg for at alt er surret, '
        'og at kabyssen kan bruges med én hånd.':
        'Det är sjö nog för att man ska märka den. Se till att allt är '
        'surrat och att pentryt går att använda med en hand.',
    'Der går omkring {liter} liter brændstof på turen.':
        'Det går åt omkring {liter} liter bränsle på resan.',
    'Vejrudsigten rækker ikke hele vejen. Kaster du los {afgang}, når '
        'du {nået} sømil på {tid} under vejs med {båd}, før prognosen '
        'slipper op {slut}':
        'Väderprognosen räcker inte hela vägen. Kastar du loss {afgang} '
        'når du {nået} distansminuter på {tid} till sjöss med {båd}, '
        'innan prognosen tar slut {slut}',
    'Med {båd} tager den beregnet {tid} under vejs. Du kaster los '
        '{afgang} og er fremme {ankomst}':
        'Med {båd} tar den beräknat {tid} till sjöss. Du kastar loss '
        '{afgang} och är framme {ankomst}',
    ' i én stræk.':
        ' i ett enda sträck.',
    '{n} af timerne er så vindsvage, at motoren må hjælpe':
        '{n} av timmarna är så vindsvaga att motorn måste hjälpa till',
    '{n} timer ligger uden for dit sejldøgn':
        '{n} timmar ligger utanför ditt etmål',
    'vindstødene går op til {kn} knob, altså noget over middelvinden':
        'vindbyarna går upp till {kn} knop, alltså en bit över '
        'medelvinden',
    'Dag {nr} · {dato}: {fra} → {til}, {sm} sømil, {afgang}–{ankomst} '
        '({tid} under vejs).':
        'Dag {nr} · {dato}: {fra} → {til}, {sm} distansminuter, '
        '{afgang}–{ankomst} ({tid} till sjöss).',
    'Og det holder ikke op, før prognosen gør: den rækker til {dato}, '
        'og der blæser det stadig. Regn med at ligge stille, til vejret '
        'vender, og læg hjemturen som en tur for sig.':
        'Och det upphör inte innan prognosen gör det: den räcker till '
        '{dato}, och då blåser det fortfarande. Räkna med att ligga '
        'stilla tills vädret vänder, och planera hemresan för sig.',
    '{sm} sømil':
        '{sm} distansminuter',
    '{tid} under vejs · snitfart {kn} knob':
        '{tid} till sjöss · snittfart {kn} knop',
    'DAG FOR DAG':
        'DAG FÖR DAG',
    'Vinden står {kn} knob fra {retning}.':
        'Vinden står {kn} knop från {retning}.',
    'Vinden står {fra}–{til} knob fra {retning}.':
        'Vinden står {fra}–{til} knop från {retning}.',
    '{tid} af det for motor.':
        '{tid} av det för motor.',
    'Strækket brydes af natten i {havn} — timerne dér er ikke talt '
        'med.':
        'Sträckan bryts av natten i {havn} — timmarna där är inte '
        'medräknade.',
    'Søen står ind forfra. Det banker i skroget, og det bliver en '
        'tur, hvor man tager farten af og sætter den på igen.':
        'Sjön står in förifrån. Det bankar i skrovet, och det blir en '
        'resa där man tar av farten och lägger på den igen.',
    'Søen står ind forfra. Der er stampen i det, men båden bliver '
        'ved.':
        'Sjön står in förifrån. Det stampar, men båten går på.',
    'Søen kommer skråt ind. Regn med rulning — sørg for at alt står '
        'fast.':
        'Sjön kommer in snett. Räkna med rullning — se till att allt står '
        'fast.',
    'Der er lidt sø, men ikke nok til at det bliver ubehageligt.':
        'Det är lite sjö, men inte nog för att det ska bli obehagligt.',
    ' Store dele af turen ligger i vindøjet og skal krydses.':
        ' Stora delar av resan ligger i vindögat och måste kryssas.',
    ' Det meste sejles for {sejlføring}.':
        ' Det mesta seglas för {sejlføring}.',
    'Turen slutter {døgn} ude i prognosen. Så langt frem er en '
        'vejrudsigt en tendens, ikke en tidsplan: retningen holder tit, '
        'men styrken og timerne rykker sig. Læg planen, og se den efter '
        'igen et par dage før afgang.':
        'Resan slutar {døgn} ut i prognosen. Så långt fram är en '
        'väderprognos en tendens, inte en tidtabell: riktningen håller '
        'ofta, men styrkan och timmarna flyttar sig. Lägg planen, och se '
        'över den igen ett par dagar före avgång.',
    'Turen når ikke frem inden for den vejrudsigt, vi har. Du kommer '
        '{nået} af {ialt} sømil — de sidste {rest} sømil kan først '
        'planlægges, når prognosen rækker så langt. Læg turen tidligere, '
        'eller planlæg den sidste del om nogle dage.':
        'Resan når inte fram inom den väderprognos vi har. Du kommer '
        '{nået} av {ialt} distansminuter — de sista {rest} '
        'distansminuterna kan planeras först när prognosen räcker så '
        'långt. Lägg resan tidigare, eller planera sista biten om några '
        'dagar.',
    'Turen kan ikke sejles inden for ét sejldøgn. Planen lægger '
        '{overnatninger} ind — første gang i {havn} kl. {tid}. Vil du '
        'hele vejen i én stræk, skal du slå mørkesejlads til.':
        'Resan går inte att segla inom ett etmål. Planen lägger in '
        '{overnatninger} — första gången i {havn} kl. {tid}. Vill du hela '
        'vägen i ett sträck måste du slå på nattsegling.',
    'Du ligger fortøjet i {havn} allerede kl. {tid}, og der er timer '
        'tilbage af dagen. Det er med vilje: næste stræk er for langt til '
        'at nås inden kl. {slut}:00, og der er ingen havn imellem. Sejler '
        'du videre nu, ender du i mørke.':
        'Du ligger förtöjd i {havn} redan kl. {tid}, och det finns timmar '
        'kvar av dagen. Det är med avsikt: nästa sträcka är för lång för '
        'att hinnas före kl. {slut}:00, och det finns ingen hamn '
        'däremellan. Seglar du vidare nu slutar du i mörker.',
    '{n} timer ligger over dine grænser — fra {hvornår}. Der er op '
        'til {kn} knob og {m} meter bølger. Overvej at udskyde eller søge '
        'havn undervejs.':
        '{n} timmar ligger över dina gränser — från {hvornår}. Det är upp '
        'till {kn} knop och {m} meter vågor. Överväg att skjuta upp eller '
        'söka hamn längs vägen.',
    '{n} timer sejles uden for sejldøgnet, første gang omkring {tid}. '
        'Sørg for lanterner, vagtplan og at besætningen er udhvilet.':
        '{n} timmar seglas utanför etmålet, första gången omkring {tid}. '
        'Se till att ha lanternor, vaktschema och en utvilad besättning.',
    'Vindstødene når {kn} knob. Middelvinden holder sig lavere, men '
        '{hvad} skal passe til stødene, ikke til middelværdien.':
        'Vindbyarna når {kn} knop. Medelvinden håller sig lägre, men '
        '{hvad} ska passa till byarna, inte till medelvärdet.',
    'Regn med omkring {liter} liter brændstof. Læg en fjerdedel oveni '
        'til reserve og til at ligge og vente.':
        'Räkna med omkring {liter} liter bränsle. Lägg en fjärdedel '
        'ovanpå till reserv och till att ligga och vänta.',
    'Den længste dag er på {tid} i træk. Aftal hvem der styrer '
        'hvornår, og hvor I kan afbryde undervejs.':
        'Den längsta dagen är {tid} i sträck. Kom överens om vem som styr '
        'när, och var ni kan avbryta längs vägen.',
    'Prognosen holder sig inden for dine grænser hele vejen, og du er '
        'i havn inden sejldøgnet er omme. Det ser ud til at blive en god '
        'tur.':
        'Prognosen håller sig inom dina gränser hela vägen, och du är i '
        'hamn innan etmålet är slut. Det ser ut att bli en bra resa.',
    'SEJLPLAN':
        'SEGLINGSPLAN',
    'ca. {liter} liter':
        'ca {liter} liter',
    'Farten svinger mellem {fra} og {til} knob.':
        'Farten pendlar mellan {fra} och {til} knop.',
    'Der holdes {kn} knob.':
        'Farten ligger på {kn} knop.',
    'Der er for lidt vind til at sejle strækket — motoren må trække '
        'det meste af vejen.':
        'Det är för lite vind för att segla sträckan — motorn får dra '
        'största delen av vägen.',
    'Bølger op til {m} meter.':
        'Vågor upp till {m} meter.',
    'Bølger op til {m} meter i {sø}.':
        'Vågor upp till {m} meter i {sø}.',
    'Du er først fortøjet i {havn} kl. {tid} — efter dit sejldøgn, '
        'der slutter {slut}:00. Der var ingen havn tættere på, du kunne '
        'nå. Overvej at afgå tidligere, eller at lægge et stop ind før.':
        'Du är förtöjd i {havn} först kl. {tid} — efter ditt etmål, som '
        'slutar {slut}:00. Det fanns ingen närmare hamn du kunde nå. '
        'Överväg att avgå tidigare, eller att lägga in ett stopp innan.',
    '{n} timer nærmer sig dine grænser ({kn} knob og {m} meter). '
        '{råd}, og hold øje med om prognosen flytter sig.':
        '{n} timmar närmar sig dina gränser ({kn} knop och {m} meter). '
        '{råd}, och håll koll på om prognosen flyttar sig.',
    'Kursen ligger så tæt på vinden, at strækket skal krydses.':
        'Kursen ligger så nära vinden att sträckan måste kryssas.',
    'Det sejles for {sejlføring} på {halse}.':
        'Det seglas för {sejlføring} för {halse}.',
    'farten':
        'farten',
    'rebningen':
        'revningen',
    'Sæt farten ned i tide':
        'Ta ner farten i tid',
    'Reb i god tid':
        'Reva i god tid',
    '{n} timer sejles i mørke':
        '{n} timmar seglas i mörker',
    '{n} timer sejles i mørke. Solen går ned {solned}, og du er '
        'stadig undervejs. Sørg for lanterner, vagtplan og at besætningen '
        'er udhvilet.':
        '{n} timmar seglas i mörker. Solen går ner {solned}, och du är '
        'fortfarande till sjöss. Se till att ha lanternor, vaktschema '
        'och en utvilad besättning.',
    '{n} timer sejles i mørke, første gang omkring {tid}. Sørg for '
        'lanterner, vagtplan og at besætningen er udhvilet.':
        '{n} timmar seglas i mörker, första gången omkring {tid}. Se till '
        'att ha lanternor, vaktschema och en utvilad besättning.',
}
