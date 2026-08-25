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
    'VHF':
        'VHF',
    'Når det ikke er MAYDAY':
        'När det inte är MAYDAY',
    'DSC — den røde knap':
        'DSC — den röda knappen',
    'Kanaler':
        'Kanaler',
    'Et almindeligt opkald':
        'Ett vanligt anrop',
    'Nødopkald — læs ovenfra og ned':
        'Nödanrop — läs uppifrån och ner',
    'Udtryk':
        'Uttryck',
    'Sådan bruger du trimrådet':
        'Så använder du trimrådet',
    'Under hvert stræk i sejlplanen, og i opslagsværket på kortet.':
        'Under varje sträcka i seglingsplanen, och i uppslagsverket på '
        'kartan.',
    'Planen kender vindens vinkel ind på båden og hvor hårdt det '
        'blæser på hvert stræk. Det er nok til et rigtigt råd, og det '
        'ligger foldet sammen under strækket: tryk "Optimér mine sejl". '
        'Øverst står sejlføringen tegnet oppefra, med bommen i den side, '
        'den faktisk skal stå i på det stræk.':
        'Planen känner vindens vinkel in mot båten och hur hårt det '
        'blåser på varje sträcka. Det räcker för ett riktigt råd, och det '
        'ligger hopfällt under sträckan: tryck på ”Trimma mina segel”. '
        'Överst står segelföringen tecknad uppifrån, med bommen på den '
        'sida där den faktiskt ska stå på den sträckan.',
    'Vil du slå op uden at have lagt en rute — hvordan står bommen nu '
        'igen for halvvind — så ligger de samme tegninger under '
        'bogikonet på kortet, én for hver sejlstilling.':
        'Vill du slå upp utan att ha lagt en rutt — hur stod bommen nu '
        'igen för halvvind — ligger samma teckningar under bokikonen på '
        'kartan, en för varje kurs mot vinden.',
    'Det er et udgangspunkt, ikke en facitliste. Sejlene er dine, og '
        'en tiårig dacronsæk vil noget andet end et nyt laminatsejl. '
        'Rådene er skrevet til en almindelig krydser med storsejl og '
        'rullegenua.':
        'Det är en utgångspunkt, inte ett facit. Seglen är dina, och en '
        'tio år gammal dacronsäck vill något annat än ett nytt '
        'laminatsegel. Råden är skrivna för en vanlig kryssare med '
        'storsegel och rullgenua.',
    'Hvad delene gør':
        'Vad delarna gör',
    'Syv liner, og hver af dem ændrer én ting ved sejlet.':
        'Sju linor, och var och en av dem ändrar en sak på seglet.',
    'Storskødet trækker bommen ind og ned på én gang. På kryds er det '
        'dét, der holder bommen nede — derfor skal bomnedhalet være løst '
        'der.':
        'Storskotet drar bommen inåt och nedåt på en gång. På kryss är '
        'det det som håller bommen nere — därför ska kicktaljan vara lös '
        'där.',
    'Løjgangsvognen flytter bommen sideværts, uden at ændre hvor '
        'hårdt sejlet er skødet ned. Det er dét, der lader dig lette '
        'trykket i en byge uden at åbne toppen af sejlet: kør vognen i læ '
        'i stedet for at slække skødet.':
        'Travaren flyttar bommen i sidled utan att ändra hur hårt seglet '
        'är skotat nedåt. Det är det som låter dig släppa trycket i en by '
        'utan att öppna toppen av seglet: kör travaren i lä i stället för '
        'att släppa på skotet.',
    'Bomnedhalet holder bommen nede, når skødet ikke længere kan — '
        'altså fra halvvind og ned. Uden det løfter bommen sig, toppen af '
        'sejlet falder af, og du mister det tryk, du troede du havde.':
        'Kicktaljan håller bommen nere när skotet inte längre kan — '
        'alltså från halvvind och neråt. Utan den lyfter bommen sig, '
        'toppen av seglet faller av, och du förlorar det tryck du trodde '
        'du hade.',
    'Udhalet strækker underliget. Stramt giver et fladt sejl forneden '
        'til meget vind; løst giver dybde til lidt vind.':
        'Uthalet sträcker underliket. Hårt ger ett platt segel nedtill '
        'till mycket vind; löst ger djup till lite vind.',
    'Nedhalet strammer forliget langs masten. Det flytter sejlets '
        'dybeste punkt fremad og flader sejlet. Stram det, når det '
        'blæser, og lad det være løst, når det ikke gør.':
        'Cunninghamen sträcker förliket längs masten. Det flyttar seglets '
        'djupaste punkt framåt och plattar ut seglet. Sträck det när det '
        'blåser, och låt det vara löst när det inte gör det.',
    'Agterstaget bøjer masten. Storsejlet flader ud, og forstaget '
        'bliver stivere — og et stift forstag er dét, der gør, at du kan '
        'holde højde i frisk vind.':
        'Akterstaget böjer masten. Storseglet plattas ut, och förstaget '
        'blir styvare — och ett styvt förstag är det som gör att du kan '
        'hålla höjd i frisk vind.',
    'Skødevognen på forsejlet bestemmer, om skødet trækker mest nedad '
        'eller mest bagud. Frem: dybde forneden og lukket top. Agter: '
        'fladt forneden og åben top.':
        'Skotvagnen på förseglet bestämmer om skotet drar mest nedåt '
        'eller mest bakåt. Fram: djup nedtill och sluten topp. Akter: '
        'platt nedtill och öppen topp.',
    'Twist — hvorfor toppen skal stå anderledes':
        'Twist — varför toppen ska stå annorlunda',
    'Vinden foroven er både stærkere og kommer fra en anden vinkel.':
        'Vinden upptill är både starkare och kommer från en annan vinkel.',
    'Vinden bremses af vandet, så den er svagere nede ved bommen end '
        'oppe i toppen af masten. Og fordi båden selv sejler, kommer den '
        'tilsyneladende vind ind i en anden vinkel foroven end forneden.':
        'Vinden bromsas av vattnet, så den är svagare nere vid bommen än '
        'uppe i masttoppen. Och eftersom båten själv seglar kommer den '
        'skenbara vinden in i en annan vinkel upptill än nedtill.',
    'Twist er den vridning, der lader toppen af sejlet stå i den '
        'vinkel, den faktisk får. Er der for lidt twist, står toppen for '
        'hårdt og lægger båden ned. Er der for meget, laver toppen '
        'ingenting.':
        'Twist är den vridning som låter toppen av seglet stå i den '
        'vinkel den faktiskt får. Är det för lite twist står toppen för '
        'hårt och trycker ner båten. Är det för mycket gör toppen '
        'ingenting.',
    'Du styrer det med skødet og bomnedhalet: strammere giver mindre '
        'twist. Kig på øverste sejlpind — den skal stå omtrent parallel '
        'med bommen. I byger må den gerne falde en smule af.':
        'Du styr det med skotet och kicktaljan: hårdare ger mindre twist. '
        'Titta på översta lattan — den ska stå ungefär parallellt med '
        'bommen. I byar får den gärna falla av en aning.',
    'Krængning og rortryk':
        'Krängning och rodertryck',
    'To ting båden fortæller dig, som er mere værd end noget '
        'instrument.':
        'Två saker båten berättar för dig, som är mer värda än något '
        'instrument.',
    'En almindelig krydser sejler bedst under omkring tyve graders '
        'krængning. Derover skrider den sidelæns i stedet for fremad, og '
        'du taber både fart og højde. Ligger den længere ned, er det ikke '
        'en stærk sejlads — det er for meget sejl.':
        'En vanlig kryssare seglar bäst under omkring tjugo graders '
        'krängning. Däröver glider den i sidled i stället för framåt, och '
        'du förlorar både fart och höjd. Ligger den längre ner är det '
        'ingen kraftfull segling — det är för mycket segel.',
    'Rortryk er det andet tegn. Skal du hele tiden holde imod for at '
        'undgå, at båden luffer op, er der for meget tryk agter i båden. '
        'Så er det storsejlet, der skal rebes — ikke forsejlet.':
        'Rodertryck är det andra tecknet. Måste du hela tiden hålla emot '
        'för att båten inte ska lova upp är det för mycket tryck akterut '
        'i båten. Då är det storseglet som ska revas — inte förseglet.',
    'Ruller man genuaen ind og lader storsejlet stå, bliver '
        'rortrykket værre, ikke bedre. Det er den fejl, de fleste gør '
        'først, fordi rullegenuaen er den nemmeste at tage af.':
        'Rullar man in genuan och låter storseglet stå blir rodertrycket '
        'värre, inte bättre. Det är det fel de flesta gör först, eftersom '
        'rullgenuan är den lättaste att ta ner.',
    'Bomholder på læns':
        'Preventerlina på läns',
    'Det ene sted, hvor trimmet ikke handler om fart.':
        'Det enda stället där trimmet inte handlar om fart.',
    'Fra rumskøds og ned mod læns kan bommen slå over af sig selv, '
        'hvis båden gribes af en bølge eller styrmanden falder for langt '
        'af. Det sker hurtigt, og bommen kommer i hovedhøjde.':
        'Från slör och ner mot läns kan bommen slå över av sig själv om '
        'båten grips av en våg eller rorsmannen faller av för långt. Det '
        'går fort, och bommen kommer i huvudhöjd.',
    'En bomholder er en line fra bommen og frem til dækket, der '
        'holder den ude. Sæt den, før du falder af — ikke bagefter. Det '
        'er dét, der gør en utilsigtet bomvending til en irritation i '
        'stedet for en ulykke.':
        'En preventerlina är en lina från bommen och fram till däck som '
        'håller den ute. Sätt den innan du faller av — inte efteråt. Det '
        'är det som gör en ofrivillig gipp till en irritation i stället '
        'för en olycka.',
    'Husk at tage den af igen, før du vender med vilje. En bomholder, '
        'der sidder, når bommen skal over, forhindrer manøvren midt i '
        'den.':
        'Kom ihåg att ta bort den igen innan du gippar med flit. En '
        'preventerlina som sitter när bommen ska över hindrar manövern '
        'mitt i den.',
    'Hvornår der skal rebes':
        'När det ska revas',
    'Tidligere end du tror — og altid før det bliver nødvendigt.':
        'Tidigare än du tror — och alltid innan det blir nödvändigt.',
    'En god regel: reb, når du begynder at overveje det. Tanken '
        'kommer som regel et kvarter, før det er ubehageligt, og det er '
        'langt nemmere at rebe, mens det stadig er behageligt.':
        'En bra regel: reva när du börjar överväga det. Tanken kommer i '
        'regel en kvart innan det blir obehagligt, och det är långt '
        'lättare att reva medan det fortfarande är behagligt.',
    'På kryds mærkes vinden hårdere end på læns, fordi bådens egen '
        'fart lægges til. Derfor rebes der tidligere op mod vinden end '
        'ned med den, og derfor kan en tur, der var rar på vej ud, være '
        'noget andet på vej hjem.':
        'På kryss känns vinden hårdare än på läns, eftersom båtens egen '
        'fart läggs till. Därför revas det tidigare på väg upp mot vinden '
        'än ner med den, och därför kan en resa som var trevlig på vägen '
        'ut vara något annat på vägen hem.',
    'Et reb koster sjældent fart. En overtrimmet båd krænger, skrider '
        'sidelæns og er trættende at styre — den rebede er ofte hurtigere '
        'over grunden og altid nemmere at være ombord på.':
        'Ett rev kostar sällan fart. En övertrimmad båt kränger, glider i '
        'sidled och är tröttsam att styra — den revade är ofta snabbare '
        'över grund och alltid enklare att vara ombord på.',
    'VHF — opkald og nødopkald':
        'VHF — anrop och nödanrop',
    'Kanal 16 til nød og opkald. Og MAYDAY ord for ord.':
        'Kanal 16 för nöd och anrop. Och MAYDAY ord för ord.',
    'Til daglig kræver en VHF et SRC-bevis, og anlægget skal være '
        'tilladt til båden. Men er nogen i fare, må enhver ombord bruge '
        'ethvert middel til at tilkalde hjælp. Så tag mikrofonen — ingen '
        'er nogensinde blevet straffet for at kalde MAYDAY, når der var '
        'brug for det.':
        'Till vardags kräver en VHF ett SRC-certifikat, och anläggningen '
        'ska vara tillståndsgiven för båten. Men är någon i fara får vem '
        'som helst ombord använda vilket medel som helst för att kalla på '
        'hjälp. Så ta mikrofonen — ingen har någonsin straffats för att '
        'ha ropat MAYDAY när det behövdes.',
    'Kanal 16 er til nød og til at kalde hinanden op. Har I fået fat '
        'i hinanden, så aftal en arbejdskanal — 06, 08, 72 eller 77 — og '
        'flyt derover, så 16 er fri. Kanal 13 er skib til skib om '
        'manøvrer; det er dér, du kalder færgen i et smalt løb. På 70 '
        'tales der aldrig — den er radioens egen til DSC.':
        'Kanal 16 är för nöd och för att anropa varandra. Har ni fått tag '
        'i varandra, kom överens om en arbetskanal — 06, 08, 72 eller 77 '
        '— och flytta dit, så att 16 är fri. Kanal 13 är fartyg till '
        'fartyg om manövrar; det är där du anropar färjan i en trång led. '
        'På 70 talas det aldrig — den är radions egen för DSC.',
    'Et opkald lyder: modtagerens navn to gange, "dette er" og dit '
        'eget navn to gange, og så Skift. Skift betyder "nu venter jeg '
        'svar". Slut betyder "samtalen er forbi".':
        'Ett anrop låter: mottagarens namn två gånger, ”det här är” och '
        'ditt eget namn två gånger, och sedan Kom. Kom betyder ”nu väntar '
        'jag svar”. Slut betyder ”samtalet är över”.',
    'Et nødopkald har en fast rækkefølge, og det er rækkefølgen, der '
        'gør, at redningen ved, hvor de skal hen og hvad de skal have '
        'med: MAYDAY tre gange, bådens navn tre gange, MAYDAY og navnet '
        'igen, position, hvad der er sket, hvad du beder om, hvor mange I '
        'er, hvordan båden ser ud — og Skift. Svarer ingen, så gentag det '
        'hele.':
        'Ett nödanrop har en fast ordning, och det är ordningen som gör '
        'att räddningen vet vart de ska och vad de ska ha med sig: MAYDAY '
        'tre gånger, båtens namn tre gånger, MAYDAY och namnet igen, '
        'position, vad som har hänt, vad du ber om, hur många ni är, hur '
        'båten ser ut — och Kom. Svarar ingen, upprepa alltihop.',
    'PAN-PAN er den, der ikke er livstruende endnu: motoren er død i '
        'et sejlløb, nogen er syg men ikke i fare. SÉCURITÉ er en '
        'advarsel til alle andre om noget i vandet.':
        'PAN-PAN är den som inte är livshotande ännu: motorn har lagt av '
        'i en farled, någon är sjuk men inte i fara. SÉCURITÉ är en '
        'varning till alla andra om något i vattnet.',
    'Den røde knap under klappen er DSC. Hold den nede i fem sekunder '
        '— radioen sender bådens MMSI og positionen af sig selv. Følg '
        'altid op med stemmen på 16: alarmen siger, at nogen har brug for '
        'hjælp, ikke hvad der er sket. Hele opkaldet står ord for ord '
        'under bogikonet på kortet.':
        'Den röda knappen under luckan är DSC. Håll den nere i fem '
        'sekunder — radion skickar båtens MMSI och positionen av sig '
        'själv. Följ alltid upp med rösten på 16: larmet säger att någon '
        'behöver hjälp, inte vad som har hänt. Hela anropet står ord för '
        'ord under bokikonen på kartan.',
    'Til daglig kræver en VHF et SRC-bevis, og anlægget skal være '
        'tilladt til båden. Men er nogen i fare, må enhver ombord bruge '
        'ethvert middel til at tilkalde hjælp. Så tag mikrofonen. Ingen '
        'er nogensinde blevet straffet for at kalde MAYDAY, når der var '
        'brug for det.':
        'Till vardags kräver en VHF ett SRC-certifikat, och anläggningen '
        'ska vara tillståndsgiven för båten. Men är någon i fara får vem '
        'som helst ombord använda vilket medel som helst för att kalla på '
        'hjälp. Så ta mikrofonen — ingen har någonsin straffats för att '
        'ha ropat MAYDAY när det behövdes.',
    '16':
        '16',
    'Nød, hastemeddelelser og opkald. Lyt her, når du sejler. Flyt '
        'over på en arbejdskanal, så snart I har fået fat i hinanden.':
        'Nöd, brådskande meddelanden och anrop. Lyssna här när du seglar. '
        'Flytta över på en arbetskanal så snart ni har fått tag i '
        'varandra.',
    '70':
        '70',
    'DSC — den digitale nødknap. Her tales der aldrig. Radioen bruger '
        'kanalen selv.':
        'DSC — den digitala nödknappen. Här talas det aldrig. Radion '
        'använder kanalen själv.',
    '13':
        '13',
    'Skib til skib om manøvrer. Det er her, du kalder færgen eller '
        'coasteren, der kommer imod dig i et smalt løb.':
        'Fartyg till fartyg om manövrar. Det är här du anropar färjan '
        'eller kustfartyget som kommer emot dig i en trång led.',
    '06 · 08 · 72 · 77':
        '06 · 08 · 72 · 77',
    'Arbejdskanaler mellem både. Aftal en, når I har kaldt hinanden '
        'op på 16.':
        'Arbetskanaler mellan båtar. Kom överens om en när ni har anropat '
        'varandra på 16.',
    'Lyngby Radio':
        'Lyngby Radio',
    'Den danske kystradio. Nødtrafik, farvandsudsigter og '
        'efterretninger. Kalder du 16, hører de med.':
        'Den danska kustradion. I Sverige är det Stockholm Radio. '
        'Nödtrafik, sjöväderrapporter och underrättelser. Anropar du 16 '
        'lyssnar de.',
    'Havnens kanal':
        'Hamnens kanal',
    'Mange havne og broer lytter på deres egen kanal. Den står i '
        'havnelodsen — slå den op, før du kommer.':
        'Många hamnar och broar lyssnar på sin egen kanal. Den står i '
        'hamnguiden — slå upp den innan du kommer.',
    'SKIFT':
        'KOM',
    'Jeg er færdig, og jeg venter svar. På engelsk: OVER.':
        'Jag är klar och väntar svar. På engelska: OVER.',
    'SLUT':
        'SLUT',
    'Samtalen er slut. Jeg venter ikke svar. OUT.':
        'Samtalet är avslutat. Jag väntar inget svar. OUT.',
    'MODTAGET':
        'UPPFATTAT',
    'Jeg har hørt og forstået. ROGER.':
        'Jag har hört och förstått. ROGER.',
    'GENTAG':
        'REPETERA',
    'Sig det igen. SAY AGAIN.':
        'Säg det igen. SAY AGAIN.',
    'VENT':
        'VÄNTA',
    'Bliv på kanalen, jeg kommer tilbage. STAND BY.':
        'Stanna på kanalen, jag återkommer. STAND BY.',
    'STAVER':
        'JAG BOKSTAVERAR',
    'Nu bogstaverer jeg. I SPELL.':
        'Nu bokstaverar jag. I SPELL.',
    'Marstal Havn, Marstal Havn — dette er Havfruen, Havfruen. Skift.':
        'Marstal Hamn, Marstal Hamn — det här är Havfruen, Havfruen. Kom.',
    'Når I har svaret hinanden: aftal en arbejdskanal og flyt '
        'derover. Kanal 16 skal være fri.':
        'När ni har svarat varandra: kom överens om en arbetskanal och '
        'flytta dit. Kanal 16 ska vara fri.',
    'PAN-PAN, tre gange, er den, der ikke er livstruende endnu: '
        'motoren er død i et sejlløb, nogen er syg, men ikke i fare, I er '
        'drevet på grund i roligt vejr. Ellers er formen den samme som '
        'MAYDAY.':
        'PAN-PAN, tre gånger, är den som inte är livshotande ännu: motorn '
        'har lagt av i en farled, någon är sjuk men inte i fara, ni har '
        'gått på grund i lugnt väder. I övrigt är formen densamma som '
        'MAYDAY.',
    'SÉCURITÉ, tre gange, er en advarsel til alle andre — en drivende '
        'genstand, et sømærke der er væk. Sig den på 16 og flyt over på '
        'en arbejdskanal med selve meldingen.':
        'SÉCURITÉ, tre gånger, är en varning till alla andra — ett '
        'drivande föremål, ett sjömärke som är borta. Säg den på 16 och '
        'flytta över på en arbetskanal med själva meddelandet.',
    'Den røde knap under klappen er DSC-nødalarmen. Hold den nede i '
        'fem sekunder. Radioen sender bådens MMSI og — er den koblet til '
        'en GPS — positionen, til alle skibe og kyststationer i nærheden.':
        'Den röda knappen under luckan är DSC-nödlarmet. Håll den nere i '
        'fem sekunder. Radion skickar båtens MMSI och — är den kopplad '
        'till en GPS — positionen, till alla fartyg och '
        'kustradiostationer i närheten.',
    'Følg altid op med stemmen på kanal 16. Alarmen siger, at nogen '
        'har brug for hjælp; den siger ikke, hvad der er sket.':
        'Följ alltid upp med rösten på kanal 16. Larmet säger att någon '
        'behöver hjälp; det säger inte vad som har hänt.',
    'Hører du en andens nødalarm og ingen svarer, så svar. Kan du '
        'ikke hjælpe selv, så giv den videre: "MAYDAY RELAY" og hvad du '
        'har hørt.':
        'Hör du någon annans nödlarm och ingen svarar, svara du. Kan du '
        'inte hjälpa själv, för det vidare: ”MAYDAY RELAY” och vad du har '
        'hört.',
    'MAYDAY — MAYDAY — MAYDAY':
        'MAYDAY — MAYDAY — MAYDAY',
    'Kun når der er fare for liv eller for at båden går tabt.':
        'Bara när det finns fara för liv eller för att båten går '
        'förlorad.',
    'Dette er Havfruen, Havfruen, Havfruen':
        'Det här är Havfruen, Havfruen, Havfruen',
    'Bådens navn tre gange. Sig også kaldesignal eller MMSI, hvis du '
        'har det.':
        'Båtens namn tre gånger. Säg också anropssignal eller MMSI om du '
        'har det.',
    'MAYDAY, Havfruen':
        'MAYDAY, Havfruen',
    'Én gang mere, så den, der skriver ned, ved, hvem meldingen er '
        'fra.':
        'En gång till, så att den som skriver ner vet vem meddelandet är '
        'från.',
    'Min position er …':
        'Min position är …',
    'Bredde og længde, hvis du har dem. Ellers: pejling og afstand '
        'til noget, alle kender — "to sømil nord for Sprogø".':
        'Latitud och longitud om du har dem. Annars: bäring och avstånd '
        'till något alla känner till — ”två distansminuter norr om '
        'Sprogø”.',
    'Jeg har …':
        'Jag har …',
    'Hvad der er sket. Brand, vand i båden, mand overbord, alvorlig '
        'tilskadekomst, grundstødning.':
        'Vad som har hänt. Brand, vatten i båten, man överbord, allvarlig '
        'skada, grundstötning.',
    'Jeg har brug for …':
        'Jag behöver …',
    'Hvad du beder om. Redning, lægehjælp, slæbning.':
        'Vad du ber om. Räddning, läkarhjälp, bogsering.',
    'Vi er … personer ombord':
        'Vi är … personer ombord',
    'Antallet. Det er dét, der afgør, hvad de sender.':
        'Antalet. Det är det som avgör vad de skickar.',
    '… og båden er …':
        '… och båten är …',
    'Kort: længde, farve, sejlbåd eller motorbåd. Nok til at finde '
        'jer.':
        'Kort: längd, färg, segel- eller motorbåt. Nog för att hitta er.',
    'Skift':
        'Kom',
    'Slip knappen og lyt. Svarer ingen, så gentag det hele.':
        'Släpp knappen och lyssna. Svarar ingen, upprepa alltihop.',
}
