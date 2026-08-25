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
    'Kom i gang':
        'Kom igång',
    'Sådan bruges Sejlplan':
        'Så används Seglingsplan',
    'Tre trin: læg ruten, vælg hvornår du kaster los, læs planen.':
        'Tre steg: lägg rutten, välj när du kastar loss, läs planen.',
    'Først lægger du ruten — mindst to punkter. Søg efter en havn, '
        'klik på kortet, eller slå havnelaget til og vælg en havn. '
        'Sejlplan lægger selv vejen uden om land.':
        'Först lägger du rutten — minst två punkter. Sök efter en hamn, '
        'klicka på kartan, eller slå på hamnlagret och välj en hamn. '
        'Seglingsplan lägger själv vägen runt land.',
    'Så trykker du Find bedste afgangstider. Vi regner hver eneste '
        'afgangstime igennem i det vindue, du har valgt, og viser dem, '
        'der giver noget forskelligt. Vi peger på én, men du vælger.':
        'Sedan trycker du på Hitta bästa avgångstider. Vi räknar igenom '
        'varje enskild avgångstimme i det fönster du har valt och visar '
        'dem som ger något annat. Vi pekar på en, men du väljer.',
    'Til sidst står sejlplanen: hvad turen bliver, dag for dag, stræk '
        'for stræk og time for time. Den kan printes, kopieres og læses '
        'uden dækning.':
        'Till sist står seglingsplanen: vad resan blir, dag för dag, '
        'sträcka för sträcka och timme för timme. Den går att skriva ut, '
        'kopiera och läsa utan täckning.',
    'Ruten og havvejen':
        'Rutten och sjövägen',
    'Stregen følger vandet, ikke luftlinjen — derfor er den længere.':
        'Strecket följer vattnet, inte fågelvägen — därför är det längre.',
    'Sejlplan lægger ruten uden om land med en søkortsagtig maske '
        'over de danske og skandinaviske farvande. Derfor står der tit '
        '"3,7 sm udenom land" ved et ben: det er, hvad det koster at '
        'komme rundt om pynten i stedet for at sejle gennem den.':
        'Seglingsplan lägger rutten runt land med en sjökortsliknande '
        'mask över de danska och skandinaviska farvattnen. Därför står '
        'det ofta ”3,7 M runt land” vid en etapp: det är vad det kostar '
        'att komma runt udden i stället för att segla genom den.',
    'Masken kender land og vand — den kender ikke dybder, sømærker, '
        'ruser eller sejlrender. Kontrollér altid benene på søkortet, '
        'især i smalt farvand og tæt på kysten.':
        'Masken känner land och vatten — den känner inte djup, sjömärken, '
        'ryssjor eller farleder. Kontrollera alltid etapperna på '
        'sjökortet, särskilt i trångt farvatten och nära kusten.',
    'Du kan trække et punkt på kortet, flytte det op og ned i listen, '
        'og vende hele ruten om under dele-ikonet.':
        'Du kan dra en punkt på kartan, flytta den upp och ner i listan, '
        'och vända hela rutten under delningsikonen.',
    'Din båd':
        'Din båt',
    'Planen er kun din, hvis den regner på din båds fart.':
        'Planen är bara din om den räknar på din båts fart.',
    'De faste både er eksempler. Ingen ejer et eksempel, og en plan, '
        'der regner på en anden båds fart, er ikke din plan. Læg din egen '
        'ind under Indstillinger.':
        'De färdiga båtarna är exempel. Ingen äger ett exempel, och en '
        'plan som räknar på en annan båts fart är inte din plan. Lägg in '
        'din egen under Inställningar.',
    'For en sejlbåd kan du søge den i registret — omkring 130 både, '
        'man møder i danske og nordiske havne. Så udfyldes længde og fart '
        'af fabrikantens mål.':
        'En segelbåt kan du söka i registret — omkring 130 båtar som man '
        'möter i danska och nordiska hamnar. Då fylls längd och fart i '
        'från varvets mått.',
    'For en motorbåd spørger vi om marchfart, skrogtype og forbrug. '
        'Skroget afgør, hvor meget søen tager af farten: en planende båd '
        'taber mest, fordi den må ned i fortrængning i en stejl modsø.':
        'För en motorbåt frågar vi om marschfart, skrovtyp och '
        'förbrukning. Skrovet avgör hur mycket sjön tar av farten: en '
        'planande båt förlorar mest, eftersom den måste ner i '
        'deplacementsfart i en brant motsjö.',
    'Fart for halvvind i 10 knobs vind':
        'Fart för halvvind i 10 knops vind',
    'Ét tal, der skalerer et polardiagram op eller ned til din båd.':
        'En enda siffra som skalar ett polardiagram upp eller ner till '
        'din båt.',
    'Et rigtigt polardiagram er en måling af netop din båd med netop '
        'dine sejl. Det har de færreste liggende. Så vi spørger om ét '
        'tal, enhver sejler kender — farten med vinden ind fra siden i en '
        'jævn brise — og skalerer en almindelig krydsers diagram, så det '
        'rammer dit tal.':
        'Ett riktigt polardiagram är en mätning av just din båt med just '
        'dina segel. Det är det få som har. Så vi frågar efter en '
        'siffra som varje seglare kan — farten med vinden in från sidan i '
        'en måttlig bris — och skalar en vanlig kryssares diagram så att '
        'det träffar din siffra.',
    'Vælger du din båd i registret, regnes tallet af sejlareal, '
        'deplacement og vandlinje. Det er et kvalificeret skøn, ikke en '
        'måling, og du kan altid rette det.':
        'Väljer du din båt i registret räknas siffran fram ur segelyta, '
        'deplacement och vattenlinje. Det är en kvalificerad '
        'uppskattning, inte en mätning, och du kan alltid ändra den.',
    'Ligger kursen tættere på vinden, end båden kan sejle, regner '
        'planen med, at du krydser: fremdriften mod målet, ikke farten '
        'gennem vandet.':
        'Ligger kursen närmare vinden än båten kan segla räknar planen '
        'med att du kryssar: med framdriften mot målet, inte med farten '
        'genom vattnet.',
    'Komfortgrænser':
        'Komfortgränser',
    'Over dem markeres timerne — det er dine grænser, ikke bådens.':
        'Över dem markeras timmarna — det är dina gränser, inte båtens.',
    'Vind og bølger over grænsen giver skærpede timer, og et stykke '
        'over dem frarådede. Det handler om, hvad du og besætningen kan '
        'holde til, ikke om hvad båden kan bære.':
        'Vind och vågor över gränsen ger skärpta timmar, och en bit över '
        'dem avrådda. Det handlar om vad du och besättningen tål, inte om '
        'vad båten bär.',
    'Bølgehøjden vejes efter, hvor søen kommer fra. Modsø tæller '
        'hårdere end tværsø, og medsø mildest — det er dét, man mærker.':
        'Våghöjden vägs efter var sjön kommer ifrån. Motsjö räknas '
        'hårdare än tvärsjö, och medsjö mildast — det är det man känner.',
    'Grænserne bruges også til at afgøre, om du bliver blæst inde på '
        'destinationen. Sætter du dem urealistisk højt, forsvinder den '
        'advarsel.':
        'Gränserna används också för att avgöra om du blir vindfast på '
        'destinationen. Sätter du dem orealistiskt högt försvinner den '
        'varningen.',
    'Tid og vejr':
        'Tid och väder',
    'Sejldøgn':
        'Etmål',
    'Sluttidspunktet er, hvornår du vil ligge fortøjet — ikke afgå.':
        'Sluttiden är när du vill ligga förtöjd — inte när du avgår.',
    'Siger du 07–20, betyder det ikke "afgå senest kl. 20". Det '
        'betyder: ligge fortøjet kl. 20. Rækker turen ikke inden for '
        'døgnet, deler Sejlplan den og finder en havn undervejs at '
        'overnatte i.':
        'Säger du 07–20 betyder det inte ”avgå senast kl. 20”. Det '
        'betyder: ligga förtöjd kl. 20. Räcker resan inte inom dygnet '
        'delar Seglingsplan den och hittar en hamn längs vägen att '
        'övernatta i.',
    'Derfor kan planen finde på at lægge til i en havn midt på dagen. '
        'Det er med vilje: er næste stræk for langt til at nås inden '
        'lukketid, og er der ingen havn imellem, ender man i mørke.':
        'Därför kan planen hitta på att lägga till i en hamn mitt på '
        'dagen. Det är med avsikt: är nästa sträcka för lång för att '
        'hinnas före stängning, och finns det ingen hamn däremellan, '
        'hamnar man i mörker.',
    'Vil du hele vejen i ét stræk, så slå mørkesejlads til under '
        'Indstillinger. Så lægges der ingen overnatninger ind, og '
        'mørketimerne tælles for sig.':
        'Vill du hela vägen i ett sträck, slå på nattsegling under '
        'Inställningar. Då läggs inga övernattningar in, och '
        'mörkertimmarna räknas för sig.',
    'Afgangstiderne':
        'Avgångstiderna',
    'Alle de afgange, der giver noget forskelligt. Du vælger.':
        'Alla avgångar som ger något annat. Du väljer.',
    'Vi regner hver afgangstime igennem i dit vindue og viser dem, '
        'der ender forskelligt — forskellig ankomst, forskellige havne '
        'undervejs eller forskellige forhold. To afgange en time fra '
        'hinanden, der giver præcis det samme, står kun én gang.':
        'Vi räknar igenom varje avgångstimme i ditt fönster och visar dem '
        'som slutar olika — annan ankomst, andra hamnar längs vägen eller '
        'andra förhållanden. Två avgångar en timme från varandra som ger '
        'precis samma sak står bara en gång.',
    'Hver dag, du overhovedet kan sejle, er med. Ellers kunne en hel '
        'dag forsvinde, fordi en anden havde bedre vejr, og så vidste du '
        'ikke, at muligheden fandtes.':
        'Varje dag du överhuvudtaget kan segla är med. Annars kunde en '
        'hel dag försvinna för att en annan hade bättre väder, och då '
        'visste du inte att möjligheten fanns.',
    'Rækkefølgen er vores anbefaling — vi vægter frarådede timer '
        'tungest, så korte passager, og til sidst hvornår du er hjemme. '
        'Det er en anbefaling, ikke en afgørelse.':
        'Ordningen är vår rekommendation — vi väger avrådda timmar '
        'tyngst, sedan korta passager, och sist när du är hemma. Det är '
        'en rekommendation, inte ett avgörande.',
    'Strøm':
        'Ström',
    'Farten er over grunden. Strømmen er regnet med.':
        'Farten är över grund. Strömmen är inräknad.',
    'Farten i planen er over grunden — dét, der flytter båden — ikke '
        'gennem vandet. Strømmen langs kursen lægges til eller trækkes '
        'fra, og står i søjlen Strøm: grøn med, rød imod.':
        'Farten i planen är över grund — det som flyttar båten — inte '
        'genom vattnet. Strömmen längs kursen läggs till eller dras ifrån '
        'och står i kolumnen Ström: grön med, röd mot.',
    'Står strømmen tværs, tæller den ikke på farten. Til gengæld '
        'sætter den af til siden, og det skal styres op — planen regner '
        'ikke afdriften ud for dig.':
        'Står strömmen tvärs räknas den inte på farten. Däremot sätter '
        'den av åt sidan, och det måste styras upp — planen räknar inte '
        'ut avdriften åt dig.',
    'Tallene kommer fra en global havmodel, og den opløser ikke de '
        'danske bælter helt. I Storebælt og Grønsund kan der løbe to-tre '
        'knob, hvor modellen viser under én. Brug den som en retning, og '
        'slå strømtabellen op, når det gælder en smal passage.':
        'Siffrorna kommer från en global havsmodell, och den löser inte '
        'upp de danska bälten helt. I Stora Bält och Grönsund kan det '
        'löpa två-tre knop där modellen visar under ett. Använd den som '
        'en riktning, och slå upp strömtabellen när det gäller en trång '
        'passage.',
    'Hvor langt frem vi kan se':
        'Hur långt fram vi kan se',
    'Ti døgn. Bølgerne er loftet, ikke vinden.':
        'Tio dygn. Vågorna är taket, inte vinden.',
    'Vinden rækker fjorten døgn frem, bølgerne ti. En sejlplan uden '
        'søen er en halv plan, så ti døgn er grænsen.':
        'Vinden räcker fjorton dygn fram, vågorna tio. En seglingsplan '
        'utan sjön är en halv plan, så tio dygn är gränsen.',
    'De første tre-fire døgn holder ret godt. Derefter er det '
        'retningen, der overlever, ikke timerne — og det står i planen, '
        'når turen slutter fem døgn eller mere ude.':
        'De första tre-fyra dygnen håller ganska bra. Därefter är det '
        'riktningen som överlever, inte timmarna — och det står i planen '
        'när resan slutar fem dygn eller mer bort.',
    'Rækker prognosen ikke hele vejen, siger planen, hvor langt du '
        'når, i stedet for at påstå en ankomst. Læg turen tidligere, '
        'eller planlæg den sidste del om nogle dage.':
        'Räcker prognosen inte hela vägen säger planen hur långt du når i '
        'stället för att påstå en ankomst. Lägg resan tidigare, eller '
        'planera sista biten om några dagar.',
    'Blæst inde':
        'Vindfast',
    'Om du kommer væk igen — ikke kun om du kommer derhen.':
        'Om du kommer bort igen — inte bara om du kommer dit.',
    'Man kigger på vejret frem til man er fremme, og ikke længere. Så '
        'sejler man til Marstal i det pæneste vejr og opdager i havnen, '
        'at det blæser femogtyve knob i tre døgn.':
        'Man tittar på vädret fram till att man är framme, och inte '
        'längre. Så seglar man till Marstal i det finaste vädret och '
        'upptäcker i hamnen att det blåser tjugofem knop i tre dygn.',
    'Sejlplan kigger videre for dig. Fra ankomsten og til prognosen '
        'slipper op tælles det efter, om der er et sejlbart døgn tilbage. '
        'Er der to eller flere døgn i træk uden, står det i planen — med '
        'hvornår vinduet åbner igen.':
        'Seglingsplan tittar vidare åt dig. Från ankomsten och tills '
        'prognosen tar slut räknas det efter om det finns ett segelbart '
        'dygn kvar. Är det två eller fler dygn i rad utan, står det i '
        'planen — med när fönstret öppnar igen.',
    'Holder det ikke op, før prognosen gør, får du det at vide som '
        'dét: vi ved ikke hvornår. Så er hjemturen en tur for sig.':
        'Upphör det inte innan prognosen gör det får du veta just det: vi '
        'vet inte när. Då är hemresan en resa för sig.',
    'Sejlplanen':
        'Seglingsplanen',
    'Stræk for stræk':
        'Sträcka för sträcka',
    'Delt op dér, hvor kursen skifter — ikke hvor du satte et kryds.':
        'Delad där kursen ändras — inte där du satte ett kryss.',
    'Sætter du Køge og Præstø ind, er det ét ben. Men det sejles mod '
        'øst, så mod syd og til sidst mod vest, og en plan, der giver én '
        'kurs for det hele, passer ingen af stederne.':
        'Sätter du in Køge och Præstø är det en etapp. Men den seglas '
        'mot öster, sedan mot söder och till sist mot väster, och en plan '
        'som ger en enda kurs för alltihop passar ingenstans.',
    'Derfor deles turen dér, hvor du faktisk skal dreje. Hvert stræk '
        'har sin kurs, sin vind, sin sø og sin sejlføring — og de gælder '
        'præcis dér, hvor du styrer den kurs.':
        'Därför delas resan där du faktiskt ska gira. Varje sträcka har '
        'sin kurs, sin vind, sin sjö och sin segelföring — och de gäller '
        'precis där du styr den kursen.',
    'Bliver et stræk brudt af en overnatning, står det i teksten. '
        'Timerne ved kaj tæller ikke med.':
        'Bryts en sträcka av en övernattning står det i texten. Timmarna '
        'vid kaj räknas inte med.',
    'Nøgletallene':
        'Nyckeltalen',
    'Under vejs er den rigtige tid fra kaj til kaj.':
        'Till sjöss är den riktiga tiden från kaj till kaj.',
    '"Under vejs" er tiden fra du kaster los, til du ligger fortøjet, '
        'lagt sammen for alle døgnene. Havnetimerne tæller ikke med.':
        '”Till sjöss” är tiden från att du kastar loss tills du ligger '
        'förtöjd, sammanlagt för alla dygnen. Hamntimmarna räknas inte '
        'med.',
    'Gennemsnitsfarten er distancen delt med den tid. Distance, tid '
        'og fart passer sammen — du kan regne efter.':
        'Snittfarten är distansen delad med den tiden. Distans, tid och '
        'fart stämmer överens — du kan räkna efter.',
    'Frarådede timer er dem, der ligger et stykke over dine grænser. '
        'Er der nogen, skal du tage stilling til dem, før du kaster los.':
        'Avrådda timmar är de som ligger en bit över dina gränser. Finns '
        'det några måste du ta ställning till dem innan du kastar loss.',
    'Time for time':
        'Timme för timme',
    'Grøn er god, gul er skærpet, rød frarådes — efter dine grænser.':
        'Grön är bra, gul är skärpt, röd avrådes — efter dina gränser.',
    'Hver række er én sejltime på det sted, du er nået til: vinden, '
        'hvor den kommer fra, bølgerne, farten og sejlføringen.':
        'Varje rad är en seglingstimme på den plats du har nått: vinden, '
        'varifrån den kommer, vågorna, farten och segelföringen.',
    'Farven kommer af dine egne komfortgrænser. Grøn er inden for '
        'dem, gul er lidt over, rød er et stykke over.':
        'Färgen kommer av dina egna komfortgränser. Grön är inom dem, gul '
        'är lite över, röd är en bit över.',
    'Står der "motor", er der for lidt vind til at sejle — under tre '
        'knobs fart tændes motoren i beregningen, hvis du har slået det '
        'til.':
        'Står det ”motor” är det för lite vind för att segla — under tre '
        'knops fart startas motorn i beräkningen, om du har slagit på '
        'det.',
    'Havne undervejs':
        'Hamnar längs vägen',
    'Steder du kan søge ind, hvis vejret skifter.':
        'Ställen du kan söka skydd i om vädret slår om.',
    'Listen er de havne, der ligger tæt nok på ruten til at være et '
        'rimeligt sted at gå ind — op til seks sømil fra vejen. Klik på '
        'en for at lægge den ind som mellemstop.':
        'Listan är de hamnar som ligger nära nog rutten för att vara ett '
        'rimligt ställe att gå in i — upp till sex distansminuter från '
        'vägen. Klicka på en för att lägga in den som mellanstopp.',
    'Vi tjekker, at man kan sejle lige ind til dem fra ruten, så et '
        'forslag aldrig kræver, at du sejler uden om en ø.':
        'Vi kontrollerar att man kan segla rakt in till dem från rutten, '
        'så att ett förslag aldrig kräver att du seglar runt en ö.',
    'Har havnen en side i havnelods.dk, er der et lille ikon ved '
        'siden af. Dér står pladser, priser, faciliteter og indsejling. '
        'Mangler ikonet, kender vi ikke havnens side — så er det bedre at '
        'lade være end at sende dig det forkerte sted hen.':
        'Har hamnen en sida på havnelods.dk finns en liten ikon bredvid. '
        'Där står platser, priser, faciliteter och infart. Saknas ikonen '
        'känner vi inte hamnens sida — då är det bättre att låta bli än '
        'att skicka dig fel.',
    'Er der plads i havnen?':
        'Finns det plats i hamnen?',
    'Det eneste, ingen model kan svare på. Kun dem, der ligger der.':
        'Det enda ingen modell kan svara på. Bara de som ligger där.',
    'Vejret kommer fra en model og afstanden fra et søkort. Om der er '
        'en plads tilbage ved ydermolen klokken fire, ved kun den, der '
        'ligger der klokken to.':
        'Vädret kommer från en modell och avståndet från ett sjökort. Om '
        'det finns en plats kvar vid ytterpiren klockan fyra vet bara den '
        'som ligger där klockan två.',
    'Derfor kan man melde: god plads, få pladser, eller fuld. Det '
        'tager to sekunder, det er anonymt, og der gemmes kun havnen, '
        'svaret og hvornår. Der er ikke noget at skrive — og dermed '
        'heller ikke et sted, hvor nogen kan skrive noget til nogen.':
        'Därför kan man rapportera: gott om plats, få platser, eller fullt. '
        'Det tar två sekunder, det är anonymt, och bara hamnen, svaret '
        'och när sparas. Det finns inget att skriva — och därmed inte '
        'heller något ställe där någon kan skriva något till någon.',
    'Alderen står altid med, for den er halvdelen af oplysningen. '
        '"Fuld" for tre timer siden er noget andet end "fuld" i går '
        'aftes. Efter halvandet døgn forsvinder meldingen af sig selv.':
        'Åldern står alltid med, för den är hälften av upplysningen. '
        '”Fullt” för tre timmar sedan är något annat än ”fullt” i går '
        'kväll. Efter ett och ett halvt dygn försvinner rapporten av sig '
        'själv.',
    'Ligger du i en havn, så meld. Det koster dig ingenting og er det '
        'eneste, den næste ikke kan finde ud af på egen hånd.':
        'Ligger du i en hamn, rapportera. Det kostar dig ingenting och är det '
        'enda den nästa inte kan lista ut på egen hand.',
    'Undervejs':
        'Till sjöss',
    'Undervejs: foran eller bagud?':
        'Till sjöss: före eller efter?',
    'Telefonens position mod planens — hvornår er du så fremme?':
        'Telefonens position mot planens — när är du då framme?',
    'Planen bliver lagt i havnen. Undervejs er spørgsmålet et andet: '
        'er jeg foran eller bagud, og hvornår er jeg så fremme i '
        'virkeligheden. Tryk "Jeg er undervejs" i sejlplanen.':
        'Planen läggs i hamnen. Till sjöss är frågan en annan: ligger '
        'jag före eller efter, och när är jag då framme i verkligheten? '
        'Tryck på ”Jag är till sjöss” i seglingsplanen.',
    'Vi finder det punkt på ruten, du er tættest på, og slår op i '
        'planens eget spor, hvor langt du skulle have været på det '
        'klokkeslæt. Ligger du mere end tre sømil fra ruten, siger vi '
        'ingenting — så betyder et forspring heller ingenting.':
        'Vi hittar den punkt på rutten du är närmast och slår upp i '
        'planens eget spår hur långt du skulle ha varit vid den tiden. '
        'Ligger du mer än tre distansminuter från rutten säger vi '
        'ingenting — då betyder ett försprång heller ingenting.',
    'Positionen bliver på din telefon og i den ene beregning. Den '
        'gemmes ikke, og ingen andre kan se den. At vise sig for andre er '
        'en anden funktion, man selv skal tænde.':
        'Positionen stannar i din telefon och i den enda beräkningen. Den '
        'sparas inte, och ingen annan kan se den. Att visa sig för andra '
        'är en annan funktion som du själv måste slå på.',
    'På iPhone virker positionen kun, mens skærmen er tændt og '
        'Sejlplan er fremme. Låser du telefonen, holder den op. Det er '
        'iOS, der bestemmer det.':
        'På iPhone fungerar positionen bara medan skärmen är på och '
        'Seglingsplan är framme. Låser du telefonen slutar den. Det är '
        'iOS som bestämmer det.',
    'Se andre både':
        'Se andra båtar',
    'Usynlig til du selv tænder — og du ser kun dem, der også har.':
        'Osynlig tills du själv slår på det — och du ser bara dem som '
        'också har.',
    'Tryk "Vis min båd for andre" og vælg et bådnavn. Så kan andre, '
        'der også er synlige, se hvor du er, og du kan se dem. Kun jer, '
        'der har slået det til.':
        'Tryck på ”Visa min båt för andra” och välj ett båtnamn. Då kan '
        'andra som också syns se var du är, och du kan se dem. Bara ni '
        'som har slagit på det.',
    'Du ser kun andre, mens du selv er synlig. Ingen kan ligge og '
        'kigge uden at være der selv. Slukker du, forsvinder du fra deres '
        'kort og de fra dit i samme øjeblik — og din position bliver '
        'slettet, ikke skjult.':
        'Du ser bara andra medan du själv syns. Ingen kan ligga och titta '
        'utan att vara där själv. Slår du av försvinner du från deras '
        'karta och de från din i samma stund — och din position raderas, '
        'den döljs inte.',
    'Positionen udløber af sig selv efter en halv time uden '
        'opdatering. Der gemmes ingen historik: hver ny position skriver '
        'den forrige over, så ingen kan slå op, hvor du var i går.':
        'Positionen går ut av sig själv efter en halvtimme utan '
        'uppdatering. Ingen historik sparas: varje ny position skriver '
        'över den förra, så ingen kan slå upp var du var i går.',
    'Skriv bådens navn, ikke dit eget — det er dét, de andre ser. Ser '
        'du ingen både, er der ingen inden for tres sømil, der har tændt.':
        'Skriv båtens namn, inte ditt eget — det är det de andra ser. Ser '
        'du inga båtar finns det ingen inom sextio distansminuter som har '
        'slagit på det.',
    'Beskeder mellem både':
        'Meddelanden mellan båtar',
    'Tryk på en båd på kortet og skriv. Kun mellem synlige både.':
        'Tryck på en båt på kartan och skriv. Bara mellan synliga båtar.',
    'Det er ikke en indbakke med fremmede og ikke en opslagstavle — '
        'det er en samtale mellem to, der ligger i det samme farvand lige '
        'nu, og som begge har valgt at være synlige.':
        'Det är ingen inkorg med främlingar och ingen anslagstavla — det '
        'är ett samtal mellan två som ligger i samma farvatten just nu '
        'och som båda har valt att synas.',
    'Har nogen skrevet, står der en prik på båden på kortet og et tal '
        'i panelet. Beskeder forsvinder efter et døgn.':
        'Har någon skrivit står det en prick på båten på kartan och en '
        'siffra i panelen. Meddelanden försvinner efter ett dygn.',
    'Bloker sidder i samtalens menu og virker begge veje med det '
        'samme: I kan hverken skrive til hinanden eller se hinanden på '
        'kortet. Anmeld sidder på selve beskeden — anmelder du en, gemmer '
        'vi teksten, for ellers ville den dø efter et døgn, og så stod '
        'ord mod ord.':
        'Blockera finns i samtalets meny och gäller åt båda håll med '
        'detsamma: ni kan varken skriva till varandra eller se varandra '
        'på kartan. Anmäl finns på själva meddelandet — anmäler du ett '
        'sparar vi texten, för annars skulle det dö efter ett dygn, och '
        'då stod ord mot ord.',
    'Skriver du tre gange til en, der ikke svarer, må du vente. Det '
        'er med vilje.':
        'Skriver du tre gånger till någon som inte svarar får du vänta. '
        'Det är med avsikt.',
    'Gem og tag med':
        'Spara och ta med',
    'Vejrvagt':
        'Vädervakt',
    'Sig til, når vejret er der — også om fjorten dage.':
        'Säg till när vädret är där — även om fjorton dagar.',
    'Skal turen først gå om tre uger, er der ingen prognose at kigge '
        'i endnu, og så skal man ikke sidde og trykke opdater hver dag. '
        'Læg en vagt på ruten, og få én mail, når der er et vindue.':
        'Ska resan först gå om tre veckor finns det ingen prognos att '
        'titta i ännu, och då ska man inte sitta och trycka på uppdatera '
        'varje dag. Lägg en vakt på rutten och få ett mejl när det finns '
        'ett fönster.',
    'Vagten venter, til prognosen når frem til dine datoer, og regner '
        'så turen igennem med din egen båd og dine egne grænser. Vi '
        'skriver kun, hvis du også kan komme hjem igen — er du blæst inde '
        'i tre døgn på destinationen, er det ikke en gevinst.':
        'Vakten väntar tills prognosen når fram till dina datum och '
        'räknar sedan igenom resan med din egen båt och dina egna '
        'gränser. Vi skriver bara om du också kan komma hem igen — är du '
        'vindfast i tre dygn på destinationen är det ingen vinst.',
    'Én vagt giver én besked. Ikke en strøm af mails, hver gang '
        'modellen flytter sig en halv knob. Kommer beskeden, er vagten '
        'brugt, og du lægger en ny.':
        'En vakt ger ett meddelande. Inte en ström av mejl varje gång '
        'modellen flyttar sig en halv knop. Kommer meddelandet är vakten '
        'förbrukad, och du lägger en ny.',
    'Vi skriver aldrig til en adresse, der ikke selv har bekræftet '
        'den, og hver mail bærer sit eget link til at stoppe.':
        'Vi skriver aldrig till en adress som inte själv har bekräftat '
        'den, och varje mejl bär sin egen länk för att sluta.',
    'Sprog':
        'Språk',
    'Dansk, tysk og svensk. Flaget i toppen skifter.':
        'Danska, tyska och svenska. Flaggan högst upp växlar.',
    'Flaget øverst på siden skifter sprog — tryk på det og vælg. Det '
        'står også under Indstillinger. Siden hentes forfra på det nye '
        'sprog.':
        'Flaggan högst upp på sidan växlar språk — tryck på den och välj. '
        'Den finns också under Inställningar. Sidan laddas om på det nya '
        'språket.',
    'Første besøg følger browserens eget førstevalg af sprog — er det '
        'ikke et af dem, vi har, får du dansk. Derefter vinder dit valg, '
        'og det gemmes hos dig selv, så det holder, også når vi lægger en '
        'ny udgave af Sejlplan ud.':
        'Första besöket följer webbläsarens eget förstahandsval av språk '
        '— är det inget av dem vi har, får du danska. Därefter vinner '
        'ditt val, och det sparas hos dig själv, så att det håller även '
        'när vi lägger ut en ny version av Seglingsplan.',
    'Er en tekst ikke oversat endnu, står den på dansk. Det er med '
        'vilje: en halvt oversat flade er brugbar, en flade med huller i '
        'er ikke.':
        'Är en text inte översatt ännu står den på danska. Det är med '
        'avsikt: ett halvöversatt gränssnitt är användbart, ett '
        'gränssnitt med hål i är det inte.',
    'Mine ruter':
        'Mina rutter',
    'Gem turen, og hent den frem igen, når prognosen når så langt.':
        'Spara resan och ta fram den igen när prognosen når så långt.',
    'En sommertur på fjorten dage kan ikke planlægges på én gang — '
        'prognosen rækker ti døgn. Men ruten kan lægges nu: afstande, '
        'ben, havne undervejs og hvor mange sejldøgn den kræver, regnes '
        'uden et gram vejr.':
        'En sommarresa på fjorton dagar går inte att planera på en gång — '
        'prognosen räcker tio dygn. Men rutten kan läggas nu: avstånd, '
        'etapper, hamnar längs vägen och hur många etmål den kräver '
        'räknas utan ett gram väder.',
    'Gem den, og hent den frem igen, efterhånden som prognosen ruller '
        'frem over din rute. Ét tryk på Gem opdaterer den, du arbejder i; '
        'vil du have en kopi, er der Gem som ny.':
        'Spara den och ta fram den igen allt eftersom prognosen rullar '
        'fram över din rutt. Ett tryck på Spara uppdaterar den du arbetar '
        'i; vill du ha en kopia finns Spara som ny.',
    'Ruterne ligger i din browser og i din session. De overlever, at '
        'vi lægger en ny version af Sejlplan ud.':
        'Rutterna ligger i din webbläsare och i din session. De överlever '
        'att vi lägger ut en ny version av Seglingsplan.',
    'Appen og uden dækning':
        'Appen och utan täckning',
    'Den seneste sejlplan kan læses uden forbindelse.':
        'Den senaste seglingsplanen går att läsa utan uppkoppling.',
    'Læg Sejlplan på hjemmeskærmen under Indstillinger, så åbner den '
        'i sit eget vindue uden browserlinje. På iPhone gør du det selv: '
        'åbn siden i Safari, tryk Del, vælg "Føj til hjemmeskærm".':
        'Lägg Seglingsplan på hemskärmen under Inställningar, så öppnas '
        'den i ett eget fönster utan webbläsarrad. På iPhone gör du det '
        'själv: öppna sidan i Safari, tryck på Dela, välj ”Lägg till på '
        'hemskärmen”.',
    'Du kan ikke lægge en rute uden dækning — beregningen sker på '
        'serveren. Men hver gang du åbner en sejlplan, lægges den ned i '
        'telefonen som et dokument, der kan stå alene. Går dækningen, '
        'kommer den frem: overblik, advarsler, dag for dag, stræk for '
        'stræk og hele timetabellen.':
        'Du kan inte lägga en rutt utan täckning — beräkningen sker på '
        'servern. Men varje gång du öppnar en seglingsplan läggs den ner '
        'i telefonen som ett dokument som kan stå för sig. Försvinner '
        'täckningen kommer den fram: överblick, varningar, dag för dag, '
        'sträcka för sträcka och hela timtabellen.',
    'De kortfliser, du har set på, gemmes også, så kortet kan vise '
        'det farvand, du lige har kigget på.':
        'De kartrutor du har tittat på sparas också, så att kartan kan '
        'visa det farvatten du just har tittat på.',
    'GPX til kortplotteren':
        'GPX till kartplottern',
    'Hele havvejen med, ikke bare dine punkter.':
        'Hela sjövägen med, inte bara dina punkter.',
    'Under dele-ikonet ligger Hent GPX til kortplotter. Filen '
        'indeholder dine egne punkter som waypoints, hele havvejen som '
        'rute med knækpunkterne uden om land, og den samme vej som spor.':
        'Under delningsikonen ligger Hämta GPX till kartplotter. Filen '
        'innehåller dina egna punkter som waypoints, hela sjövägen som '
        'rutt med brytpunkterna runt land, och samma väg som spår.',
    'Både rute og spor er med, fordi der findes plottere, der kun '
        'læser det ene.':
        'Både rutt och spår är med, eftersom det finns plottrar som bara '
        'läser det ena.',
    'Samme sted kan du kopiere et delelink. Det åbner ruten hos den, '
        'du sender det til — også hvis de aldrig har brugt Sejlplan før.':
        'På samma ställe kan du kopiera en delningslänk. Den öppnar '
        'rutten hos den du skickar den till — även om de aldrig har '
        'använt Seglingsplan förut.',
    'Skippervurdering':
        'Skepparbedömning',
    'En erfaren sejlkonsulent læser planen igennem.':
        'En erfaren seglingskonsult läser igenom planen.',
    'Vurderingen gennemgår ruten ben for ben og kommenterer det, '
        'tallene ikke siger: hvornår du bør reve, hvad der er værd at '
        'holde øje med, og om afgangen er den rigtige.':
        'Bedömningen går igenom rutten etapp för etapp och '
        'kommenterar det siffrorna inte säger: när du bör reva, vad som '
        'är värt att hålla ögonen på, och om avgången är den rätta.',
    'Den skrives af en sprogmodel ud fra din plan. Den er god til at '
        'få øje på det, der ikke hænger sammen — men den erstatter ikke '
        'din egen vurdering.':
        'Den skrivs av en språkmodell utifrån din plan. Den är bra på att '
        'få syn på det som inte hänger ihop — men den ersätter inte din '
        'egen bedömning.',
    'Sejlplan er et planlægningsværktøj. Prognoser er prognoser, og '
        'en landmaske er ikke et søkort. Planen erstatter ikke søkort, '
        'farvandsudsigt, efterretninger for søfarende eller almindelig '
        'sømandskab. Ansvaret for sejladsen er skipperens.':
        'Seglingsplan är ett planeringsverktyg. Prognoser är prognoser, '
        'och en landmask är inget sjökort. Planen ersätter inte sjökort, '
        'sjöväderrapport, underrättelser för sjöfarande eller vanligt '
        'sjömanskap. Ansvaret för seglingen är skepparens.',
    'Hvem er der lige nu':
        'Vilka är här just nu',
    'Listen over både, delt op efter havn. Nemmere end kortet.':
        'Listan över båtar, delad efter hamn. Enklare än kartan.',
    'Kortet er godt til at vise, hvor nogen er. Det er dårligt til at '
        'svare på, hvem der overhovedet er der: en båd er en lille '
        'trekant, og zoomer man ud så hele farvandet er med, kan man ikke '
        'se dem.':
        'Kartan är bra på att visa var någon är. Den är dålig på att '
        'svara på vilka som överhuvudtaget är där: en båt är en liten '
        'triangel, och zoomar man ut så att hela farvattnet är med kan '
        'man inte se dem.',
    'Tryk "Se hvem der er i nærheden". De både, der ligger i en havn, '
        'står under havnens navn — for det er dét, man vil vide, når man '
        'leder efter nogen at drikke kaffe med. Resten står under '
        'Undervejs med afstand og pejling.':
        'Tryck på ”Se vilka som är i närheten”. De båtar som ligger i en '
        'hamn står under hamnens namn — för det är det man vill veta när '
        'man letar efter någon att dricka kaffe med. Resten står under '
        'Till sjöss med avstånd och bäring.',
    'Havnene på ruten får også et mærke, når der ligger nogen: "3 '
        'både her". Tryk på det, og du er i listen.':
        'Hamnarna på rutten får också ett märke när det ligger någon där: '
        '”3 båtar här”. Tryck på det, så är du i listan.',
    'Tryk på en båd for at skrive til den. Du ser kun både, der også '
        'har gjort sig synlige — den regel gælder her som alle andre '
        'steder.':
        'Tryck på en båt för att skriva till den. Du ser bara båtar som '
        'också har gjort sig synliga — den regeln gäller här som överallt '
        'annars.',
    'Mørketimerne tælles efter solen, ikke efter uret: hvornår den '
        'faktisk går ned dér, hvor du er. I juni er der halvanden times '
        'forskel på solnedgang i Gedser og i Skagen, og det er dét, der '
        'afgør, om der skal føres lanterner.':
        'Mörkertimmarna räknas efter solen, inte efter klockan: när den '
        'faktiskt går ner där du är. I juni är det en och en halv timmes '
        'skillnad på solnedgången i Gedser och i Skagen, och det är det '
        'som avgör om lanternor ska föras.',
    'Bølgeperioden vejes med. To søer på halvanden meter er ikke det '
        'samme: fem sekunder mellem toppene er en stejl, brydende vindsø, '
        'ni sekunder er en dønning, man sover i.':
        'Vågperioden vägs med. Två sjöar på en och en halv meter är inte '
        'samma sak: fem sekunder mellan topparna är en brant, brytande '
        'vindsjö, nio sekunder är en dyning man sover i.',
}
