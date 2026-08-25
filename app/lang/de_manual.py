"""Manualen på tysk.

Nøglen er den danske sætning fra `app/help.py`, ord for ord. Teksterne står
her og ikke i `de.py`, fordi de er prosa og fylder mere end hele resten af
fladen tilsammen.

Oversat som en sejler ville sige det, ikke ord for ord: sejldøgn er Etmal,
efterretninger for søfarende er Nachrichten für Seefahrer, og "blæst inde"
findes ikke som ét ord på tysk — dér står omskrivningen.
"""

WORDS: dict[str, str] = {
    'Kom i gang':
        'Erste Schritte',
    'Sådan bruges Sejlplan':
        'So funktioniert Segelplan',
    'Tre trin: læg ruten, vælg hvornår du kaster los, læs planen.':
        'Drei Schritte: Route legen, Ablegezeit wählen, Plan lesen.',
    'Først lægger du ruten — mindst to punkter. Søg efter en havn, klik '
        'på kortet, eller slå havnelaget til og vælg en havn. Sejlplan '
        'lægger selv vejen uden om land.':
        'Zuerst legst du die Route — mindestens zwei Punkte. Suche einen '
        'Hafen, klicke auf die Karte, oder schalte die Hafenebene ein und '
        'wähle einen Hafen. Segelplan legt den Weg von selbst um das Land '
        'herum.',
    'Så trykker du Find bedste afgangstider. Vi regner hver eneste '
        'afgangstime igennem i det vindue, du har valgt, og viser dem, der '
        'giver noget forskelligt. Vi peger på én, men du vælger.':
        'Dann drückst du Beste Abfahrtszeiten finden. Wir rechnen jede '
        'einzelne Abfahrtsstunde in deinem Zeitfenster durch und zeigen '
        'die, die etwas anderes ergeben. Wir empfehlen eine — aber du '
        'wählst.',
    'Til sidst står sejlplanen: hvad turen bliver, dag for dag, stræk '
        'for stræk og time for time. Den kan printes, kopieres og læses '
        'uden dækning.':
        'Zuletzt steht der Segelplan da: was aus dem Törn wird, Tag für '
        'Tag, Abschnitt für Abschnitt und Stunde für Stunde. Er lässt sich '
        'drucken, kopieren und ohne Empfang lesen.',
    'Ruten og havvejen':
        'Die Route und der Seeweg',
    'Stregen følger vandet, ikke luftlinjen — derfor er den længere.':
        'Der Strich folgt dem Wasser, nicht der Luftlinie — darum ist er '
        'länger.',
    'Sejlplan lægger ruten uden om land med en søkortsagtig maske over '
        'de danske og skandinaviske farvande. Derfor står der tit "3,7 sm '
        'udenom land" ved et ben: det er, hvad det koster at komme rundt om '
        'pynten i stedet for at sejle gennem den.':
        'Segelplan legt die Route mit einer seekartenähnlichen Maske über '
        'den dänischen und skandinavischen Gewässern um das Land herum. '
        'Deshalb steht an einer Etappe oft „3,7 sm ums Land herum“: So viel '
        'kostet es, um die Landspitze herumzukommen, statt mitten '
        'hindurchzusegeln.',
    'Masken kender land og vand — den kender ikke dybder, sømærker, '
        'ruser eller sejlrender. Kontrollér altid benene på søkortet, især '
        'i smalt farvand og tæt på kysten.':
        'Die Maske kennt Land und Wasser — sie kennt keine Tiefen, keine '
        'Seezeichen, keine Reusen und keine Fahrrinnen. Prüfe die Etappen '
        'immer auf der Seekarte, besonders im engen Fahrwasser und dicht '
        'unter Land.',
    'Du kan trække et punkt på kortet, flytte det op og ned i listen, '
        'og vende hele ruten om under dele-ikonet.':
        'Du kannst einen Punkt auf der Karte verschieben, ihn in der Liste '
        'hoch und runter bewegen und die ganze Route unter dem '
        'Teilen-Symbol umkehren.',
    'Din båd':
        'Dein Boot',
    'Planen er kun din, hvis den regner på din båds fart.':
        'Der Plan ist nur dann deiner, wenn er mit der Fahrt deines Bootes '
        'rechnet.',
    'De faste både er eksempler. Ingen ejer et eksempel, og en plan, '
        'der regner på en anden båds fart, er ikke din plan. Læg din egen '
        'ind under Indstillinger.':
        'Die vorgegebenen Boote sind Beispiele. Ein Beispiel gehört '
        'niemandem, und ein Plan, der mit der Fahrt eines fremden Bootes '
        'rechnet, ist nicht dein Plan. Trage dein eigenes unter '
        'Einstellungen ein.',
    'For en sejlbåd kan du søge den i registret — omkring 130 både, man '
        'møder i danske og nordiske havne. Så udfyldes længde og fart af '
        'fabrikantens mål.':
        'Ein Segelboot kannst du im Register suchen — rund 130 Boote, wie '
        'man sie in dänischen und nordischen Häfen antrifft. Länge und '
        'Fahrt kommen dann aus den Angaben der Werft.',
    'For en motorbåd spørger vi om marchfart, skrogtype og forbrug. '
        'Skroget afgør, hvor meget søen tager af farten: en planende båd '
        'taber mest, fordi den må ned i fortrængning i en stejl modsø.':
        'Bei einem Motorboot fragen wir nach Marschfahrt, Rumpfform und '
        'Verbrauch. Der Rumpf entscheidet, wie viel der Seegang von der '
        'Fahrt nimmt: Ein Gleiter verliert am meisten, weil er in steiler '
        'Gegensee zurück in Verdrängerfahrt muss.',
    'Fart for halvvind i 10 knobs vind':
        'Fahrt bei halbem Wind und 10 Knoten',
    'Ét tal, der skalerer et polardiagram op eller ned til din båd.':
        'Eine einzige Zahl, die ein Polardiagramm auf dein Boot hoch- oder '
        'herunterskaliert.',
    'Et rigtigt polardiagram er en måling af netop din båd med netop '
        'dine sejl. Det har de færreste liggende. Så vi spørger om ét tal, '
        'enhver sejler kender — farten med vinden ind fra siden i en jævn '
        'brise — og skalerer en almindelig krydsers diagram, så det rammer '
        'dit tal.':
        'Ein echtes Polardiagramm ist eine Vermessung genau deines Bootes '
        'mit genau deinen Segeln. Das hat kaum jemand in der Schublade '
        'liegen. Also fragen wir nach der einen Zahl, die jeder Segler '
        'kennt — der Fahrt mit dem Wind von der Seite bei mäßiger Brise — '
        'und skalieren das Diagramm eines gewöhnlichen Fahrtenkreuzers so, '
        'dass es deine Zahl trifft.',
    'Vælger du din båd i registret, regnes tallet af sejlareal, '
        'deplacement og vandlinje. Det er et kvalificeret skøn, ikke en '
        'måling, og du kan altid rette det.':
        'Wählst du dein Boot im Register, wird die Zahl aus Segelfläche, '
        'Verdrängung und Wasserlinie errechnet. Das ist eine begründete '
        'Schätzung, keine Messung, und du kannst sie jederzeit ändern.',
    'Ligger kursen tættere på vinden, end båden kan sejle, regner '
        'planen med, at du krydser: fremdriften mod målet, ikke farten '
        'gennem vandet.':
        'Liegt der Kurs höher am Wind, als das Boot segeln kann, rechnet '
        'der Plan damit, dass du kreuzt: mit dem Vorankommen zum Ziel, '
        'nicht mit der Fahrt durchs Wasser.',
    'Komfortgrænser':
        'Komfortgrenzen',
    'Over dem markeres timerne — det er dine grænser, ikke bådens.':
        'Darüber werden die Stunden markiert — es sind deine Grenzen, nicht '
        'die des Bootes.',
    'Vind og bølger over grænsen giver skærpede timer, og et stykke '
        'over dem frarådede. Det handler om, hvad du og besætningen kan '
        'holde til, ikke om hvad båden kan bære.':
        'Wind und Wellen über der Grenze machen Stunden anspruchsvoll, ein '
        'gutes Stück darüber wird abgeraten. Es geht darum, was du und die '
        'Crew aushalten, nicht darum, was das Boot trägt.',
    'Bølgehøjden vejes efter, hvor søen kommer fra. Modsø tæller '
        'hårdere end tværsø, og medsø mildest — det er dét, man mærker.':
        'Die Wellenhöhe wird danach gewichtet, woher die See kommt. '
        'Gegensee zählt härter als querlaufende See, mitlaufende See am '
        'mildesten — genau so fühlt es sich an.',
    'Grænserne bruges også til at afgøre, om du bliver blæst inde på '
        'destinationen. Sætter du dem urealistisk højt, forsvinder den '
        'advarsel.':
        'Die Grenzen entscheiden auch darüber, ob du am Ziel vom Wind '
        'festgesetzt wirst. Setzt du sie unrealistisch hoch, verschwindet '
        'diese Warnung.',
    'Tid og vejr':
        'Zeit und Wetter',
    'Sejldøgn':
        'Etmal',
    'Sluttidspunktet er, hvornår du vil ligge fortøjet — ikke afgå.':
        'Die Endzeit ist, wann du festgemacht liegen willst — nicht, wann '
        'du ablegst.',
    'Siger du 07–20, betyder det ikke "afgå senest kl. 20". Det '
        'betyder: ligge fortøjet kl. 20. Rækker turen ikke inden for '
        'døgnet, deler Sejlplan den og finder en havn undervejs at '
        'overnatte i.':
        'Sagst du 07–20 Uhr, heißt das nicht „spätestens um 20 Uhr '
        'ablegen“. Es heißt: um 20 Uhr festgemacht liegen. Reicht der Törn '
        'nicht innerhalb des Etmals, teilt Segelplan ihn und sucht einen '
        'Hafen unterwegs zum Übernachten.',
    'Derfor kan planen finde på at lægge til i en havn midt på dagen. '
        'Det er med vilje: er næste stræk for langt til at nås inden '
        'lukketid, og er der ingen havn imellem, ender man i mørke.':
        'Deshalb kann der Plan mitten am Tag einen Hafen anlaufen. Das ist '
        'Absicht: Ist die nächste Etappe zu lang, um sie noch rechtzeitig '
        'zu schaffen, und liegt kein Hafen dazwischen, endet man im '
        'Dunkeln.',
    'Vil du hele vejen i ét stræk, så slå mørkesejlads til under '
        'Indstillinger. Så lægges der ingen overnatninger ind, og '
        'mørketimerne tælles for sig.':
        'Willst du den ganzen Weg in einem Rutsch, dann schalte Nachtfahrt '
        'unter Einstellungen ein. Dann werden keine Übernachtungen '
        'eingelegt, und die Dunkelstunden werden gesondert gezählt.',
    'Afgangstiderne':
        'Die Abfahrtszeiten',
    'Alle de afgange, der giver noget forskelligt. Du vælger.':
        'Alle Abfahrten, die etwas anderes ergeben. Du wählst.',
    'Vi regner hver afgangstime igennem i dit vindue og viser dem, der '
        'ender forskelligt — forskellig ankomst, forskellige havne '
        'undervejs eller forskellige forhold. To afgange en time fra '
        'hinanden, der giver præcis det samme, står kun én gang.':
        'Wir rechnen jede Abfahrtsstunde in deinem Zeitfenster durch und '
        'zeigen die, die unterschiedlich enden — andere Ankunft, andere '
        'Häfen unterwegs oder andere Bedingungen. Zwei Abfahrten eine '
        'Stunde auseinander, die genau dasselbe ergeben, stehen nur einmal '
        'da.',
    'Hver dag, du overhovedet kan sejle, er med. Ellers kunne en hel '
        'dag forsvinde, fordi en anden havde bedre vejr, og så vidste du '
        'ikke, at muligheden fandtes.':
        'Jeder Tag, an dem du überhaupt segeln kannst, ist dabei. Sonst '
        'könnte ein ganzer Tag verschwinden, weil ein anderer besseres '
        'Wetter hatte — und dann wüsstest du nicht, dass es die Möglichkeit '
        'gab.',
    'Rækkefølgen er vores anbefaling — vi vægter frarådede timer '
        'tungest, så korte passager, og til sidst hvornår du er hjemme. Det '
        'er en anbefaling, ikke en afgørelse.':
        'Die Reihenfolge ist unsere Empfehlung — am schwersten wiegen '
        'abgeratene Stunden, dann kurze Passagen und zuletzt, wann du zu '
        'Hause bist. Eine Empfehlung, keine Entscheidung.',
    'Strøm':
        'Strom',
    'Farten er over grunden. Strømmen er regnet med.':
        'Die Fahrt ist über Grund. Der Strom ist eingerechnet.',
    'Farten i planen er over grunden — dét, der flytter båden — ikke '
        'gennem vandet. Strømmen langs kursen lægges til eller trækkes fra, '
        'og står i søjlen Strøm: grøn med, rød imod.':
        'Die Fahrt im Plan ist über Grund — das, was das Boot versetzt — '
        'nicht durchs Wasser. Der Strom längs des Kurses wird addiert oder '
        'abgezogen und steht in der Spalte Strom: grün mit, rot gegen.',
    'Står strømmen tværs, tæller den ikke på farten. Til gengæld sætter '
        'den af til siden, og det skal styres op — planen regner ikke '
        'afdriften ud for dig.':
        'Steht der Strom quer, zählt er nicht auf die Fahrt. Dafür versetzt '
        'er zur Seite, und das muss vorgehalten werden — den Versatz '
        'rechnet der Plan nicht für dich aus.',
    'Tallene kommer fra en global havmodel, og den opløser ikke de '
        'danske bælter helt. I Storebælt og Grønsund kan der løbe to-tre '
        'knob, hvor modellen viser under én. Brug den som en retning, og '
        'slå strømtabellen op, når det gælder en smal passage.':
        'Die Zahlen stammen aus einem globalen Meeresmodell, und das löst '
        'die dänischen Belte nicht vollständig auf. Im Großen Belt und im '
        'Grønsund können zwei bis drei Knoten laufen, wo das Modell unter '
        'einem zeigt. Nimm es als Richtung und schlage die Stromtabelle '
        'nach, wenn es um eine enge Passage geht.',
    'Hvor langt frem vi kan se':
        'Wie weit wir vorausschauen können',
    'Ti døgn. Bølgerne er loftet, ikke vinden.':
        'Zehn Tage. Die Wellen sind die Grenze, nicht der Wind.',
    'Vinden rækker fjorten døgn frem, bølgerne ti. En sejlplan uden '
        'søen er en halv plan, så ti døgn er grænsen.':
        'Der Wind reicht vierzehn Tage voraus, die Wellen zehn. Ein '
        'Segelplan ohne den Seegang ist ein halber Plan, also sind zehn '
        'Tage die Grenze.',
    'De første tre-fire døgn holder ret godt. Derefter er det '
        'retningen, der overlever, ikke timerne — og det står i planen, når '
        'turen slutter fem døgn eller mere ude.':
        'Die ersten drei bis vier Tage halten recht gut. Danach überlebt '
        'die Richtung, nicht die einzelne Stunde — und das steht im Plan, '
        'wenn der Törn fünf Tage oder mehr voraus endet.',
    'Rækker prognosen ikke hele vejen, siger planen, hvor langt du når, '
        'i stedet for at påstå en ankomst. Læg turen tidligere, eller '
        'planlæg den sidste del om nogle dage.':
        'Reicht die Vorhersage nicht den ganzen Weg, sagt der Plan, wie '
        'weit du kommst, statt eine Ankunft zu behaupten. Lege den Törn '
        'früher, oder plane das letzte Stück in ein paar Tagen.',
    'Blæst inde':
        'Vom Wind festgesetzt',
    'Om du kommer væk igen — ikke kun om du kommer derhen.':
        'Ob du wieder wegkommst — nicht nur, ob du hinkommst.',
    'Man kigger på vejret frem til man er fremme, og ikke længere. Så '
        'sejler man til Marstal i det pæneste vejr og opdager i havnen, at '
        'det blæser femogtyve knob i tre døgn.':
        'Man schaut aufs Wetter, bis man da ist, und keine Stunde länger. '
        'So segelt man bei schönstem Wetter nach Marstal und stellt im '
        'Hafen fest, dass es drei Tage lang fünfundzwanzig Knoten weht.',
    'Sejlplan kigger videre for dig. Fra ankomsten og til prognosen '
        'slipper op tælles det efter, om der er et sejlbart døgn tilbage. '
        'Er der to eller flere døgn i træk uden, står det i planen — med '
        'hvornår vinduet åbner igen.':
        'Segelplan schaut für dich weiter. Von der Ankunft an bis zum Ende '
        'der Vorhersage zählen wir nach, ob noch ein segelbares Etmal übrig '
        'ist. Sind es zwei oder mehr Tage am Stück ohne, steht es im Plan — '
        'mitsamt dem Zeitpunkt, an dem sich das Fenster wieder öffnet.',
    'Holder det ikke op, før prognosen gør, får du det at vide som dét: '
        'vi ved ikke hvornår. Så er hjemturen en tur for sig.':
        'Hört es nicht auf, bevor die Vorhersage aufhört, bekommst du genau '
        'das gesagt: Wir wissen nicht, wann. Dann ist der Rückweg ein Törn '
        'für sich.',
    'Sejlplanen':
        'Der Segelplan',
    'Stræk for stræk':
        'Abschnitt für Abschnitt',
    'Delt op dér, hvor kursen skifter — ikke hvor du satte et kryds.':
        'Dort geteilt, wo der Kurs wechselt — nicht dort, wo du ein Kreuz '
        'gesetzt hast.',
    'Sætter du Køge og Præstø ind, er det ét ben. Men det sejles mod '
        'øst, så mod syd og til sidst mod vest, og en plan, der giver én '
        'kurs for det hele, passer ingen af stederne.':
        'Setzt du Køge und Præstø ein, ist das eine Etappe. Aber sie wird '
        'nach Osten gesegelt, dann nach Süden und zuletzt nach Westen, und '
        'ein Plan, der einen einzigen Kurs für das Ganze angibt, passt an '
        'keiner der Stellen.',
    'Derfor deles turen dér, hvor du faktisk skal dreje. Hvert stræk '
        'har sin kurs, sin vind, sin sø og sin sejlføring — og de gælder '
        'præcis dér, hvor du styrer den kurs.':
        'Deshalb wird der Törn dort geteilt, wo du tatsächlich abdrehen '
        'musst. Jeder Abschnitt hat seinen Kurs, seinen Wind, seine See und '
        'seine Segelführung — und die gelten genau dort, wo du diesen Kurs '
        'steuerst.',
    'Bliver et stræk brudt af en overnatning, står det i teksten. '
        'Timerne ved kaj tæller ikke med.':
        'Wird ein Abschnitt von einer Übernachtung unterbrochen, steht das '
        'im Text. Die Stunden am Steg zählen nicht mit.',
    'Nøgletallene':
        'Die Kennzahlen',
    'Under vejs er den rigtige tid fra kaj til kaj.':
        'Unterwegs ist die echte Zeit von Leine los bis fest.',
    '"Under vejs" er tiden fra du kaster los, til du ligger fortøjet, '
        'lagt sammen for alle døgnene. Havnetimerne tæller ikke med.':
        '„Unterwegs“ ist die Zeit vom Ablegen bis zum Festmachen, über alle '
        'Tage zusammengezählt. Die Stunden im Hafen zählen nicht mit.',
    'Gennemsnitsfarten er distancen delt med den tid. Distance, tid og '
        'fart passer sammen — du kan regne efter.':
        'Die Durchschnittsfahrt ist die Distanz geteilt durch diese Zeit. '
        'Distanz, Zeit und Fahrt passen zusammen — du kannst nachrechnen.',
    'Frarådede timer er dem, der ligger et stykke over dine grænser. Er '
        'der nogen, skal du tage stilling til dem, før du kaster los.':
        'Abgeratene Stunden sind die, die ein gutes Stück über deinen '
        'Grenzen liegen. Gibt es welche, musst du dazu Stellung nehmen, '
        'bevor du ablegst.',
    'Time for time':
        'Stunde für Stunde',
    'Grøn er god, gul er skærpet, rød frarådes — efter dine grænser.':
        'Grün ist gut, Gelb ist anspruchsvoll, Rot wird abgeraten — nach '
        'deinen Grenzen.',
    'Hver række er én sejltime på det sted, du er nået til: vinden, '
        'hvor den kommer fra, bølgerne, farten og sejlføringen.':
        'Jede Zeile ist eine Segelstunde an der Stelle, bis zu der du '
        'gekommen bist: der Wind, woher er kommt, die Wellen, die Fahrt und '
        'die Segelführung.',
    'Farven kommer af dine egne komfortgrænser. Grøn er inden for dem, '
        'gul er lidt over, rød er et stykke over.':
        'Die Farbe kommt von deinen eigenen Komfortgrenzen. Grün liegt '
        'innerhalb, Gelb etwas darüber, Rot ein gutes Stück darüber.',
    'Står der "motor", er der for lidt vind til at sejle — under tre '
        'knobs fart tændes motoren i beregningen, hvis du har slået det '
        'til.':
        'Steht dort „Motor“, ist zu wenig Wind zum Segeln — unter drei '
        'Knoten Fahrt wird der Motor in der Berechnung angeworfen, wenn du '
        'das eingeschaltet hast.',
    'Havne undervejs':
        'Häfen unterwegs',
    'Steder du kan søge ind, hvis vejret skifter.':
        'Orte, die du anlaufen kannst, wenn das Wetter umschlägt.',
    'Listen er de havne, der ligger tæt nok på ruten til at være et '
        'rimeligt sted at gå ind — op til seks sømil fra vejen. Klik på en '
        'for at lægge den ind som mellemstop.':
        'Die Liste zeigt die Häfen, die nah genug an der Route liegen, um '
        'ein vernünftiges Ziel zum Einlaufen zu sein — bis zu sechs '
        'Seemeilen vom Weg. Klicke einen an, um ihn als Zwischenstopp '
        'einzufügen.',
    'Vi tjekker, at man kan sejle lige ind til dem fra ruten, så et '
        'forslag aldrig kræver, at du sejler uden om en ø.':
        'Wir prüfen, dass man von der Route aus geradewegs hineinlaufen '
        'kann, damit ein Vorschlag nie verlangt, dass du um eine Insel '
        'herumsegelst.',
    'Har havnen en side i havnelods.dk, er der et lille ikon ved siden '
        'af. Dér står pladser, priser, faciliteter og indsejling. Mangler '
        'ikonet, kender vi ikke havnens side — så er det bedre at lade være '
        'end at sende dig det forkerte sted hen.':
        'Hat der Hafen eine Seite bei havnelods.dk, steht ein kleines '
        'Symbol daneben. Dort stehen Liegeplätze, Preise, Einrichtungen und '
        'die Einfahrt. Fehlt das Symbol, kennen wir die Seite des Hafens '
        'nicht — dann ist es besser, es zu lassen, als dich an die falsche '
        'Stelle zu schicken.',
    'Er der plads i havnen?':
        'Ist im Hafen noch Platz?',
    'Det eneste, ingen model kan svare på. Kun dem, der ligger der.':
        'Das Einzige, was kein Modell beantworten kann. Nur die, die dort '
        'liegen.',
    'Vejret kommer fra en model og afstanden fra et søkort. Om der er '
        'en plads tilbage ved ydermolen klokken fire, ved kun den, der '
        'ligger der klokken to.':
        'Das Wetter kommt aus einem Modell und die Entfernung aus einer '
        'Seekarte. Ob um vier Uhr noch ein Platz an der Außenmole frei ist, '
        'weiß nur, wer um zwei dort liegt.',
    'Derfor kan man melde: god plads, få pladser, eller fuld. Det tager '
        'to sekunder, det er anonymt, og der gemmes kun havnen, svaret og '
        'hvornår. Der er ikke noget at skrive — og dermed heller ikke et '
        'sted, hvor nogen kan skrive noget til nogen.':
        'Deshalb kann man melden: viel Platz, wenige Plätze oder voll. Es '
        'dauert zwei Sekunden, es ist anonym, und gespeichert werden nur '
        'der Hafen, die Antwort und der Zeitpunkt. Es gibt nichts zu '
        'schreiben — und damit auch keine Stelle, an der jemand jemandem '
        'etwas schreiben kann.',
    'Alderen står altid med, for den er halvdelen af oplysningen. '
        '"Fuld" for tre timer siden er noget andet end "fuld" i går aftes. '
        'Efter halvandet døgn forsvinder meldingen af sig selv.':
        'Das Alter steht immer dabei, denn es ist die Hälfte der Auskunft. '
        '„Voll“ vor drei Stunden ist etwas anderes als „voll“ gestern '
        'Abend. Nach anderthalb Tagen verschwindet die Meldung von selbst.',
    'Ligger du i en havn, så meld. Det koster dig ingenting og er det '
        'eneste, den næste ikke kan finde ud af på egen hånd.':
        'Liegst du in einem Hafen, dann melde. Es kostet dich nichts und '
        'ist das Einzige, was der Nächste nicht selbst herausfinden kann.',
    'Undervejs':
        'Unterwegs',
    'Undervejs: foran eller bagud?':
        'Unterwegs: voraus oder zurück?',
    'Telefonens position mod planens — hvornår er du så fremme?':
        'Die Position des Telefons gegen die des Plans — wann bist du also '
        'da?',
    'Planen bliver lagt i havnen. Undervejs er spørgsmålet et andet: er '
        'jeg foran eller bagud, og hvornår er jeg så fremme i '
        'virkeligheden. Tryk "Jeg er undervejs" i sejlplanen.':
        'Der Plan wird im Hafen gemacht. Unterwegs ist die Frage eine '
        'andere: Bin ich voraus oder zurück, und wann bin ich in '
        'Wirklichkeit da? Drücke „Ich bin unterwegs“ im Segelplan.',
    'Vi finder det punkt på ruten, du er tættest på, og slår op i '
        'planens eget spor, hvor langt du skulle have været på det '
        'klokkeslæt. Ligger du mere end tre sømil fra ruten, siger vi '
        'ingenting — så betyder et forspring heller ingenting.':
        'Wir suchen den Punkt auf der Route, dem du am nächsten bist, und '
        'schlagen in der Spur des Plans nach, wie weit du zu dieser Uhrzeit '
        'hättest sein sollen. Liegst du mehr als drei Seemeilen von der '
        'Route entfernt, sagen wir nichts — dann bedeutet ein Vorsprung '
        'auch nichts.',
    'Positionen bliver på din telefon og i den ene beregning. Den '
        'gemmes ikke, og ingen andre kan se den. At vise sig for andre er '
        'en anden funktion, man selv skal tænde.':
        'Die Position bleibt auf deinem Telefon und in dieser einen '
        'Berechnung. Sie wird nicht gespeichert, und niemand sonst kann sie '
        'sehen. Sich anderen zu zeigen, ist eine andere Funktion, die du '
        'selbst einschalten musst.',
    'På iPhone virker positionen kun, mens skærmen er tændt og Sejlplan '
        'er fremme. Låser du telefonen, holder den op. Det er iOS, der '
        'bestemmer det.':
        'Auf dem iPhone funktioniert die Position nur, solange der '
        'Bildschirm an und Segelplan im Vordergrund ist. Sperrst du das '
        'Telefon, hört sie auf. Das bestimmt iOS.',
    'Se andre både':
        'Andere Boote sehen',
    'Usynlig til du selv tænder — og du ser kun dem, der også har.':
        'Unsichtbar, bis du selbst einschaltest — und du siehst nur die, '
        'die es auch getan haben.',
    'Tryk "Vis min båd for andre" og vælg et bådnavn. Så kan andre, der '
        'også er synlige, se hvor du er, og du kan se dem. Kun jer, der har '
        'slået det til.':
        'Drücke „Mein Boot für andere sichtbar machen“ und wähle einen '
        'Bootsnamen. Dann können andere, die auch sichtbar sind, sehen, wo '
        'du bist, und du siehst sie. Nur ihr, die es eingeschaltet habt.',
    'Du ser kun andre, mens du selv er synlig. Ingen kan ligge og kigge '
        'uden at være der selv. Slukker du, forsvinder du fra deres kort og '
        'de fra dit i samme øjeblik — og din position bliver slettet, ikke '
        'skjult.':
        'Du siehst andere nur, solange du selbst sichtbar bist. Niemand '
        'kann zuschauen, ohne selbst dabei zu sein. Schaltest du aus, '
        'verschwindest du im selben Augenblick von ihrer Karte und sie von '
        'deiner — und deine Position wird gelöscht, nicht versteckt.',
    'Positionen udløber af sig selv efter en halv time uden opdatering. '
        'Der gemmes ingen historik: hver ny position skriver den forrige '
        'over, så ingen kan slå op, hvor du var i går.':
        'Die Position läuft nach einer halben Stunde ohne Aktualisierung '
        'von selbst ab. Es wird kein Verlauf gespeichert: Jede neue '
        'Position überschreibt die vorige, sodass niemand nachschlagen '
        'kann, wo du gestern warst.',
    'Skriv bådens navn, ikke dit eget — det er dét, de andre ser. Ser '
        'du ingen både, er der ingen inden for tres sømil, der har tændt.':
        'Schreibe den Namen des Bootes, nicht deinen eigenen — das ist es, '
        'was die anderen sehen. Siehst du keine Boote, hat innerhalb von '
        'sechzig Seemeilen niemand eingeschaltet.',
    'Beskeder mellem både':
        'Nachrichten zwischen Booten',
    'Tryk på en båd på kortet og skriv. Kun mellem synlige både.':
        'Tippe ein Boot auf der Karte an und schreibe. Nur zwischen '
        'sichtbaren Booten.',
    'Det er ikke en indbakke med fremmede og ikke en opslagstavle — det '
        'er en samtale mellem to, der ligger i det samme farvand lige nu, '
        'og som begge har valgt at være synlige.':
        'Es ist kein Posteingang voller Fremder und kein schwarzes Brett — '
        'es ist ein Gespräch zwischen zweien, die gerade im selben Revier '
        'liegen und die beide sichtbar sein wollten.',
    'Har nogen skrevet, står der en prik på båden på kortet og et tal i '
        'panelet. Beskeder forsvinder efter et døgn.':
        'Hat jemand geschrieben, steht ein Punkt am Boot auf der Karte und '
        'eine Zahl im Panel. Nachrichten verschwinden nach einem Tag.',
    'Bloker sidder i samtalens menu og virker begge veje med det samme: '
        'I kan hverken skrive til hinanden eller se hinanden på kortet. '
        'Anmeld sidder på selve beskeden — anmelder du en, gemmer vi '
        'teksten, for ellers ville den dø efter et døgn, og så stod ord mod '
        'ord.':
        'Blockieren steht im Menü des Gesprächs und wirkt sofort in beide '
        'Richtungen: Ihr könnt einander weder schreiben noch auf der Karte '
        'sehen. Melden steht an der Nachricht selbst — meldest du eine, '
        'speichern wir den Text, denn sonst wäre er nach einem Tag weg, und '
        'dann stünde Aussage gegen Aussage.',
    'Skriver du tre gange til en, der ikke svarer, må du vente. Det er '
        'med vilje.':
        'Schreibst du dreimal an jemanden, der nicht antwortet, musst du '
        'warten. Das ist Absicht.',
    'Gem og tag med':
        'Speichern und mitnehmen',
    'Vejrvagt':
        'Wetterwache',
    'Sig til, når vejret er der — også om fjorten dage.':
        'Sag Bescheid, wenn das Wetter da ist — auch in vierzehn Tagen.',
    'Skal turen først gå om tre uger, er der ingen prognose at kigge i '
        'endnu, og så skal man ikke sidde og trykke opdater hver dag. Læg '
        'en vagt på ruten, og få én mail, når der er et vindue.':
        'Soll der Törn erst in drei Wochen losgehen, gibt es noch keine '
        'Vorhersage, in die man schauen könnte, und dann soll man nicht '
        'jeden Tag auf Aktualisieren drücken. Lege eine Wache auf die Route '
        'und bekomme eine einzige Mail, wenn sich ein Fenster auftut.',
    'Vagten venter, til prognosen når frem til dine datoer, og regner '
        'så turen igennem med din egen båd og dine egne grænser. Vi skriver '
        'kun, hvis du også kan komme hjem igen — er du blæst inde i tre '
        'døgn på destinationen, er det ikke en gevinst.':
        'Die Wache wartet, bis die Vorhersage deine Daten erreicht, und '
        'rechnet den Törn dann mit deinem eigenen Boot und deinen eigenen '
        'Grenzen durch. Wir schreiben nur, wenn du auch wieder nach Hause '
        'kommst — liegst du am Ziel drei Tage fest, ist das kein Gewinn.',
    'Én vagt giver én besked. Ikke en strøm af mails, hver gang '
        'modellen flytter sig en halv knob. Kommer beskeden, er vagten '
        'brugt, og du lægger en ny.':
        'Eine Wache gibt eine Nachricht. Keinen Strom von Mails, jedes Mal '
        'wenn das Modell sich um einen halben Knoten verschiebt. Kommt die '
        'Nachricht, ist die Wache verbraucht, und du legst eine neue.',
    'Vi skriver aldrig til en adresse, der ikke selv har bekræftet den, '
        'og hver mail bærer sit eget link til at stoppe.':
        'Wir schreiben nie an eine Adresse, die sie nicht selbst bestätigt '
        'hat, und jede Mail trägt ihren eigenen Link zum Abbestellen.',
    'Sprog':
        'Sprache',
    'Dansk og tysk. Flaget i toppen skifter.':
        'Dänisch und Deutsch. Die Flagge oben schaltet um.',
    'Flaget øverst på siden skifter sprog — tryk på det og vælg. Det '
        'står også under Indstillinger. Siden hentes forfra på det nye '
        'sprog.':
        'Die Flagge oben auf der Seite wechselt die Sprache — tippe sie an '
        'und wähle. Sie steht auch unter Einstellungen. Die Seite wird in '
        'der neuen Sprache neu geladen.',
    'Første besøg følger browserens eget førstevalg af sprog — er det ikke '
        'dansk eller tysk, får du dansk. Derefter vinder dit valg, og det '
        'gemmes hos dig selv, så det holder, også når vi lægger en ny udgave '
        'af Sejlplan ud.':
        'Beim ersten Besuch folgen wir der ersten Sprachwahl des Browsers — '
        'ist das weder Dänisch noch Deutsch, bekommst du Dänisch. Danach '
        'gewinnt deine Wahl, und sie wird bei dir selbst gespeichert, sodass '
        'sie hält, auch wenn wir eine neue Ausgabe von Segelplan ausrollen.',
    'Er en tekst ikke oversat endnu, står den på dansk. Det er med '
        'vilje: en halvt oversat flade er brugbar, en flade med huller i er '
        'ikke.':
        'Ist ein Text noch nicht übersetzt, steht er auf Dänisch. Das ist '
        'Absicht: Eine halb übersetzte Oberfläche ist brauchbar, eine mit '
        'Löchern nicht.',
    'Mine ruter':
        'Meine Routen',
    'Gem turen, og hent den frem igen, når prognosen når så langt.':
        'Speichere den Törn und hole ihn wieder hervor, wenn die Vorhersage '
        'so weit reicht.',
    'En sommertur på fjorten dage kan ikke planlægges på én gang — '
        'prognosen rækker ti døgn. Men ruten kan lægges nu: afstande, ben, '
        'havne undervejs og hvor mange sejldøgn den kræver, regnes uden et '
        'gram vejr.':
        'Ein Sommertörn über vierzehn Tage lässt sich nicht auf einmal '
        'planen — die Vorhersage reicht zehn Tage. Aber die Route lässt '
        'sich jetzt legen: Entfernungen, Etappen, Häfen unterwegs und wie '
        'viele Etmale sie kostet, werden ohne ein Gramm Wetter gerechnet.',
    'Gem den, og hent den frem igen, efterhånden som prognosen ruller '
        'frem over din rute. Ét tryk på Gem opdaterer den, du arbejder i; '
        'vil du have en kopi, er der Gem som ny.':
        'Speichere sie und hole sie wieder hervor, während die Vorhersage '
        'über deine Route vorrückt. Ein Druck auf Speichern aktualisiert '
        'die, in der du arbeitest; willst du eine Kopie, gibt es Als neue '
        'speichern.',
    'Ruterne ligger i din browser og i din session. De overlever, at vi '
        'lægger en ny version af Sejlplan ud.':
        'Die Routen liegen in deinem Browser und in deiner Sitzung. Sie '
        'überleben es, wenn wir eine neue Version von Segelplan ausrollen.',
    'Appen og uden dækning':
        'Die App und ohne Empfang',
    'Den seneste sejlplan kan læses uden forbindelse.':
        'Der letzte Segelplan lässt sich ohne Verbindung lesen.',
    'Læg Sejlplan på hjemmeskærmen under Indstillinger, så åbner den i '
        'sit eget vindue uden browserlinje. På iPhone gør du det selv: åbn '
        'siden i Safari, tryk Del, vælg "Føj til hjemmeskærm".':
        'Lege Segelplan unter Einstellungen auf den Startbildschirm, dann '
        'öffnet er sich in einem eigenen Fenster ohne Browserzeile. Auf dem '
        'iPhone machst du das selbst: Seite in Safari öffnen, auf Teilen '
        'tippen, „Zum Home-Bildschirm“ wählen.',
    'Du kan ikke lægge en rute uden dækning — beregningen sker på '
        'serveren. Men hver gang du åbner en sejlplan, lægges den ned i '
        'telefonen som et dokument, der kan stå alene. Går dækningen, '
        'kommer den frem: overblik, advarsler, dag for dag, stræk for stræk '
        'og hele timetabellen.':
        'Ohne Empfang kannst du keine Route legen — gerechnet wird auf dem '
        'Server. Aber jedes Mal, wenn du einen Segelplan öffnest, wird er '
        'als eigenständiges Dokument ins Telefon gelegt. Fällt der Empfang '
        'aus, kommt er hervor: Überblick, Warnungen, Tag für Tag, Abschnitt '
        'für Abschnitt und die ganze Stundentabelle.',
    'De kortfliser, du har set på, gemmes også, så kortet kan vise det '
        'farvand, du lige har kigget på.':
        'Die Kartenkacheln, die du angesehen hast, werden ebenfalls '
        'gespeichert, sodass die Karte das Revier zeigen kann, das du '
        'gerade betrachtet hast.',
    'GPX til kortplotteren':
        'GPX für den Kartenplotter',
    'Hele havvejen med, ikke bare dine punkter.':
        'Der ganze Seeweg ist dabei, nicht nur deine Punkte.',
    'Under dele-ikonet ligger Hent GPX til kortplotter. Filen '
        'indeholder dine egne punkter som waypoints, hele havvejen som rute '
        'med knækpunkterne uden om land, og den samme vej som spor.':
        'Unter dem Teilen-Symbol liegt GPX für Kartenplotter laden. Die '
        'Datei enthält deine eigenen Punkte als Wegpunkte, den ganzen '
        'Seeweg als Route mit den Knickpunkten um das Land herum und '
        'denselben Weg als Track.',
    'Både rute og spor er med, fordi der findes plottere, der kun læser '
        'det ene.':
        'Route und Track sind beide dabei, weil es Plotter gibt, die nur '
        'das eine lesen.',
    'Samme sted kan du kopiere et delelink. Det åbner ruten hos den, du '
        'sender det til — også hvis de aldrig har brugt Sejlplan før.':
        'An derselben Stelle kannst du einen Freigabe-Link kopieren. Er '
        'öffnet die Route bei dem, dem du ihn schickst — auch wenn er '
        'Segelplan noch nie benutzt hat.',
    'Skippervurdering':
        'Skipper-Einschätzung',
    'En erfaren sejlkonsulent læser planen igennem.':
        'Ein erfahrener Segelberater liest den Plan durch.',
    'Vurderingen gennemgår ruten ben for ben og kommenterer det, '
        'tallene ikke siger: hvornår du bør reve, hvad der er værd at holde '
        'øje med, og om afgangen er den rigtige.':
        'Die Einschätzung geht die Route Etappe für Etappe durch und '
        'kommentiert, was die Zahlen nicht sagen: wann du reffen solltest, '
        'worauf zu achten ist und ob die Abfahrt die richtige ist.',
    'Den skrives af en sprogmodel ud fra din plan. Den er god til at få '
        'øje på det, der ikke hænger sammen — men den erstatter ikke din '
        'egen vurdering.':
        'Sie wird von einem Sprachmodell aus deinem Plan geschrieben. Es '
        'hat ein gutes Auge für das, was nicht zusammenpasst — aber es '
        'ersetzt nicht deine eigene Beurteilung.',
    'Sejlplan er et planlægningsværktøj. Prognoser er prognoser, og en '
        'landmaske er ikke et søkort. Planen erstatter ikke søkort, '
        'farvandsudsigt, efterretninger for søfarende eller almindelig '
        'sømandskab. Ansvaret for sejladsen er skipperens.':
        'Segelplan ist ein Planungswerkzeug. Vorhersagen sind Vorhersagen, '
        'und eine Landmaske ist keine Seekarte. Der Plan ersetzt weder '
        'Seekarte noch Seewetterbericht, weder Nachrichten für Seefahrer '
        'noch gewöhnliche Seemannschaft. Die Verantwortung für die Fahrt '
        'trägt der Skipper.',

    # ── Hvem er der lige nu ────────────────────────────────────────
    'Hvem er der lige nu':
        'Wer ist gerade da',
    'Listen over både, delt op efter havn. Nemmere end kortet.':
        'Die Liste der Boote, nach Häfen geteilt. Einfacher als die Karte.',
    'Kortet er godt til at vise, hvor nogen er. Det er dårligt til at svare '
        'på, hvem der overhovedet er der: en båd er en lille trekant, og '
        'zoomer man ud så hele farvandet er med, kan man ikke se dem.':
        'Die Karte ist gut darin zu zeigen, wo jemand ist. Sie ist schlecht '
        'darin zu beantworten, wer überhaupt da ist: Ein Boot ist ein kleines '
        'Dreieck, und zoomt man so weit heraus, dass das ganze Revier drauf '
        'ist, sieht man sie nicht mehr.',
    'Tryk "Se hvem der er i nærheden". De både, der ligger i en havn, står '
        'under havnens navn — for det er dét, man vil vide, når man leder '
        'efter nogen at drikke kaffe med. Resten står under Undervejs med '
        'afstand og pejling.':
        'Tippe auf „Sieh, wer in der Nähe ist“. Die Boote, die in einem Hafen '
        'liegen, stehen unter dem Namen des Hafens — denn das will man '
        'wissen, wenn man jemanden zum Kaffee sucht. Der Rest steht unter '
        'Unterwegs, mit Entfernung und Peilung.',
    'Havnene på ruten får også et mærke, når der ligger nogen: "3 både her". '
        'Tryk på det, og du er i listen.':
        'Auch die Häfen auf der Route bekommen ein Zeichen, wenn dort jemand '
        'liegt: „3 Boote hier“. Tippe darauf, und du bist in der Liste.',
    'Tryk på en båd for at skrive til den. Du ser kun både, der også har '
        'gjort sig synlige — den regel gælder her som alle andre steder.':
        'Tippe ein Boot an, um ihm zu schreiben. Du siehst nur Boote, die '
        'sich ebenfalls sichtbar gemacht haben — diese Regel gilt hier wie '
        'überall sonst.',
}
