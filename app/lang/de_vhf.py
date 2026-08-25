"""Trimkapitlet og VHF på tysk.

Nøglen er den danske sætning fra `app/trim.py` og `app/seamanship.py`.

VHF-udtrykkene er de tyske procedureord, ikke oversættelser: KOMMEN for skift,
ENDE for slut, VERSTANDEN for modtaget. MAYDAY, PAN-PAN og SÉCURITÉ er de
samme på alle sprog — det er hele pointen med dem.
"""

WORDS: dict[str, str] = {
    'VHF':
        'UKW',
    'Når det ikke er MAYDAY':
        'Wenn es kein MAYDAY ist',
    'DSC — den røde knap':
        'DSC — die rote Taste',
    'Kanaler':
        'Kanäle',
    'Et almindeligt opkald':
        'Ein gewöhnlicher Anruf',
    'Nødopkald — læs ovenfra og ned':
        'Notruf — von oben nach unten ablesen',
    'Udtryk':
        'Redewendungen',
    'Sådan bruger du trimrådet':
        'So benutzt du den Trimmratschlag',
    'Under hvert stræk i sejlplanen, og i opslagsværket på kortet.':
        'Unter jedem Abschnitt im Segelplan, und im Nachschlagewerk auf '
        'der Karte.',
    'Planen kender vindens vinkel ind på båden og hvor hårdt det '
        'blæser på hvert stræk. Det er nok til et rigtigt råd, og det '
        'ligger foldet sammen under strækket: tryk "Optimér mine sejl".':
        'Der Plan kennt den Winkel, in dem der Wind auf das Boot trifft, '
        'und wie hart es auf jedem Abschnitt weht. Das reicht für einen '
        'richtigen Rat, und er liegt zusammengefaltet unter dem '
        'Abschnitt: Tippe auf „Meine Segel trimmen“.',
    'Vil du slå op uden at have lagt en rute — hvordan står bommen nu '
        'igen for halvvind — så ligger det samme under bogikonet på '
        'kortet, med en tegning af sejlføringen set oppefra.':
        'Willst du nachschlagen, ohne eine Route gelegt zu haben — wie '
        'stand der Baum noch mal bei halbem Wind — dann liegt dasselbe '
        'unter dem Buchsymbol auf der Karte, mit einer Zeichnung der '
        'Segelstellung von oben.',
    'Det er et udgangspunkt, ikke en facitliste. Sejlene er dine, og '
        'en tiårig dacronsæk vil noget andet end et nyt laminatsejl. '
        'Rådene er skrevet til en almindelig krydser med storsejl og '
        'rullegenua.':
        'Es ist ein Ausgangspunkt, keine Musterlösung. Die Segel sind '
        'deine, und ein zehn Jahre alter Dacronsack will etwas anderes '
        'als ein neues Laminatsegel. Die Ratschläge sind für einen '
        'gewöhnlichen Fahrtenkreuzer mit Großsegel und Rollgenua '
        'geschrieben.',
    'Hvad delene gør':
        'Was die Teile tun',
    'Syv liner, og hver af dem ændrer én ting ved sejlet.':
        'Sieben Leinen, und jede von ihnen ändert eine Sache am Segel.',
    'Storskødet trækker bommen ind og ned på én gang. På kryds er det '
        'dét, der holder bommen nede — derfor skal bomnedhalet være løst '
        'der.':
        'Die Großschot zieht den Baum zugleich nach innen und nach unten. '
        'Am Wind ist sie es, die den Baum unten hält — deshalb muss der '
        'Baumniederholer dort lose sein.',
    'Løjgangsvognen flytter bommen sideværts, uden at ændre hvor '
        'hårdt sejlet er skødet ned. Det er dét, der lader dig lette '
        'trykket i en byge uden at åbne toppen af sejlet: kør vognen i læ '
        'i stedet for at slække skødet.':
        'Der Traveller verschiebt den Baum seitlich, ohne zu ändern, wie '
        'dicht das Segel nach unten geschotet ist. Das ist es, was dich '
        'den Druck in einer Bö herausnehmen lässt, ohne den Kopf des '
        'Segels zu öffnen: Fahre den Traveller nach Lee, statt die Schot '
        'zu fieren.',
    'Bomnedhalet holder bommen nede, når skødet ikke længere kan — '
        'altså fra halvvind og ned. Uden det løfter bommen sig, toppen af '
        'sejlet falder af, og du mister det tryk, du troede du havde.':
        'Der Baumniederholer hält den Baum unten, wenn die Schot es nicht '
        'mehr kann — also ab halbem Wind und weiter. Ohne ihn hebt sich '
        'der Baum, der Kopf des Segels fällt ab, und du verlierst den '
        'Druck, den du zu haben glaubtest.',
    'Udhalet strækker underliget. Stramt giver et fladt sejl forneden '
        'til meget vind; løst giver dybde til lidt vind.':
        'Der Unterliekstrecker streckt das Unterliek. Dicht gibt ein '
        'flaches Segel unten für viel Wind; lose gibt Profiltiefe für '
        'wenig Wind.',
    'Nedhalet strammer forliget langs masten. Det flytter sejlets '
        'dybeste punkt fremad og flader sejlet. Stram det, når det '
        'blæser, og lad det være løst, når det ikke gør.':
        'Der Cunningham holt das Vorliek längs des Mastes dicht. Das '
        'schiebt den tiefsten Punkt des Segels nach vorn und flacht es '
        'ab. Hol ihn dicht, wenn es weht, und lass ihn lose, wenn nicht.',
    'Agterstaget bøjer masten. Storsejlet flader ud, og forstaget '
        'bliver stivere — og et stift forstag er dét, der gør, at du kan '
        'holde højde i frisk vind.':
        'Das Achterstag biegt den Mast. Das Großsegel flacht ab, und das '
        'Vorstag wird steifer — und ein steifes Vorstag ist es, was dich '
        'bei frischer Brise Höhe halten lässt.',
    'Skødevognen på forsejlet bestemmer, om skødet trækker mest nedad '
        'eller mest bagud. Frem: dybde forneden og lukket top. Agter: '
        'fladt forneden og åben top.':
        'Der Holepunkt am Vorsegel bestimmt, ob die Schot mehr nach unten '
        'oder mehr nach achtern zieht. Vorn: Profiltiefe unten und '
        'geschlossener Kopf. Achtern: flach unten und offener Kopf.',
    'Twist — hvorfor toppen skal stå anderledes':
        'Twist — warum der Kopf anders stehen muss',
    'Vinden foroven er både stærkere og kommer fra en anden vinkel.':
        'Der Wind oben ist stärker und kommt aus einem anderen Winkel.',
    'Vinden bremses af vandet, så den er svagere nede ved bommen end '
        'oppe i toppen af masten. Og fordi båden selv sejler, kommer den '
        'tilsyneladende vind ind i en anden vinkel foroven end forneden.':
        'Der Wind wird vom Wasser gebremst, also ist er unten am Baum '
        'schwächer als oben im Masttop. Und weil das Boot selbst fährt, '
        'trifft der scheinbare Wind oben in einem anderen Winkel ein als '
        'unten.',
    'Twist er den vridning, der lader toppen af sejlet stå i den '
        'vinkel, den faktisk får. Er der for lidt twist, står toppen for '
        'hårdt og lægger båden ned. Er der for meget, laver toppen '
        'ingenting.':
        'Twist ist die Verwindung, die den Kopf des Segels in dem Winkel '
        'stehen lässt, den er tatsächlich bekommt. Ist zu wenig Twist '
        'drin, steht der Kopf zu dicht und legt das Boot. Ist zu viel '
        'drin, macht der Kopf nichts.',
    'Du styrer det med skødet og bomnedhalet: strammere giver mindre '
        'twist. Kig på øverste sejlpind — den skal stå omtrent parallel '
        'med bommen. I byger må den gerne falde en smule af.':
        'Du steuerst ihn mit der Schot und dem Baumniederholer: dichter '
        'heißt weniger Twist. Sieh auf die oberste Latte — sie soll etwa '
        'parallel zum Baum stehen. In Böen darf sie eine Spur abfallen.',
    'Krængning og rortryk':
        'Krängung und Ruderdruck',
    'To ting båden fortæller dig, som er mere værd end noget '
        'instrument.':
        'Zwei Dinge, die das Boot dir sagt und die mehr wert sind als '
        'jedes Instrument.',
    'En almindelig krydser sejler bedst under omkring tyve graders '
        'krængning. Derover skrider den sidelæns i stedet for fremad, og '
        'du taber både fart og højde. Ligger den længere ned, er det ikke '
        'en stærk sejlads — det er for meget sejl.':
        'Ein gewöhnlicher Fahrtenkreuzer segelt am besten unter etwa '
        'zwanzig Grad Krängung. Darüber rutscht er seitwärts statt '
        'vorwärts, und du verlierst Fahrt und Höhe. Legt er sich weiter, '
        'ist das kein kraftvolles Segeln — es ist zu viel Tuch.',
    'Rortryk er det andet tegn. Skal du hele tiden holde imod for at '
        'undgå, at båden luffer op, er der for meget tryk agter i båden. '
        'Så er det storsejlet, der skal rebes — ikke forsejlet.':
        'Ruderdruck ist das zweite Zeichen. Musst du dauernd gegenhalten, '
        'damit das Boot nicht anluvt, ist zu viel Druck achtern im Boot. '
        'Dann muss das Großsegel gerefft werden — nicht das Vorsegel.',
    'Ruller man genuaen ind og lader storsejlet stå, bliver '
        'rortrykket værre, ikke bedre. Det er den fejl, de fleste gør '
        'først, fordi rullegenuaen er den nemmeste at tage af.':
        'Rollt man die Genua ein und lässt das Großsegel stehen, wird der '
        'Ruderdruck schlimmer, nicht besser. Das ist der Fehler, den die '
        'meisten zuerst machen, weil die Rollgenua am leichtesten '
        'wegzunehmen ist.',
    'Bomholder på læns':
        'Bullenstander vor dem Wind',
    'Det ene sted, hvor trimmet ikke handler om fart.':
        'Die eine Stelle, an der Trimm nicht von Geschwindigkeit handelt.',
    'Fra rumskøds og ned mod læns kan bommen slå over af sig selv, '
        'hvis båden gribes af en bølge eller styrmanden falder for langt '
        'af. Det sker hurtigt, og bommen kommer i hovedhøjde.':
        'Von raumem Wind bis vor den Wind kann der Baum von selbst '
        'herüberschlagen, wenn das Boot von einer Welle gepackt wird oder '
        'der Rudergänger zu weit abfällt. Das geht schnell, und der Baum '
        'kommt auf Kopfhöhe.',
    'En bomholder er en line fra bommen og frem til dækket, der '
        'holder den ude. Sæt den, før du falder af — ikke bagefter. Det '
        'er dét, der gør en utilsigtet bomvending til en irritation i '
        'stedet for en ulykke.':
        'Ein Bullenstander ist eine Leine vom Baum nach vorn an Deck, die '
        'ihn draußen hält. Setze ihn, bevor du abfällst — nicht danach. '
        'Das ist es, was aus einer unbeabsichtigten Patenthalse ein '
        'Ärgernis statt eines Unfalls macht.',
    'Husk at tage den af igen, før du vender med vilje. En bomholder, '
        'der sidder, når bommen skal over, forhindrer manøvren midt i '
        'den.':
        'Denk daran, ihn wieder zu lösen, bevor du absichtlich halst. Ein '
        'Bullenstander, der sitzt, wenn der Baum herüber soll, verhindert '
        'das Manöver mitten darin.',
    'Hvornår der skal rebes':
        'Wann gerefft werden muss',
    'Tidligere end du tror — og altid før det bliver nødvendigt.':
        'Früher, als du denkst — und immer, bevor es nötig wird.',
    'En god regel: reb, når du begynder at overveje det. Tanken '
        'kommer som regel et kvarter, før det er ubehageligt, og det er '
        'langt nemmere at rebe, mens det stadig er behageligt.':
        'Eine gute Regel: Reffe, wenn du anfängst, darüber nachzudenken. '
        'Der Gedanke kommt in der Regel eine Viertelstunde, bevor es '
        'unangenehm wird, und es ist weit leichter zu reffen, solange es '
        'noch angenehm ist.',
    'På kryds mærkes vinden hårdere end på læns, fordi bådens egen '
        'fart lægges til. Derfor rebes der tidligere op mod vinden end '
        'ned med den, og derfor kan en tur, der var rar på vej ud, være '
        'noget andet på vej hjem.':
        'Am Wind fühlt sich der Wind härter an als vor dem Wind, weil die '
        'eigene Fahrt des Bootes dazukommt. Deshalb wird auf dem Weg nach '
        'oben früher gerefft als nach unten, und deshalb kann ein Törn, '
        'der hinaus schön war, auf dem Rückweg etwas anderes sein.',
    'Et reb koster sjældent fart. En overtrimmet båd krænger, skrider '
        'sidelæns og er trættende at styre — den rebede er ofte hurtigere '
        'over grunden og altid nemmere at være ombord på.':
        'Ein Reff kostet selten Fahrt. Ein übertrimmtes Boot krängt, '
        'rutscht seitwärts und ist anstrengend zu steuern — das gereffte '
        'ist oft schneller über Grund und immer angenehmer an Bord.',
    'VHF — opkald og nødopkald':
        'UKW — Anruf und Notruf',
    'Kanal 16 til nød og opkald. Og MAYDAY ord for ord.':
        'Kanal 16 für Not und Anruf. Und MAYDAY Wort für Wort.',
    'Til daglig kræver en VHF et SRC-bevis, og anlægget skal være '
        'tilladt til båden. Men er nogen i fare, må enhver ombord bruge '
        'ethvert middel til at tilkalde hjælp. Så tag mikrofonen — ingen '
        'er nogensinde blevet straffet for at kalde MAYDAY, når der var '
        'brug for det.':
        'Im Alltag braucht eine UKW-Anlage ein SRC-Zeugnis, und das Gerät '
        'muss für das Boot zugelassen sein. Ist aber jemand in Gefahr, '
        'darf jeder an Bord jedes Mittel benutzen, um Hilfe zu rufen. '
        'Also nimm das Mikrofon — niemand ist je dafür bestraft worden, '
        'MAYDAY gerufen zu haben, als es nötig war.',
    'Kanal 16 er til nød og til at kalde hinanden op. Har I fået fat '
        'i hinanden, så aftal en arbejdskanal — 06, 08, 72 eller 77 — og '
        'flyt derover, så 16 er fri. Kanal 13 er skib til skib om '
        'manøvrer; det er dér, du kalder færgen i et smalt løb. På 70 '
        'tales der aldrig — den er radioens egen til DSC.':
        'Kanal 16 ist für Not und um einander anzurufen. Habt ihr euch '
        'erreicht, dann verabredet einen Arbeitskanal — 06, 08, 72 oder '
        '77 — und geht dorthin, damit 16 frei ist. Kanal 13 ist Schiff zu '
        'Schiff über Manöver; dort rufst du die Fähre im engen '
        'Fahrwasser. Auf 70 wird nie gesprochen — der gehört dem Gerät '
        'für DSC.',
    'Et opkald lyder: modtagerens navn to gange, "dette er" og dit '
        'eget navn to gange, og så Skift. Skift betyder "nu venter jeg '
        'svar". Slut betyder "samtalen er forbi".':
        'Ein Anruf klingt so: der Name des Empfängers zweimal, „hier ist“ '
        'und dein eigener Name zweimal, und dann Kommen. Kommen heißt '
        '„jetzt warte ich auf Antwort“. Ende heißt „das Gespräch ist '
        'vorbei“.',
    'Et nødopkald har en fast rækkefølge, og det er rækkefølgen, der '
        'gør, at redningen ved, hvor de skal hen og hvad de skal have '
        'med: MAYDAY tre gange, bådens navn tre gange, MAYDAY og navnet '
        'igen, position, hvad der er sket, hvad du beder om, hvor mange I '
        'er, hvordan båden ser ud — og Skift. Svarer ingen, så gentag det '
        'hele.':
        'Ein Notruf hat eine feste Reihenfolge, und die Reihenfolge ist '
        'es, die die Rettung wissen lässt, wohin sie muss und was sie '
        'mitnehmen soll: MAYDAY dreimal, der Name des Bootes dreimal, '
        'MAYDAY und der Name noch einmal, Position, was passiert ist, '
        'worum du bittest, wie viele ihr seid, wie das Boot aussieht — '
        'und Kommen. Antwortet niemand, dann wiederhole das Ganze.',
    'PAN-PAN er den, der ikke er livstruende endnu: motoren er død i '
        'et sejlløb, nogen er syg men ikke i fare. SÉCURITÉ er en '
        'advarsel til alle andre om noget i vandet.':
        'PAN-PAN ist das, was noch nicht lebensbedrohlich ist: die '
        'Maschine ist im Fahrwasser ausgefallen, jemand ist krank, aber '
        'nicht in Gefahr. SÉCURITÉ ist eine Warnung an alle anderen über '
        'etwas im Wasser.',
    'Den røde knap under klappen er DSC. Hold den nede i fem sekunder '
        '— radioen sender bådens MMSI og positionen af sig selv. Følg '
        'altid op med stemmen på 16: alarmen siger, at nogen har brug for '
        'hjælp, ikke hvad der er sket. Hele opkaldet står ord for ord '
        'under bogikonet på kortet.':
        'Die rote Taste unter der Klappe ist DSC. Halte sie fünf Sekunden '
        'gedrückt — das Gerät sendet die MMSI des Bootes und die Position '
        'von selbst. Folge immer mit der Stimme auf 16 nach: Der Alarm '
        'sagt, dass jemand Hilfe braucht, nicht was passiert ist. Der '
        'ganze Notruf steht Wort für Wort unter dem Buchsymbol auf der '
        'Karte.',
    'Til daglig kræver en VHF et SRC-bevis, og anlægget skal være '
        'tilladt til båden. Men er nogen i fare, må enhver ombord bruge '
        'ethvert middel til at tilkalde hjælp. Så tag mikrofonen. Ingen '
        'er nogensinde blevet straffet for at kalde MAYDAY, når der var '
        'brug for det.':
        'Im Alltag braucht eine UKW-Anlage ein SRC-Zeugnis, und das Gerät '
        'muss für das Boot zugelassen sein. Ist aber jemand in Gefahr, '
        'darf jeder an Bord jedes Mittel benutzen, um Hilfe zu rufen. '
        'Also nimm das Mikrofon — niemand ist je dafür bestraft worden, '
        'MAYDAY gerufen zu haben, als es nötig war.',
    '16':
        '16',
    'Nød, hastemeddelelser og opkald. Lyt her, når du sejler. Flyt '
        'over på en arbejdskanal, så snart I har fået fat i hinanden.':
        'Not, Dringlichkeit und Anruf. Hör hier mit, wenn du unterwegs '
        'bist. Wechselt auf einen Arbeitskanal, sobald ihr einander '
        'erreicht habt.',
    '70':
        '70',
    'DSC — den digitale nødknap. Her tales der aldrig. Radioen bruger '
        'kanalen selv.':
        'DSC — die digitale Nottaste. Hier wird nie gesprochen. Das Gerät '
        'benutzt den Kanal selbst.',
    '13':
        '13',
    'Skib til skib om manøvrer. Det er her, du kalder færgen eller '
        'coasteren, der kommer imod dig i et smalt løb.':
        'Schiff zu Schiff über Manöver. Hier rufst du die Fähre oder den '
        'Coaster, der dir im engen Fahrwasser entgegenkommt.',
    '06 · 08 · 72 · 77':
        '06 · 08 · 72 · 77',
    'Arbejdskanaler mellem både. Aftal en, når I har kaldt hinanden '
        'op på 16.':
        'Arbeitskanäle zwischen Booten. Verabredet einen, wenn ihr euch '
        'auf 16 angerufen habt.',
    'Lyngby Radio':
        'Lyngby Radio',
    'Den danske kystradio. Nødtrafik, farvandsudsigter og '
        'efterretninger. Kalder du 16, hører de med.':
        'Die dänische Küstenfunkstelle. Notverkehr, Seewetterberichte und '
        'Nachrichten. Rufst du auf 16, hören sie mit.',
    'Havnens kanal':
        'Der Kanal des Hafens',
    'Mange havne og broer lytter på deres egen kanal. Den står i '
        'havnelodsen — slå den op, før du kommer.':
        'Viele Häfen und Brücken hören auf ihrem eigenen Kanal. Er steht '
        'im Hafenhandbuch — schlag ihn nach, bevor du ankommst.',
    'SKIFT':
        'KOMMEN',
    'Jeg er færdig, og jeg venter svar. På engelsk: OVER.':
        'Ich bin fertig und warte auf Antwort. Auf Englisch: OVER.',
    'SLUT':
        'ENDE',
    'Samtalen er slut. Jeg venter ikke svar. OUT.':
        'Das Gespräch ist beendet. Ich warte keine Antwort ab. OUT.',
    'MODTAGET':
        'VERSTANDEN',
    'Jeg har hørt og forstået. ROGER.':
        'Ich habe gehört und verstanden. ROGER.',
    'GENTAG':
        'WIEDERHOLEN',
    'Sig det igen. SAY AGAIN.':
        'Sag es noch einmal. SAY AGAIN.',
    'VENT':
        'WARTEN',
    'Bliv på kanalen, jeg kommer tilbage. STAND BY.':
        'Bleib auf dem Kanal, ich komme zurück. STAND BY.',
    'STAVER':
        'ICH BUCHSTABIERE',
    'Nu bogstaverer jeg. I SPELL.':
        'Jetzt buchstabiere ich. I SPELL.',
    'Marstal Havn, Marstal Havn — dette er Havfruen, Havfruen. Skift.':
        'Hafen Marstal, Hafen Marstal — hier ist Havfruen, Havfruen. '
        'Kommen.',
    'Når I har svaret hinanden: aftal en arbejdskanal og flyt '
        'derover. Kanal 16 skal være fri.':
        'Wenn ihr einander geantwortet habt: Verabredet einen '
        'Arbeitskanal und geht dorthin. Kanal 16 muss frei sein.',
    'PAN-PAN, tre gange, er den, der ikke er livstruende endnu: '
        'motoren er død i et sejlløb, nogen er syg, men ikke i fare, I er '
        'drevet på grund i roligt vejr. Ellers er formen den samme som '
        'MAYDAY.':
        'PAN-PAN, dreimal, ist das, was noch nicht lebensbedrohlich ist: '
        'die Maschine ist im Fahrwasser ausgefallen, jemand ist krank, '
        'aber nicht in Gefahr, ihr seid bei ruhigem Wetter aufgelaufen. '
        'Sonst ist die Form dieselbe wie beim MAYDAY.',
    'SÉCURITÉ, tre gange, er en advarsel til alle andre — en drivende '
        'genstand, et sømærke der er væk. Sig den på 16 og flyt over på '
        'en arbejdskanal med selve meldingen.':
        'SÉCURITÉ, dreimal, ist eine Warnung an alle anderen — ein '
        'treibender Gegenstand, ein Seezeichen, das fehlt. Sag sie auf 16 '
        'und geh mit der eigentlichen Meldung auf einen Arbeitskanal.',
    'Den røde knap under klappen er DSC-nødalarmen. Hold den nede i '
        'fem sekunder. Radioen sender bådens MMSI og — er den koblet til '
        'en GPS — positionen, til alle skibe og kyststationer i nærheden.':
        'Die rote Taste unter der Klappe ist der DSC-Notalarm. Halte sie '
        'fünf Sekunden gedrückt. Das Gerät sendet die MMSI des Bootes und '
        '— ist es an ein GPS angeschlossen — die Position, an alle '
        'Schiffe und Küstenfunkstellen in der Nähe.',
    'Følg altid op med stemmen på kanal 16. Alarmen siger, at nogen '
        'har brug for hjælp; den siger ikke, hvad der er sket.':
        'Folge immer mit der Stimme auf Kanal 16 nach. Der Alarm sagt, '
        'dass jemand Hilfe braucht; er sagt nicht, was passiert ist.',
    'Hører du en andens nødalarm og ingen svarer, så svar. Kan du '
        'ikke hjælpe selv, så giv den videre: "MAYDAY RELAY" og hvad du '
        'har hørt.':
        'Hörst du den Notalarm eines anderen und niemand antwortet, dann '
        'antworte du. Kannst du selbst nicht helfen, dann gib ihn weiter: '
        '„MAYDAY RELAY“ und was du gehört hast.',
    'MAYDAY — MAYDAY — MAYDAY':
        'MAYDAY — MAYDAY — MAYDAY',
    'Kun når der er fare for liv eller for at båden går tabt.':
        'Nur wenn Gefahr für Leben besteht oder das Boot verloren zu '
        'gehen droht.',
    'Dette er Havfruen, Havfruen, Havfruen':
        'Hier ist Havfruen, Havfruen, Havfruen',
    'Bådens navn tre gange. Sig også kaldesignal eller MMSI, hvis du '
        'har det.':
        'Der Name des Bootes dreimal. Nenne auch Rufzeichen oder MMSI, '
        'wenn du sie hast.',
    'MAYDAY, Havfruen':
        'MAYDAY, Havfruen',
    'Én gang mere, så den, der skriver ned, ved, hvem meldingen er '
        'fra.':
        'Noch einmal, damit der, der mitschreibt, weiß, von wem die '
        'Meldung ist.',
    'Min position er …':
        'Meine Position ist …',
    'Bredde og længde, hvis du har dem. Ellers: pejling og afstand '
        'til noget, alle kender — "to sømil nord for Sprogø".':
        'Breite und Länge, wenn du sie hast. Sonst: Peilung und Abstand '
        'zu etwas, das jeder kennt — „zwei Seemeilen nördlich von '
        'Sprogø“.',
    'Jeg har …':
        'Ich habe …',
    'Hvad der er sket. Brand, vand i båden, mand overbord, alvorlig '
        'tilskadekomst, grundstødning.':
        'Was passiert ist. Feuer, Wassereinbruch, Mann über Bord, schwere '
        'Verletzung, Grundberührung.',
    'Jeg har brug for …':
        'Ich brauche …',
    'Hvad du beder om. Redning, lægehjælp, slæbning.':
        'Worum du bittest. Rettung, ärztliche Hilfe, Schleppen.',
    'Vi er … personer ombord':
        'Wir sind … Personen an Bord',
    'Antallet. Det er dét, der afgør, hvad de sender.':
        'Die Anzahl. Das ist es, was bestimmt, was sie schicken.',
    '… og båden er …':
        '… und das Boot ist …',
    'Kort: længde, farve, sejlbåd eller motorbåd. Nok til at finde '
        'jer.':
        'Kurz: Länge, Farbe, Segel- oder Motorboot. Genug, um euch zu '
        'finden.',
    'Skift':
        'Kommen',
    'Slip knappen og lyt. Svarer ingen, så gentag det hele.':
        'Lass die Taste los und hör zu. Antwortet niemand, dann '
        'wiederhole das Ganze.',
}
