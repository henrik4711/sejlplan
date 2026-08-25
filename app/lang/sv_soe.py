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
    'Sådan læses en fyrkarakter':
        'Så läser man en fyrkaraktär',
    'Lanterner om natten':
        'Lanternor på natten',
    'Dagsignaler':
        'Dagsignaler',
    'Lydsignaler når I ser hinanden':
        'Ljudsignaler när ni ser varandra',
    'Lydsignaler i nedsat sigtbarhed':
        'Ljudsignaler vid nedsatt sikt',
    'Nødsignaler':
        'Nödsignaler',
    'Sømærker og signaler':
        'Sjömärken och signaler',
    'Afmærkningen er IALA A — Danmark, Tyskland, Sverige, Norge og '
        'resten af Europa.':
        'Utmärkningen är IALA A — Danmark, Tyskland, Sverige, Norge och '
        'resten av Europa.',
    'En huskeseddel, ikke Søvejsreglerne. Er du i tvivl om en '
        'vigepligt, er det reglerne, der gælder. Og farerne står i '
        'søkortet — dem kender Sejlplan ikke.':
        'En minneslapp, inte sjövägsreglerna. Är du osäker på en '
        'väjningsplikt är det reglerna som gäller. Och farorna står i '
        'sjökortet — dem känner Seglingsplan inte.',
    'Hvad betyder det':
        'Vad betyder det',
    'Sømærker, fyrkarakterer, lanterner og signaler':
        'Sjömärken, fyrkaraktärer, lanternor och signaler',
    'Kig efter':
        'Titta efter',
    'Rebning':
        'Revning',
    'Ved {kn} knob på {sejlføring}. Et udgangspunkt — dine sejl og '
        'deres alder bestemmer resten.':
        'Vid {kn} knop på {sejlføring}. En utgångspunkt — dina segel och '
        'deras ålder bestämmer resten.',
    'Optimér mine sejl':
        'Trimma mina segel',
    'Til søs':
        'Till sjöss',
    'Hvad mærkerne i vandet betyder, og hvad du gør ved dem.':
        'Vad märkena i vattnet betyder, och vad du gör med dem.',
    'Afmærkningen er IALA A. Den gælder i Danmark, Tyskland, Sverige, '
        'Norge og resten af Europa. I Nord- og Sydamerika er de røde og '
        'grønne sidemærker byttet om.':
        'Utmärkningen är IALA A. Den gäller i Danmark, Tyskland, Sverige, '
        'Norge och i resten av Europa. I Nord- och Sydamerika är de röda '
        'och gröna lateralmärkena omkastade.',
    'Sidemærkerne siger, hvor løbet er: rødt og dåseformet i bagbord, '
        'grønt og spidst i styrbord, når du sejler ind. Ud igen er det '
        'omvendt.':
        'Lateralmärkena säger var farleden är: rött och cylindriskt om '
        'babord, grönt och spetsigt om styrbord, när du går in. Ut igen '
        'är det tvärtom.',
    'Kardinalmærkerne siger, hvilken side du skal gå på. Keglerne '
        'øverst peger hen mod den side, der er ren: to kegler opad er et '
        'nordmærke, og så skal du nord om. Antallet af blink følger uret '
        '— tre for øst, seks for syd, ni for vest.':
        'Kardinalmärkena säger vilken sida du ska gå på. Konerna överst '
        'pekar mot den sida som är fri: två koner uppåt är ett nordmärke, '
        'och då ska du gå norr om. Antalet blixtar följer klockan — tre '
        'för ost, sex för syd, nio för väst.',
    'Enkeltstående fare er sort med røde bånd og to kugler. Der er '
        'vand hele vejen rundt, men gå ikke tæt på. Sikkert vand er '
        'rød-hvidt stribet med en rød kugle — dér er der vand hele vejen '
        'rundt.':
        'Punktmärket är svart med röda band och två klot. Det är vatten '
        'runt om, men gå inte nära. Mittledsmärket är rödvitrandigt med '
        'ett rött klot — där är det vatten runt om.',
    'Under bogikonet i toppen ligger tegningerne af dem alle sammen, '
        'med fyrkarakter og huskeregel.':
        'Under bokikonen högst upp ligger teckningarna av dem allihop, '
        'med fyrkaraktär och minnesregel.',
    'Fyr og karakterer':
        'Fyrar och karaktärer',
    'Sådan læser du Fl(3)WR.10s — og hvad et sektorfyr fortæller.':
        'Så läser du Fl(3)WR.10s — och vad en sektorfyr säger dig.',
    'Bogstaverne siger, hvordan lyset opfører sig: Fl er blink, Oc er '
        'formørkelse, Iso er lige lang tid tændt og slukket, Q er '
        'hurtigblink. Tallet i parentes er antal blink i gruppen, og '
        'sekundtallet er hele periodens længde.':
        'Bokstäverna säger hur ljuset beter sig: Fl är blixt, Oc är '
        'avbrott, Iso är lika länge tänt och släckt, Q är snabblixt. '
        'Siffran i parentes är antalet blixtar i gruppen, och sekundtalet '
        'är hela periodens längd.',
    'Fl(3)WR.10s er altså tre blink, hvidt i én retning og rødt i en '
        'anden, gentaget hvert tiende sekund. Tag tid på perioden med et '
        'ur — det er dét, der skiller to fyr, der ellers ligner hinanden.':
        'Fl(3)WR.10s är alltså tre blixtar, vitt åt ett håll och rött åt '
        'ett annat, upprepat var tionde sekund. Ta tid på perioden med en '
        'klocka — det är det som skiljer två fyrar som annars liknar '
        'varandra.',
    'Et sektorfyr viser forskellig farve i forskellige retninger. '
        'Hvidt betyder som regel det rene løb. Hvilken side rødt og grønt '
        'dækker, står i søkortet — det er ikke det samme alle steder.':
        'En sektorfyr visar olika färg åt olika håll. Vitt betyder i '
        'regel den fria farleden. Vilken sida rött och grönt täcker står '
        'i sjökortet — det är inte likadant överallt.',
    'Lanterner og dagsignaler':
        'Lanternor och dagsignaler',
    'Hvad du ser om natten, og hvad det siger om, hvem der viger.':
        'Vad du ser på natten, och vad det säger om vem som väjer.',
    'Ser du både rødt og grønt uden hvidt over, er det en sejlbåd, '
        'der kommer lige imod dig. Er der ét hvidt lys over, er det et '
        'motorfartøj. Ser du kun hvidt, ser du den bagfra — og så er det '
        'dig, der indhenter og skal holde klar.':
        'Ser du både rött och grönt utan vitt över är det en segelbåt som '
        'kommer rakt emot dig. Finns ett vitt ljus över är det ett '
        'maskindrivet fartyg. Ser du bara vitt ser du det bakifrån — och '
        'då är det du som hinner ikapp och ska hålla undan.',
    'To røde over hinanden betyder, at fartøjet ikke er under '
        'kommando. Rød-hvid-rød betyder, at det er begrænset i sin evne '
        'til at manøvrere. Begge dele betyder: hold godt klar.':
        'Två röda över varandra betyder att fartyget är manöverodugligt. '
        'Rött-vitt-rött betyder begränsad manöverförmåga. Bådadera '
        'betyder: håll ordentligt undan.',
    'Om dagen: en sort kugle er for anker. En sort kegle med spidsen '
        'nedad er en sejlbåd, der også har motoren i gang — og så gælder '
        'reglerne for motorfartøjer. Den kegle glemmer næsten alle, og '
        'den ændrer, hvem der viger.':
        'På dagen: ett svart klot betyder för ankar. En svart kon med '
        'spetsen nedåt är en segelbåt som också har motorn igång — och då '
        'gäller reglerna för maskindrivna fartyg. Den konen glömmer '
        'nästan alla, och den ändrar vem som väjer.',
    'Lyd- og nødsignaler':
        'Ljud- och nödsignaler',
    'Ét kort er styrbord, fem korte er en advarsel.':
        'En kort stöt är styrbord, fem korta är en varning.',
    'Når I kan se hinanden: ét kort stød betyder "jeg drejer til '
        'styrbord", to korte "til bagbord", tre korte "jeg bakker". Fem '
        'korte eller flere er advarslen — jeg forstår dig ikke, eller du '
        'gør ikke nok for at holde klar.':
        'När ni ser varandra: en kort stöt betyder ”jag girar styrbord”, '
        'två korta ”babord”, tre korta ”jag backar”. Fem korta eller fler '
        'är varningen — jag förstår dig inte, eller du gör inte nog för '
        'att hålla undan.',
    'I tåge lyder det hvert andet minut: ét langt fra et motorfartøj '
        'med fart i, to lange fra et, der ligger stille, og ét langt plus '
        'to korte fra en sejlbåd — og fra en fisker og en manøvrehæmmet. '
        'Så du ved ikke hvilken, kun at du skal holde klar.':
        'I dimma låter det varannan minut: en lång från ett maskindrivet '
        'fartyg med fart, två långa från ett som ligger stilla, och en '
        'lång plus två korta från en segelbåt — och från en fiskare och '
        'en manöverbegränsad. Du vet alltså inte vilket, bara att du ska '
        'hålla undan.',
    'I nød: MAYDAY på kanal 16 eller DSC-nødknappen. 112 går videre '
        'til JRCC og virker, så længe du har mobildækning. Røde blus er '
        'nød; et hvidt blus er en advarsel og noget helt andet.':
        'I nöd: MAYDAY på kanal 16 eller DSC-nödknappen. I Sverige går '
        '112 vidare till JRCC Göteborg så länge du har mobiltäckning. '
        'Röda ljus är nöd; en vit fackla är en varning och något helt '
        'annat.',
    'Hvorfor vi ikke advarer om grunde':
        'Varför vi inte varnar för grund',
    'Sejlplan kender land og vand — ikke dybder. Farerne står i '
        'søkortet.':
        'Seglingsplan känner land och vatten — inte djup. Farorna står i '
        'sjökortet.',
    'Ruten lægges uden om land med en maske over de skandinaviske '
        'farvande. Masken kender kysten. Den kender ikke dybder, grunde, '
        'rev, sten, spærrede områder, skydeområder eller sejlrender.':
        'Rutten läggs runt land med en mask över de skandinaviska '
        'farvattnen. Masken känner kusten. Den känner inte djup, grund, '
        'rev, stenar, skjutfält, spärrområden eller farleder.',
    'Vi kunne godt skrive "pas på grunden her" ud fra et gæt. Vi '
        'lader være. En advarsel, der ser rigtig ud og er forkert, er '
        'farligere end ingen advarsel — for så holder man op med at kigge '
        'i søkortet.':
        'Vi kunde skriva ”akta grundet här” utifrån en gissning. Vi låter '
        'bli. En varning som ser rätt ut och är fel är farligare än ingen '
        'varning — då slutar man nämligen titta i sjökortet.',
    'Farerne står i søkortet og i Efterretninger for Søfarende. Læg '
        'ruten her, og gå den efter dér. Særligt i smalt farvand, tæt på '
        'kysten og omkring pynter og rev.':
        'Farorna står i sjökortet och i Underrättelser för sjöfarande. '
        'Lägg rutten här, och gå igenom den där. Särskilt i trångt '
        'farvatten, nära land och runt uddar och rev.',
    'Bagbords sidemærke':
        'Babords lateralmärke',
    'Rød, dåseformet. Står i bagbords side af løbet, når du sejler '
        'ind — mod havn, op ad et løb, eller den vej afmærkningsretningen '
        'går på søkortet.':
        'Rött, cylindriskt. Står på babords sida av farleden när du går in — '
        'mot hamn, uppför en led, eller åt det håll utmärkningsriktningen '
        'går i sjökortet.',
    'Hold det i bagbord, når du går ind. Ud igen: i styrbord.':
        'Håll det om babord när du går in. Ut igen: om styrbord.',
    'Rødt. Enhver karakter.':
        'Rött. Vilken karaktär som helst.',
    'Rødt i bagbord, når du går ind. I Amerika er det omvendt — dér '
        'gælder IALA B.':
        'Rött om babord när du går in. I Amerika är det tvärtom — där '
        'gäller IALA B.',
    'Styrbords sidemærke':
        'Styrbords lateralmärke',
    'Grøn, spids som en kegle. Står i styrbords side af løbet, når du '
        'sejler ind.':
        'Grönt, spetsigt som en kon. Står på styrbords sida av farleden '
        'när du går in.',
    'Hold det i styrbord, når du går ind. Ud igen: i bagbord.':
        'Håll det om styrbord när du går in. Ut igen: om babord.',
    'Grønt. Enhver karakter.':
        'Grönt. Vilken karaktär som helst.',
    'Nordmærke':
        'Nordmärke',
    'Sort øverst, gul nederst. To kegler med spidserne opad — de '
        'peger op mod det sorte.':
        'Svart överst, gult nederst. Två koner med spetsarna uppåt — de '
        'pekar upp mot det svarta.',
    'Passér nord for mærket. Farvandet syd for det er ikke sikkert.':
        'Passera norr om märket. Farvattnet söder om det är inte säkert.',
    'Hvidt, uafbrudt hurtigblink: Q eller VQ.':
        'Vitt, oavbruten snabblixt: Q eller VQ.',
    'Keglerne peger hen mod den side, du skal gå.':
        'Konerna pekar mot den sida du ska gå.',
    'Østmærke':
        'Ostmärke',
    'Sort, gult bånd, sort. To kegler bund mod bund.':
        'Svart, gult band, svart. Två koner bas mot bas.',
    'Passér øst for mærket.':
        'Passera öster om märket.',
    'Hvidt: Q(3) 10s eller VQ(3) 5s.':
        'Vitt: Q(3) 10s eller VQ(3) 5s.',
    'Tre blink som klokken tre — øst.':
        'Tre blixtar som klockan tre — ost.',
    'Sydmærke':
        'Sydmärke',
    'Gul øverst, sort nederst. To kegler med spidserne nedad.':
        'Gult överst, svart nederst. Två koner med spetsarna nedåt.',
    'Passér syd for mærket.':
        'Passera söder om märket.',
    'Hvidt: Q(6) + langt blink 15s, eller VQ(6) + langt blink 10s.':
        'Vitt: Q(6) + lång blixt 15s, eller VQ(6) + lång blixt 10s.',
    'Seks blink som klokken seks — syd. Det lange blink er der, så du '
        'ikke kommer i tvivl om, hvor gruppen slutter.':
        'Sex blixtar som klockan sex — syd. Den långa blixten finns där '
        'för att du inte ska bli osäker på var gruppen slutar.',
    'Vestmærke':
        'Västmärke',
    'Gul, sort bånd, gul. To kegler spids mod spids — som et '
        'timeglas.':
        'Gult, svart band, gult. Två koner spets mot spets — som ett '
        'timglas.',
    'Passér vest for mærket.':
        'Passera väster om märket.',
    'Hvidt: Q(9) 15s eller VQ(9) 10s.':
        'Vitt: Q(9) 15s eller VQ(9) 10s.',
    'Ni blink som klokken ni — vest.':
        'Nio blixtar som klockan nio — väst.',
    'Enkeltstående fare':
        'Punktmärke',
    'Sort med et eller flere brede røde bånd. To sorte kugler over '
        'hinanden.':
        'Svart med ett eller flera breda röda band. Två svarta klot över '
        'varandra.',
    'Der er farbart vand hele vejen rundt, men faren ligger lige dér. '
        'Gå udenom med god margen.':
        'Det är farbart vatten runt om, men faran ligger precis där. Gå '
        'utanför med god marginal.',
    'Hvidt: to blink, Fl(2) 5s.':
        'Vitt: två blixtar, Fl(2) 5s.',
    'Sikkert vand':
        'Mittledsmärke',
    'Røde og hvide lodrette striber. Én rød kugle.':
        'Röda och vita lodräta ränder. Ett rött klot.',
    'Der er vand hele vejen rundt. Bruges midt i et løb og som '
        'landfaldsbøje — dén, man styrer efter, når man kommer ind fra '
        'søen.':
        'Det är vatten runt om. Används mitt i en farled och som '
        'angöringsboj — den man styr på när man kommer in från sjön.',
    'Hvidt: Iso, Oc, langt blink hvert 10. sekund, eller morse A.':
        'Vitt: Iso, Oc, lång blixt var tionde sekund, eller morse A.',
    'Særligt mærke':
        'Specialmärke',
    'Gult, med et liggende gult kryds.':
        'Gult, med ett liggande gult kryss.',
    'Markerer noget andet end sejladsen: kabler, rørledninger, '
        'badeområder, opdræt, kapsejladsbaner. Slå op i søkortet, hvad '
        'det er, før du sejler henover.':
        'Markerar något annat än seglingen: kablar, rörledningar, '
        'badområden, odlingar, kappseglingsbanor. Slå upp i sjökortet vad '
        'det är innan du seglar över.',
    'Gult.':
        'Gult.',
    'Ny fare':
        'Ny fara',
    'Blå og gule lodrette striber. Stående gult kryds.':
        'Blå och gula lodräta ränder. Stående gult kryss.',
    'Et vrag eller en fare, der lige er opstået, og som endnu ikke '
        'står i søkortet. Hold godt klar.':
        'Ett vrak eller en fara som just har uppstått och som ännu inte '
        'står i sjökortet. Håll ordentligt undan.',
    'Skiftevis blåt og gult, ét sekund hver.':
        'Omväxlande blått och gult, en sekund vardera.',
    'Blink — lyset er kortere end mørket.':
        'Blixt — ljuset är kortare än mörkret.',
    'Langt blink — mindst to sekunder.':
        'Lång blixt — minst två sekunder.',
    'Formørkelse — lyset er længere end mørket.':
        'Avbrott — ljuset är längre än mörkret.',
    'Lige lang tid tændt og slukket.':
        'Lika länge tänt och släckt.',
    'Hurtigblink, omkring 50–60 i minuttet.':
        'Snabblixt, omkring 50–60 i minuten.',
    'Meget hurtigt blink, omkring 100–120 i minuttet.':
        'Mycket snabb blixt, omkring 100–120 i minuten.',
    'Fast lys, der ikke blinker.':
        'Fast sken som inte blinkar.',
    'Morse A: kort-langt. Bruges på landfaldsbøjer.':
        'Morse A: kort-lång. Används på angöringsbojar.',
    'Tallet i parentes er antal blink i gruppen.':
        'Siffran i parentes är antalet blixtar i gruppen.',
    'Sekundtallet er hele periodens længde — tag tid på den.':
        'Sekundtalet är hela periodens längd — ta tid på den.',
    'Farven: hvid, rød, grøn.':
        'Färgen: vit, röd, grön.',
    'Tre blink, hvidt i én retning og rødt i en anden, og det hele '
        'gentager sig hvert tiende sekund.':
        'Tre blixtar, vitt åt ett håll och rött åt ett annat, och '
        'alltihop upprepas var tionde sekund.',
    'Et sektorfyr viser forskellig farve i forskellige retninger. '
        'Hvidt betyder som regel, at du er i det rene løb; rødt og grønt, '
        'at du er ude af det til hver sin side. Hvilken side hvad er, '
        'står i søkortet — det er ikke det samme alle steder.':
        'En sektorfyr visar olika färg åt olika håll. Vitt betyder i '
        'regel att du är i den rena farleden; rött och grönt att du är '
        'ute ur den åt var sitt håll. Vilken sida som är vad står i '
        'sjökortet — det är inte likadant överallt.',
    'Rød og grøn side om side, ingen hvid over':
        'Rött och grönt bredvid varandra, inget vitt över',
    'En sejlbåd for sejl, der kommer lige imod dig.':
        'En segelbåt för segel som kommer rakt emot dig.',
    'Rød og grøn med ét hvidt lys over':
        'Rött och grönt med ett vitt ljus över',
    'Et motorfartøj, der kommer lige imod dig.':
        'Ett maskindrivet fartyg som kommer rakt emot dig.',
    'Rød og grøn med to hvide over hinanden':
        'Rött och grönt med två vita över varandra',
    'Et motorfartøj over 50 meter — og det bagerste hvide lys er '
        'højest. Står de to hvide lodret over hinanden, kommer det lige '
        'imod dig.':
        'Ett maskindrivet fartyg över 50 meter — och det aktre vita '
        'ljuset står högre. Står de två vita lodrätt över varandra kommer '
        'det rakt emot dig.',
    'Kun grønt':
        'Bara grönt',
    'Du ser dens styrbords side. Den går fra bagbord mod styrbord '
        'foran dig.':
        'Du ser dess styrbordssida. Den går från babord mot styrbord '
        'framför dig.',
    'Kun rødt':
        'Bara rött',
    'Du ser dens bagbords side. Som udgangspunkt er det dig, der '
        'viger — men se på pejlingen, ikke på farven alene.':
        'Du ser dess babordssida. Som utgångspunkt är det du som väjer — '
        'men se på bäringen, inte bara på färgen.',
    'Kun hvidt agter':
        'Bara vitt akterut',
    'Du ser den bagfra. Du indhenter den, og så er det dig, der '
        'holder klar.':
        'Du ser den bakifrån. Du hinner ikapp, och då är det du som ska '
        'hålla undan.',
    'Ét hvidt rundtlysende, ingen andet':
        'Ett vitt runtlysande, inget annat',
    'Et fartøj for anker — eller en lille båd under 7 meter.':
        'Ett fartyg för ankar — eller en liten båt under 7 meter.',
    'To røde over hinanden, rundtlysende':
        'Två röda runtlysande över varandra',
    'Ikke under kommando. Den kan ikke styre. Hold klar.':
        'Manöveroduglig. Den kan inte styra. Håll undan.',
    'Rød–hvid–rød lodret':
        'Rött–vitt–rött lodrätt',
    'Begrænset i sin evne til at manøvrere. Uddybning, bugsering, '
        'dykkerarbejde. Hold godt klar.':
        'Begränsad manöverförmåga. Muddring, bogsering, dykarbete. Håll '
        'ordentligt undan.',
    'Grønt over hvidt':
        'Grönt över vitt',
    'Trawler. Der kan gå wire langt agterud.':
        'Trålare. Det kan gå wire långt akterut.',
    'En sort kugle':
        'Ett svart klot',
    'For anker.':
        'För ankar.',
    'En sort kegle med spidsen nedad':
        'En svart kon med spetsen nedåt',
    'En sejlbåd, der også har motoren i gang. Så gælder reglerne for '
        'motorfartøjer, ikke for sejlbåde — og det er dét, folk glemmer.':
        'En segelbåt som också har motorn igång. Då gäller reglerna för '
        'maskindrivna fartyg, inte de för segelbåtar — och det är det '
        'folk glömmer.',
    'To sorte kugler over hinanden':
        'Två svarta klot över varandra',
    'Ikke under kommando.':
        'Manöveroduglig.',
    'Kugle – rombe – kugle':
        'Klot – romb – klot',
    'Begrænset i sin evne til at manøvrere.':
        'Begränsad manöverförmåga.',
    'En sort cylinder':
        'En svart cylinder',
    'Begrænset af sin dybgang.':
        'Begränsad av sitt djupgående.',
    'Tre sorte kugler over hinanden':
        'Tre svarta klot över varandra',
    'Fartøjet står på grund.':
        'Fartyget står på grund.',
    'Ét kort stød':
        'En kort stöt',
    'Jeg drejer til styrbord.':
        'Jag girar styrbord.',
    'To korte stød':
        'Två korta stötar',
    'Jeg drejer til bagbord.':
        'Jag girar babord.',
    'Tre korte stød':
        'Tre korta stötar',
    'Jeg bakker.':
        'Jag backar.',
    'Fem korte stød eller flere':
        'Fem korta stötar eller fler',
    'Jeg forstår ikke, hvad du har tænkt dig — eller: du gør ikke nok '
        'for at holde klar. Det er advarslen.':
        'Jag förstår inte vad du tänker göra — eller: du gör inte nog för '
        'att hålla undan. Det är varningen.',
    'Ét langt stød':
        'En lång stöt',
    'Jeg nærmer mig et sving eller et sted, hvor jeg ikke kan se, '
        'hvad der kommer.':
        'Jag närmar mig en krök eller en plats där jag inte kan se vad '
        'som kommer.',
    'Ét langt hvert andet minut':
        'En lång varannan minut',
    'Motorfartøj med fart gennem vandet.':
        'Maskindrivet fartyg med fart genom vattnet.',
    'To lange hvert andet minut':
        'Två långa varannan minut',
    'Motorfartøj, der ligger stille i vandet.':
        'Maskindrivet fartyg som ligger stilla i vattnet.',
    'Ét langt og to korte hvert andet minut':
        'En lång och två korta varannan minut',
    'Sejlbåd for sejl. Det samme lyder fra en fisker, en bugserende '
        'og en manøvrehæmmet — så du ved ikke hvilken, kun at du skal '
        'holde klar.':
        'Segelbåt för segel. Detsamma låter från en fiskare, en '
        'bogserande och en manöverbegränsad — du vet alltså inte vilket, '
        'bara att du ska hålla undan.',
    'Klokke i fem sekunder hvert minut':
        'Klocka i fem sekunder varje minut',
    'Fartøj for anker. Er det over 100 meter, kommer der en gongong '
        'agter bagefter.':
        'Fartyg för ankar. Är det över 100 meter följer en gonggong '
        'akterut.',
    'VHF kanal 16 — MAYDAY':
        'VHF kanal 16 — MAYDAY',
    'Sig MAYDAY tre gange, bådens navn, position, hvad der er sket, '
        'og hvor mange I er. DSC-nødknappen sender position og '
        'kaldesignal af sig selv.':
        'Säg MAYDAY tre gånger, båtens namn, position, vad som har hänt '
        'och hur många ni är. DSC-nödknappen skickar position och '
        'anropssignal av sig själv.',
    '112':
        '112',
    'Går videre til JRCC. Virker, når du har mobildækning, og det har '
        'man tit tættere på land end man tror.':
        'Går vidare till JRCC. Fungerar så länge du har mobiltäckning, '
        'och det har man ofta närmare land än man tror.',
    'Rødt faldskærmsblus eller rødt håndblus':
        'Röd fallskärmsraket eller rött handbloss',
    'Nød. Et hvidt blus er derimod en advarsel — ikke det samme.':
        'Nöd. En vit fackla är däremot en varning — inte samma sak.',
    'Orange røgsignal':
        'Orange röksignal',
    'Nød, om dagen. Ses langt i klart vejr.':
        'Nöd, på dagen. Syns långt i klart väder.',
    'Langsomme bevægelser op og ned med begge arme':
        'Långsamma rörelser upp och ner med båda armarna',
    'Nød. Det er det signal, man kan give uden udstyr.':
        'Nöd. Det är den signal man kan ge utan utrustning.',
    'Orange dug med sort firkant og cirkel':
        'Orange duk med svart fyrkant och cirkel',
    'Nød, set fra luften. Læg den, så et fly kan se den.':
        'Nöd, sett från luften. Lägg den så att ett flygplan kan se den.',
    'Vend, når vindpejlingen til målet er lige så stor til den anden '
        'side. Så sejler du ikke længere end nødvendigt.':
        'Slå när vindbäringen till målet är lika stor åt andra hållet. Då '
        'seglar du inte längre än nödvändigt.',
    'Fuldt sejl.':
        'Fulla segel.',
    'Bommen':
        'Bommen',
    'Kursen ligger tættere på vinden, end båden kan sejle. Strækket '
        'skal krydses — læg dig på den halse, der bringer dig nærmest '
        'målet, og trim som til bidevind.':
        'Kursen ligger närmare vinden än båten kan segla. Sträckan måste '
        'kryssas — lägg dig på den halsen som för dig närmast målet, och '
        'trimma som för bidevind.',
    'Overvej første reb, hvis båden lægger sig mere end tyve grader, '
        'eller hvis der er tryk i roret.':
        'Överväg första revet om båten lägger sig mer än tjugo grader, '
        'eller om det är tryck i rodret.',
    'Første reb. Det koster ikke fart — en overtrimmet båd krænger og '
        'skrider sidelæns.':
        'Första revet. Det kostar ingen fart — en övertrimmad båt kränger '
        'och glider i sidled.',
    'Andet reb og rullet genua. Kommer det over tredive knob, er det '
        'tredje reb eller en stormfok — og så er spørgsmålet, om turen '
        'skal sejles i dag.':
        'Andra revet och inrullad genua. Kommer det över trettio knop är '
        'det tredje revet eller en stormfock — och då är frågan om resan '
        'ska seglas i dag.',
    'Telltalerne på forsejlet skal strømme bagud på begge sider. '
        'Lifter de i luv, så fald af eller stram skødet. Øverste sejlpind '
        'i storsejlet omtrent parallel med bommen.':
        'Telltalesen på förseglet ska strömma akterut på båda sidor. '
        'Lyfter de i lovart, fall av eller skota hem. Översta lattan i '
        'storseglet ungefär parallell med bommen.',
    'Omtrent på midterlinjen. Kig op ad bommen — den skal pege lige '
        'agterud eller en anelse i læ.':
        'Ungefär på mittlinjen. Titta längs bommen — den ska peka rakt '
        'akterut eller en aning i lä.',
    'Løjgangsvognen':
        'Travaren',
    'Lidt til luv for midten. Så kan skødet holde bommen inde uden at '
        'trække sejlet fladt.':
        'En bit till lovart om mitten. Då kan skotet hålla bommen inne '
        'utan att dra seglet platt.',
    'Storskødet':
        'Storskotet',
    'Løst nok til at agterliget hænger blødt. Et fladt sejl trækker '
        'ikke i let vind.':
        'Löst nog för att akterliket ska hänga mjukt. Ett platt segel '
        'drar inte i lätt vind.',
    'Bomnedhalet':
        'Kicktaljan',
    'Løst. På kryds er det skødet, der holder bommen nede — nedhalet '
        'skal først bruges, når du skøder ud.':
        'Löst. På kryss är det skotet som håller bommen nere — kicken ska '
        'först användas när du skotar ut.',
    'Udhalet':
        'Uthalet',
    'Løst, så der er dybde i underliget.':
        'Löst, så att det finns djup i underliket.',
    'Nedhalet':
        'Cunninghamen',
    'Helt løst. Rynker i forliget er i orden, når det blæser lidt.':
        'Helt löst. Veck i förliket går bra när det blåser lite.',
    'Agterstaget':
        'Akterstaget',
    'Løst.':
        'Löst.',
    'Forsejlet':
        'Förseglet',
    'Skødevognen frem, så sejlet får dybde forneden. Skød blødt — '
        'genuaen skal ikke røre saling eller vant.':
        'Skotvagnen fram, så att seglet får djup nedtill. Skota mjukt — '
        'genuan ska inte röra salning eller vant.',
    'Midtskibs.':
        'Midskepps.',
    'Stramt. Øverste sejlpind parallel med bommen — i byger må den '
        'gerne falde en smule af.':
        'Hårt. Översta lattan parallell med bommen — i byar får den gärna '
        'falla av en aning.',
    'Stramt. Fladt sejl, mindre krængning.':
        'Hårt. Platt segel, mindre krängning.',
    'Stram, til rynkerne langs masten lige forsvinder. Det flytter '
        'trykpunktet frem og flader sejlet.':
        'Sträck tills vecken längs masten precis försvinner. Det '
        'flyttar tryckpunkten framåt och plattar ut seglet.',
    'Skødevognen midt i sporet. Telltalerne skal lifte samtidig oppe '
        'og nede.':
        'Skotvagnen mitt i skenan. Telltalesen ska lyfta samtidigt uppe '
        'och nere.',
    'Til læ, indtil båden retter sig op. Det åbner toppen og lader '
        'trykket gå ud foroven i stedet for at lægge båden ned.':
        'Till lä tills båten reser sig. Det öppnar toppen och släpper ut '
        'trycket upptill i stället för att trycka ner båten.',
    'Stram. Masten bøjer, storsejlet flader ud, og forstaget bliver '
        'stivere — det er dét, der gør, at du kan holde højde.':
        'Hårt. Masten böjer sig, storseglet plattas ut, och förstaget '
        'blir styvare — och det är det som gör att du kan hålla höjd.',
    'Skødevognen agter. Toppen åbner, og båden retter sig op uden at '
        'du mister fart.':
        'Skotvagnen akterut. Toppen öppnar, och båten reser sig utan att '
        'du förlorar fart.',
    'Skød ud, til forkanten lige begynder at bagge, og stram så lidt '
        'til igen. Det er dér, sejlet trækker mest.':
        'Skota ut tills förliket precis börjar killa, och skota sedan hem '
        'en aning igen. Där drar seglet som mest.',
    'Ud til omkring tyve-tredive grader fra midterlinjen.':
        'Ut till omkring tjugo-trettio grader från mittlinjen.',
    'Til læ. Nu er det bomnedhalet, der styrer twisten — ikke vognen.':
        'Till lä. Nu är det kicktaljan som styr twisten — inte travaren.',
    'Skød ud, til forkanten lige begynder at bagge, og stram så lidt '
        'til.':
        'Skota ut tills förliket precis börjar killa, och skota sedan hem '
        'en aning.',
    'Stram nu. Uden det løfter bommen sig, toppen af sejlet falder '
        'af, og du mister det tryk, du troede du havde.':
        'Hårt nu. Utan den lyfter bommen sig, toppen av seglet faller av, '
        'och du förlorar det tryck du trodde du hade.',
    'Løsn en smule. Halvvind vil have dybde.':
        'Släpp efter en aning. Halvvind vill ha djup.',
    'Løsn, med mindre det blæser.':
        'Släpp efter, om det inte blåser.',
    'Løsn. Du skal ikke bruge højde her.':
        'Släpp efter. Höjd behöver du inte här.',
    'Skødevognen lidt frem og ud. Slæk skødet, til telltalerne '
        'strømmer på begge sider.':
        'Skotvagnen lite fram och ut. Släpp skotet tills telltalesen '
        'strömmar på båda sidor.',
    'Telltalen agter på storsejlet skal strømme. Krøller den ind bag '
        'sejlet, er der for meget twist — stram bomnedhalet.':
        'Telltalen akterut på storseglet ska strömma. Kröker den in bakom '
        'seglet är det för mycket twist — hårdare kicktalja.',
    'Fra her og ned mod læns er der risiko for en utilsigtet '
        'bomvending. Sæt bomholder.':
        'Härifrån och ner mot läns finns risk för en ofrivillig gipp. '
        'Sätt en preventerlina.',
    'Godt ud. Pas på, at den ikke ligger an mod vantet — det slider '
        'sejlet i stykker på en lang dag.':
        'Långt ut. Se upp så att den inte ligger an mot vantet — det '
        'nöter sönder seglet på en lång dag.',
    'Helt i læ.':
        'Helt i lä.',
    'Ud, til sejlet lige bagger i forkanten.':
        'Ut tills seglet precis backar i förkanten.',
    'Hårdt. Det er nu, det tjener sig ind.':
        'Hårt. Nu lönar den sig.',
    'Løst. Dybt sejl.':
        'Löst. Djupt segel.',
    'Skødevognen helt frem og ud. Bliver genuaen dækket af '
        'storsejlet, så tag den over på den anden side med en bom — eller '
        'sæt spiler eller gennaker, hvis I har hænder til det.':
        'Skotvagnen helt fram och ut. Täcks genuan av storseglet, ta den '
        'över på andra sidan med en bom — eller sätt spinnaker eller '
        'gennaker om ni har händer till det.',
    'Fuldt sejl. Hold øje med bygerne.':
        'Fulla segel. Håll koll på byarna.',
    'Første reb, hvis det er trættende at styre.':
        'Första revet, om det blir tröttsamt att styra.',
    'Hold øje med vindviseren og med bølgerne agterfra. Ruller båden, '
        'så luf en smule op — læns er ikke det hurtigste, og sjældent det '
        'roligste.':
        'Håll koll på vindvisaren och på vågorna akterifrån. Rullar '
        'båten, lova upp en aning — läns är inte det snabbaste och sällan '
        'det lugnaste.',
    'Sæt bomholder, før du falder af. En utilsigtet bomvending på '
        'læns er dét, der slår folk ned og river rigge ned — og den '
        'kommer, når nogen kigger et andet sted hen.':
        'Sätt preventerlinan innan du faller av. En ofrivillig gipp på '
        'läns är det som slår ner folk och river ner riggar — och den '
        'kommer när någon tittar åt ett annat håll.',
    'Helt ud.':
        'Helt ut.',
    'Ude. Det er nedhalet og bomholderen, der holder bommen.':
        'Ute. Det är kicktaljan och preventerlinan som håller bommen.',
    'Hårdt.':
        'Hårt.',
    'Bom genuaen ud på modsat side af storsejlet, eller sæt spiler. '
        'Uden det står den og klapper i storsejlets læ og gør ingen '
        'nytte.':
        'Boma ut genuan på motsatt sida av storseglet, eller sätt '
        'spinnaker. Utan det står den och slår i storseglets lä och gör '
        'ingen nytta.',
    'Sejltrim':
        'Segeltrimm',
    'Sådan står sejlene på hver sejlstilling ved omkring {kn} knob. I '
        'sejlplanen står det samme for den vind, du faktisk får på hvert '
        'stræk.':
        'Så står seglen på varje kurs mot vinden vid omkring {kn} knop. I '
        'seglingsplanen står detsamma för den vind du faktiskt får på '
        'varje sträcka.',
    'Set oppefra, stævnen opad.':
        'Sett rakt uppifrån, fören uppåt.',
    'Den stiplede pil er vinden. Det gyldne er storsejlet, det grønne '
        'forsejlet.':
        'Den streckade pilen är vinden. Det gyllene är storseglet, det '
        'gröna förseglet.',
    'Bommen står omkring {grader}° fra midterlinjen.':
        'Bommen står omkring {grader}° från mittlinjen.',
}
