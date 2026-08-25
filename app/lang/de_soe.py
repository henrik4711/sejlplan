"""Sømærker, signaler og sejltrim på tysk.

Nøglen er den danske sætning fra `app/seamanship.py` og `app/trim.py`.

Skrevet med de tyske ord, en tysk sejler bruger: Bullenstander for bomholder,
Patenthalse for en utilsigtet bomvending, Holepunkt for skødevognen,
Einzelgefahrenzeichen for enkeltstående fare, KVR for Søvejsreglerne. Det er
ikke oversættelser af de danske ord — det er de ord, der står i den tyske
lærebog og på det tyske søkort.
"""

WORDS: dict[str, str] = {
    'Sådan læses en fyrkarakter':
        'So liest man eine Feuerkennung',
    'Lanterner om natten':
        'Lichter bei Nacht',
    'Dagsignaler':
        'Tageszeichen',
    'Lydsignaler når I ser hinanden':
        'Schallsignale in Sichtweite',
    'Lydsignaler i nedsat sigtbarhed':
        'Schallsignale bei verminderter Sicht',
    'Nødsignaler':
        'Notsignale',
    'Sømærker og signaler':
        'Seezeichen und Signale',
    'Afmærkningen er IALA A — Danmark, Tyskland, Sverige, Norge og '
        'resten af Europa.':
        'Die Betonnung ist IALA A — Dänemark, Deutschland, Schweden, '
        'Norwegen und der Rest Europas.',
    'En huskeseddel, ikke Søvejsreglerne. Er du i tvivl om en '
        'vigepligt, er det reglerne, der gælder. Og farerne står i '
        'søkortet — dem kender Sejlplan ikke.':
        'Ein Spickzettel, nicht die KVR. Bist du bei einer '
        'Ausweichpflicht im Zweifel, gelten die Regeln. Und die Gefahren '
        'stehen in der Seekarte — die kennt Segelplan nicht.',
    'Hvad betyder det':
        'Was bedeutet das',
    'Sømærker, fyrkarakterer, lanterner og signaler':
        'Seezeichen, Feuerkennungen, Lichter und Signale',
    'Kig efter':
        'Achte auf',
    'Rebning':
        'Reffen',
    'Ved {kn} knob på {sejlføring}. Et udgangspunkt — dine sejl og '
        'deres alder bestemmer resten.':
        'Bei {kn} Knoten {sejlføring}. Ein Ausgangspunkt — deine Segel '
        'und ihr Alter bestimmen den Rest.',
    'Optimér mine sejl':
        'Meine Segel trimmen',
    'Til søs':
        'Auf See',
    'Hvad mærkerne i vandet betyder, og hvad du gør ved dem.':
        'Was die Zeichen im Wasser bedeuten und was du mit ihnen machst.',
    'Afmærkningen er IALA A. Den gælder i Danmark, Tyskland, Sverige, '
        'Norge og resten af Europa. I Nord- og Sydamerika er de røde og '
        'grønne sidemærker byttet om.':
        'Die Betonnung ist IALA A. Sie gilt in Dänemark, Deutschland, '
        'Schweden, Norwegen und im übrigen Europa. In Nord- und '
        'Südamerika sind die roten und grünen Lateralzeichen vertauscht.',
    'Sidemærkerne siger, hvor løbet er: rødt og dåseformet i bagbord, '
        'grønt og spidst i styrbord, når du sejler ind. Ud igen er det '
        'omvendt.':
        'Die Lateralzeichen sagen, wo das Fahrwasser ist: rot und stumpf '
        'an Backbord, grün und spitz an Steuerbord, wenn du einläufst. '
        'Hinaus ist es umgekehrt.',
    'Kardinalmærkerne siger, hvilken side du skal gå på. Keglerne '
        'øverst peger hen mod den side, der er ren: to kegler opad er et '
        'nordmærke, og så skal du nord om. Antallet af blink følger uret '
        '— tre for øst, seks for syd, ni for vest.':
        'Die Kardinalzeichen sagen, auf welcher Seite du vorbeimusst. Die '
        'Kegel oben zeigen zu der Seite, die frei ist: zwei Kegel nach '
        'oben ist eine Nordtonne, also gehst du nördlich vorbei. Die Zahl '
        'der Blitze folgt der Uhr — drei für Ost, sechs für Süd, neun für '
        'West.',
    'Enkeltstående fare er sort med røde bånd og to kugler. Der er '
        'vand hele vejen rundt, men gå ikke tæt på. Sikkert vand er '
        'rød-hvidt stribet med en rød kugle — dér er der vand hele vejen '
        'rundt.':
        'Das Einzelgefahrenzeichen ist schwarz mit roten Bändern und zwei '
        'Bällen. Ringsum ist Wasser, aber geh nicht dicht heran. Sicheres '
        'Fahrwasser ist rot-weiß gestreift mit einem roten Ball — dort '
        'ist ringsum Wasser.',
    'Under bogikonet i toppen ligger tegningerne af dem alle sammen, '
        'med fyrkarakter og huskeregel.':
        'Unter dem Buchsymbol oben liegen die Zeichnungen von allen, mit '
        'Feuerkennung und Eselsbrücke.',
    'Fyr og karakterer':
        'Feuer und Kennungen',
    'Sådan læser du Fl(3)WR.10s — og hvad et sektorfyr fortæller.':
        'So liest du Fl(3)WR.10s — und was ein Sektorenfeuer dir sagt.',
    'Bogstaverne siger, hvordan lyset opfører sig: Fl er blink, Oc er '
        'formørkelse, Iso er lige lang tid tændt og slukket, Q er '
        'hurtigblink. Tallet i parentes er antal blink i gruppen, og '
        'sekundtallet er hele periodens længde.':
        'Die Buchstaben sagen, wie sich das Licht verhält: Fl ist Blitz, '
        'Oc ist unterbrochen, Iso ist gleich lang hell und dunkel, Q ist '
        'Funkelfeuer. Die Zahl in Klammern ist die Anzahl der Blitze in '
        'der Gruppe, und die Sekundenzahl ist die Länge der ganzen '
        'Periode.',
    'Fl(3)WR.10s er altså tre blink, hvidt i én retning og rødt i en '
        'anden, gentaget hvert tiende sekund. Tag tid på perioden med et '
        'ur — det er dét, der skiller to fyr, der ellers ligner hinanden.':
        'Fl(3)WR.10s sind also drei Blitze, weiß in die eine Richtung und '
        'rot in die andere, wiederholt alle zehn Sekunden. Stoppe die '
        'Periode mit der Uhr — das ist es, was zwei Feuer unterscheidet, '
        'die sich sonst ähneln.',
    'Et sektorfyr viser forskellig farve i forskellige retninger. '
        'Hvidt betyder som regel det rene løb. Hvilken side rødt og grønt '
        'dækker, står i søkortet — det er ikke det samme alle steder.':
        'Ein Sektorenfeuer zeigt in verschiedene Richtungen verschiedene '
        'Farben. Weiß bedeutet in der Regel das freie Fahrwasser. Welche '
        'Seite rot und grün abdecken, steht in der Seekarte — das ist '
        'nicht überall gleich.',
    'Lanterner og dagsignaler':
        'Lichter und Tageszeichen',
    'Hvad du ser om natten, og hvad det siger om, hvem der viger.':
        'Was du nachts siehst, und was es darüber sagt, wer ausweicht.',
    'Ser du både rødt og grønt uden hvidt over, er det en sejlbåd, '
        'der kommer lige imod dig. Er der ét hvidt lys over, er det et '
        'motorfartøj. Ser du kun hvidt, ser du den bagfra — og så er det '
        'dig, der indhenter og skal holde klar.':
        'Siehst du Rot und Grün ohne Weiß darüber, ist es ein Segelboot, '
        'das genau auf dich zukommt. Ist ein weißes Licht darüber, ist es '
        'ein Maschinenfahrzeug. Siehst du nur Weiß, siehst du es von '
        'achtern — dann bist du der Überholende und musst ausweichen.',
    'To røde over hinanden betyder, at fartøjet ikke er under '
        'kommando. Rød-hvid-rød betyder, at det er begrænset i sin evne '
        'til at manøvrere. Begge dele betyder: hold godt klar.':
        'Zwei rote übereinander bedeuten, dass das Fahrzeug '
        'manövrierunfähig ist. Rot-Weiß-Rot bedeutet manövrierbehindert. '
        'Beides heißt: gut freihalten.',
    'Om dagen: en sort kugle er for anker. En sort kegle med spidsen '
        'nedad er en sejlbåd, der også har motoren i gang — og så gælder '
        'reglerne for motorfartøjer. Den kegle glemmer næsten alle, og '
        'den ændrer, hvem der viger.':
        'Am Tag: ein schwarzer Ball heißt vor Anker. Ein schwarzer Kegel '
        'mit der Spitze nach unten ist ein Segelboot, das auch die '
        'Maschine laufen hat — und dann gelten die Regeln für '
        'Maschinenfahrzeuge. Diesen Kegel vergisst fast jeder, und er '
        'ändert, wer ausweicht.',
    'Lyd- og nødsignaler':
        'Schall- und Notsignale',
    'Ét kort er styrbord, fem korte er en advarsel.':
        'Ein kurzer Ton heißt Steuerbord, fünf kurze sind eine Warnung.',
    'Når I kan se hinanden: ét kort stød betyder "jeg drejer til '
        'styrbord", to korte "til bagbord", tre korte "jeg bakker". Fem '
        'korte eller flere er advarslen — jeg forstår dig ikke, eller du '
        'gør ikke nok for at holde klar.':
        'Wenn ihr euch seht: ein kurzer Ton heißt „ich drehe nach '
        'Steuerbord“, zwei kurze „nach Backbord“, drei kurze „ich gehe '
        'rückwärts“. Fünf kurze oder mehr sind die Warnung — ich verstehe '
        'dich nicht, oder du tust nicht genug, um freizuhalten.',
    'I tåge lyder det hvert andet minut: ét langt fra et motorfartøj '
        'med fart i, to lange fra et, der ligger stille, og ét langt plus '
        'to korte fra en sejlbåd — og fra en fisker og en manøvrehæmmet. '
        'Så du ved ikke hvilken, kun at du skal holde klar.':
        'Im Nebel klingt es alle zwei Minuten: ein langer Ton von einem '
        'Maschinenfahrzeug mit Fahrt, zwei lange von einem ohne Fahrt, '
        'und ein langer plus zwei kurze von einem Segelboot — und von '
        'einem Fischer und einem Manövrierbehinderten. Du weißt also '
        'nicht welches, nur dass du freihalten musst.',
    'I nød: MAYDAY på kanal 16 eller DSC-nødknappen. 112 går videre '
        'til JRCC og virker, så længe du har mobildækning. Røde blus er '
        'nød; et hvidt blus er en advarsel og noget helt andet.':
        'In Not: MAYDAY auf Kanal 16 oder die DSC-Nottaste. In Dänemark '
        'geht 112 weiter an das JRCC, solange du Mobilempfang hast; in '
        'Deutschland ist es 112 an die Seenotleitung Bremen. Rote Signale '
        'sind Not; eine weiße Fackel ist eine Warnung und etwas ganz '
        'anderes.',
    'Hvorfor vi ikke advarer om grunde':
        'Warum wir nicht vor Untiefen warnen',
    'Sejlplan kender land og vand — ikke dybder. Farerne står i '
        'søkortet.':
        'Segelplan kennt Land und Wasser — keine Tiefen. Die Gefahren '
        'stehen in der Seekarte.',
    'Ruten lægges uden om land med en maske over de skandinaviske '
        'farvande. Masken kender kysten. Den kender ikke dybder, grunde, '
        'rev, sten, spærrede områder, skydeområder eller sejlrender.':
        'Die Route wird mit einer Maske über den skandinavischen '
        'Gewässern um das Land herum gelegt. Die Maske kennt die Küste. '
        'Sie kennt keine Tiefen, keine Untiefen, keine Riffe, keine '
        'Steine, keine Sperrgebiete, keine Schießgebiete und keine '
        'Fahrrinnen.',
    'Vi kunne godt skrive "pas på grunden her" ud fra et gæt. Vi '
        'lader være. En advarsel, der ser rigtig ud og er forkert, er '
        'farligere end ingen advarsel — for så holder man op med at kigge '
        'i søkortet.':
        'Wir könnten aus einer Vermutung heraus „Achtung, hier ist eine '
        'Untiefe“ schreiben. Wir lassen es. Eine Warnung, die richtig '
        'aussieht und falsch ist, ist gefährlicher als gar keine — dann '
        'hört man nämlich auf, in die Seekarte zu schauen.',
    'Farerne står i søkortet og i Efterretninger for Søfarende. Læg '
        'ruten her, og gå den efter dér. Særligt i smalt farvand, tæt på '
        'kysten og omkring pynter og rev.':
        'Die Gefahren stehen in der Seekarte und in den Nachrichten für '
        'Seefahrer. Lege die Route hier, und geh sie dort durch. '
        'Besonders im engen Fahrwasser, dicht unter Land und um '
        'Landspitzen und Riffe herum.',
    'Bagbords sidemærke':
        'Backbordtonne',
    'Rød, dåseformet. Står i bagbords side af løbet, når du sejler '
        'ind — mod havn, op ad et løb, eller den vej afmærkningsretningen '
        'går på søkortet.':
        'Rot, stumpf. Steht an der Backbordseite des Fahrwassers, wenn du '
        'einläufst — zum Hafen, ein Fahrwasser hinauf, oder in die '
        'Richtung, in die die Betonnungsrichtung in der Seekarte weist.',
    'Hold det i bagbord, når du går ind. Ud igen: i styrbord.':
        'Halte sie an Backbord, wenn du einläufst. Hinaus: an Steuerbord.',
    'Rødt. Enhver karakter.':
        'Rot. Jede Kennung.',
    'Rødt i bagbord, når du går ind. I Amerika er det omvendt — dér '
        'gælder IALA B.':
        'Rot an Backbord, wenn du einläufst. In Amerika ist es umgekehrt '
        '— dort gilt IALA B.',
    'Styrbords sidemærke':
        'Steuerbordtonne',
    'Grøn, spids som en kegle. Står i styrbords side af løbet, når du '
        'sejler ind.':
        'Grün, spitz wie ein Kegel. Steht an der Steuerbordseite des '
        'Fahrwassers, wenn du einläufst.',
    'Hold det i styrbord, når du går ind. Ud igen: i bagbord.':
        'Halte sie an Steuerbord, wenn du einläufst. Hinaus: an Backbord.',
    'Grønt. Enhver karakter.':
        'Grün. Jede Kennung.',
    'Nordmærke':
        'Nordtonne',
    'Sort øverst, gul nederst. To kegler med spidserne opad — de '
        'peger op mod det sorte.':
        'Oben schwarz, unten gelb. Zwei Kegel mit den Spitzen nach oben — '
        'sie zeigen hinauf zum Schwarzen.',
    'Passér nord for mærket. Farvandet syd for det er ikke sikkert.':
        'Passiere nördlich von der Tonne. Das Fahrwasser südlich davon '
        'ist nicht sicher.',
    'Hvidt, uafbrudt hurtigblink: Q eller VQ.':
        'Weiß, ununterbrochenes Funkeln: Q oder VQ.',
    'Keglerne peger hen mod den side, du skal gå.':
        'Die Kegel zeigen zu der Seite, auf der du vorbeimusst.',
    'Østmærke':
        'Osttonne',
    'Sort, gult bånd, sort. To kegler bund mod bund.':
        'Schwarz, gelbes Band, schwarz. Zwei Kegel Basis an Basis.',
    'Passér øst for mærket.':
        'Passiere östlich von der Tonne.',
    'Hvidt: Q(3) 10s eller VQ(3) 5s.':
        'Weiß: Q(3) 10s oder VQ(3) 5s.',
    'Tre blink som klokken tre — øst.':
        'Drei Blitze wie drei Uhr — Ost.',
    'Sydmærke':
        'Südtonne',
    'Gul øverst, sort nederst. To kegler med spidserne nedad.':
        'Oben gelb, unten schwarz. Zwei Kegel mit den Spitzen nach unten.',
    'Passér syd for mærket.':
        'Passiere südlich von der Tonne.',
    'Hvidt: Q(6) + langt blink 15s, eller VQ(6) + langt blink 10s.':
        'Weiß: Q(6) + langer Blitz 15s, oder VQ(6) + langer Blitz 10s.',
    'Seks blink som klokken seks — syd. Det lange blink er der, så du '
        'ikke kommer i tvivl om, hvor gruppen slutter.':
        'Sechs Blitze wie sechs Uhr — Süd. Der lange Blitz ist da, damit '
        'du nicht im Zweifel bist, wo die Gruppe endet.',
    'Vestmærke':
        'Westtonne',
    'Gul, sort bånd, gul. To kegler spids mod spids — som et '
        'timeglas.':
        'Gelb, schwarzes Band, gelb. Zwei Kegel Spitze an Spitze — wie '
        'eine Sanduhr.',
    'Passér vest for mærket.':
        'Passiere westlich von der Tonne.',
    'Hvidt: Q(9) 15s eller VQ(9) 10s.':
        'Weiß: Q(9) 15s oder VQ(9) 10s.',
    'Ni blink som klokken ni — vest.':
        'Neun Blitze wie neun Uhr — West.',
    'Enkeltstående fare':
        'Einzelgefahrenzeichen',
    'Sort med et eller flere brede røde bånd. To sorte kugler over '
        'hinanden.':
        'Schwarz mit einem oder mehreren breiten roten Bändern. Zwei '
        'schwarze Bälle übereinander.',
    'Der er farbart vand hele vejen rundt, men faren ligger lige dér. '
        'Gå udenom med god margen.':
        'Ringsum ist befahrbares Wasser, aber die Gefahr liegt genau '
        'dort. Geh mit gutem Abstand außen herum.',
    'Hvidt: to blink, Fl(2) 5s.':
        'Weiß: zwei Blitze, Fl(2) 5s.',
    'Sikkert vand':
        'Sicheres Fahrwasser',
    'Røde og hvide lodrette striber. Én rød kugle.':
        'Rote und weiße senkrechte Streifen. Ein roter Ball.',
    'Der er vand hele vejen rundt. Bruges midt i et løb og som '
        'landfaldsbøje — dén, man styrer efter, når man kommer ind fra '
        'søen.':
        'Ringsum ist Wasser. Wird in der Mitte eines Fahrwassers und als '
        'Ansteuerungstonne benutzt — die, auf die man zuhält, wenn man '
        'von See kommt.',
    'Hvidt: Iso, Oc, langt blink hvert 10. sekund, eller morse A.':
        'Weiß: Iso, Oc, langer Blitz alle 10 Sekunden, oder Morse A.',
    'Særligt mærke':
        'Sonderzeichen',
    'Gult, med et liggende gult kryds.':
        'Gelb, mit einem liegenden gelben Kreuz.',
    'Markerer noget andet end sejladsen: kabler, rørledninger, '
        'badeområder, opdræt, kapsejladsbaner. Slå op i søkortet, hvad '
        'det er, før du sejler henover.':
        'Markiert etwas anderes als die Fahrt: Kabel, Rohrleitungen, '
        'Badegebiete, Aquakultur, Regattabahnen. Schlag in der Seekarte '
        'nach, was es ist, bevor du darüber hinwegsegelst.',
    'Gult.':
        'Gelb.',
    'Ny fare':
        'Neue Gefahr',
    'Blå og gule lodrette striber. Stående gult kryds.':
        'Blaue und gelbe senkrechte Streifen. Stehendes gelbes Kreuz.',
    'Et vrag eller en fare, der lige er opstået, og som endnu ikke '
        'står i søkortet. Hold godt klar.':
        'Ein Wrack oder eine Gefahr, die gerade erst entstanden ist und '
        'noch nicht in der Seekarte steht. Halte gut frei.',
    'Skiftevis blåt og gult, ét sekund hver.':
        'Abwechselnd blau und gelb, je eine Sekunde.',
    'Blink — lyset er kortere end mørket.':
        'Blitz — das Licht ist kürzer als die Dunkelheit.',
    'Langt blink — mindst to sekunder.':
        'Langer Blitz — mindestens zwei Sekunden.',
    'Formørkelse — lyset er længere end mørket.':
        'Unterbrochen — das Licht ist länger als die Dunkelheit.',
    'Lige lang tid tændt og slukket.':
        'Gleich lang hell und dunkel.',
    'Hurtigblink, omkring 50–60 i minuttet.':
        'Funkelfeuer, etwa 50–60 in der Minute.',
    'Meget hurtigt blink, omkring 100–120 i minuttet.':
        'Schnelles Funkelfeuer, etwa 100–120 in der Minute.',
    'Fast lys, der ikke blinker.':
        'Festes Licht, das nicht blinkt.',
    'Morse A: kort-langt. Bruges på landfaldsbøjer.':
        'Morse A: kurz-lang. Wird auf Ansteuerungstonnen benutzt.',
    'Tallet i parentes er antal blink i gruppen.':
        'Die Zahl in Klammern ist die Anzahl der Blitze in der Gruppe.',
    'Sekundtallet er hele periodens længde — tag tid på den.':
        'Die Sekundenzahl ist die Länge der ganzen Periode — stoppe sie.',
    'Farven: hvid, rød, grøn.':
        'Die Farbe: weiß, rot, grün.',
    'Tre blink, hvidt i én retning og rødt i en anden, og det hele '
        'gentager sig hvert tiende sekund.':
        'Drei Blitze, weiß in die eine Richtung und rot in die andere, '
        'und das Ganze wiederholt sich alle zehn Sekunden.',
    'Et sektorfyr viser forskellig farve i forskellige retninger. '
        'Hvidt betyder som regel, at du er i det rene løb; rødt og grønt, '
        'at du er ude af det til hver sin side. Hvilken side hvad er, '
        'står i søkortet — det er ikke det samme alle steder.':
        'Ein Sektorenfeuer zeigt in verschiedene Richtungen verschiedene '
        'Farben. Weiß bedeutet in der Regel, dass du im freien Fahrwasser '
        'bist; rot und grün, dass du zu je einer Seite heraus bist. '
        'Welche Seite was ist, steht in der Seekarte — das ist nicht '
        'überall gleich.',
    'Rød og grøn side om side, ingen hvid over':
        'Rot und Grün nebeneinander, kein Weiß darüber',
    'En sejlbåd for sejl, der kommer lige imod dig.':
        'Ein Segelboot unter Segeln, das genau auf dich zukommt.',
    'Rød og grøn med ét hvidt lys over':
        'Rot und Grün mit einem weißen Licht darüber',
    'Et motorfartøj, der kommer lige imod dig.':
        'Ein Maschinenfahrzeug, das genau auf dich zukommt.',
    'Rød og grøn med to hvide over hinanden':
        'Rot und Grün mit zwei weißen übereinander',
    'Et motorfartøj over 50 meter — og det bagerste hvide lys er '
        'højest. Står de to hvide lodret over hinanden, kommer det lige '
        'imod dig.':
        'Ein Maschinenfahrzeug über 50 Meter — und das achtere weiße '
        'Licht steht höher. Stehen die beiden weißen senkrecht '
        'übereinander, kommt es genau auf dich zu.',
    'Kun grønt':
        'Nur Grün',
    'Du ser dens styrbords side. Den går fra bagbord mod styrbord '
        'foran dig.':
        'Du siehst seine Steuerbordseite. Es geht von Backbord nach '
        'Steuerbord vor dir durch.',
    'Kun rødt':
        'Nur Rot',
    'Du ser dens bagbords side. Som udgangspunkt er det dig, der '
        'viger — men se på pejlingen, ikke på farven alene.':
        'Du siehst seine Backbordseite. Im Grundsatz weichst du aus — '
        'aber sieh auf die Peilung, nicht allein auf die Farbe.',
    'Kun hvidt agter':
        'Nur Weiß von achtern',
    'Du ser den bagfra. Du indhenter den, og så er det dig, der '
        'holder klar.':
        'Du siehst es von hinten. Du überholst, und dann musst du '
        'freihalten.',
    'Ét hvidt rundtlysende, ingen andet':
        'Ein weißes Rundumlicht, sonst nichts',
    'Et fartøj for anker — eller en lille båd under 7 meter.':
        'Ein Fahrzeug vor Anker — oder ein kleines Boot unter 7 Meter.',
    'To røde over hinanden, rundtlysende':
        'Zwei rote Rundumlichter übereinander',
    'Ikke under kommando. Den kan ikke styre. Hold klar.':
        'Manövrierunfähig. Es kann nicht steuern. Halte frei.',
    'Rød–hvid–rød lodret':
        'Rot–Weiß–Rot senkrecht',
    'Begrænset i sin evne til at manøvrere. Uddybning, bugsering, '
        'dykkerarbejde. Hold godt klar.':
        'Manövrierbehindert. Baggern, Schleppen, Taucharbeiten. Halte gut '
        'frei.',
    'Grønt over hvidt':
        'Grün über Weiß',
    'Trawler. Der kan gå wire langt agterud.':
        'Trawler. Es kann weit achteraus Draht stehen.',
    'En sort kugle':
        'Ein schwarzer Ball',
    'For anker.':
        'Vor Anker.',
    'En sort kegle med spidsen nedad':
        'Ein schwarzer Kegel mit der Spitze nach unten',
    'En sejlbåd, der også har motoren i gang. Så gælder reglerne for '
        'motorfartøjer, ikke for sejlbåde — og det er dét, folk glemmer.':
        'Ein Segelboot, das auch die Maschine laufen hat. Dann gelten die '
        'Regeln für Maschinenfahrzeuge, nicht die für Segelboote — und '
        'das ist es, was die Leute vergessen.',
    'To sorte kugler over hinanden':
        'Zwei schwarze Bälle übereinander',
    'Ikke under kommando.':
        'Manövrierunfähig.',
    'Kugle – rombe – kugle':
        'Ball – Rhombus – Ball',
    'Begrænset i sin evne til at manøvrere.':
        'Manövrierbehindert.',
    'En sort cylinder':
        'Ein schwarzer Zylinder',
    'Begrænset af sin dybgang.':
        'Tiefgangbehindert.',
    'Tre sorte kugler over hinanden':
        'Drei schwarze Bälle übereinander',
    'Fartøjet står på grund.':
        'Das Fahrzeug sitzt auf Grund.',
    'Ét kort stød':
        'Ein kurzer Ton',
    'Jeg drejer til styrbord.':
        'Ich drehe nach Steuerbord.',
    'To korte stød':
        'Zwei kurze Töne',
    'Jeg drejer til bagbord.':
        'Ich drehe nach Backbord.',
    'Tre korte stød':
        'Drei kurze Töne',
    'Jeg bakker.':
        'Ich gehe rückwärts.',
    'Fem korte stød eller flere':
        'Fünf kurze Töne oder mehr',
    'Jeg forstår ikke, hvad du har tænkt dig — eller: du gør ikke nok '
        'for at holde klar. Det er advarslen.':
        'Ich verstehe nicht, was du vorhast — oder: du tust nicht genug, '
        'um freizuhalten. Das ist die Warnung.',
    'Ét langt stød':
        'Ein langer Ton',
    'Jeg nærmer mig et sving eller et sted, hvor jeg ikke kan se, '
        'hvad der kommer.':
        'Ich nähere mich einer Biegung oder einer Stelle, an der ich '
        'nicht sehen kann, was kommt.',
    'Ét langt hvert andet minut':
        'Ein langer Ton alle zwei Minuten',
    'Motorfartøj med fart gennem vandet.':
        'Maschinenfahrzeug mit Fahrt durchs Wasser.',
    'To lange hvert andet minut':
        'Zwei lange Töne alle zwei Minuten',
    'Motorfartøj, der ligger stille i vandet.':
        'Maschinenfahrzeug, das ohne Fahrt im Wasser liegt.',
    'Ét langt og to korte hvert andet minut':
        'Ein langer und zwei kurze Töne alle zwei Minuten',
    'Sejlbåd for sejl. Det samme lyder fra en fisker, en bugserende '
        'og en manøvrehæmmet — så du ved ikke hvilken, kun at du skal '
        'holde klar.':
        'Segelboot unter Segeln. Dasselbe klingt von einem Fischer, einem '
        'Schleppenden und einem Manövrierbehinderten — du weißt also '
        'nicht welches, nur dass du freihalten musst.',
    'Klokke i fem sekunder hvert minut':
        'Glocke fünf Sekunden lang jede Minute',
    'Fartøj for anker. Er det over 100 meter, kommer der en gongong '
        'agter bagefter.':
        'Fahrzeug vor Anker. Ist es über 100 Meter, folgt achtern ein '
        'Gong.',
    'VHF kanal 16 — MAYDAY':
        'UKW Kanal 16 — MAYDAY',
    'Sig MAYDAY tre gange, bådens navn, position, hvad der er sket, '
        'og hvor mange I er. DSC-nødknappen sender position og '
        'kaldesignal af sig selv.':
        'Sag dreimal MAYDAY, den Namen des Bootes, die Position, was '
        'passiert ist und wie viele ihr seid. Die DSC-Nottaste sendet '
        'Position und Rufzeichen von selbst.',
    '112':
        '112',
    'Går videre til JRCC. Virker, når du har mobildækning, og det har '
        'man tit tættere på land end man tror.':
        'Geht in Dänemark weiter an das JRCC, in Deutschland an die '
        'Seenotleitung Bremen. Funktioniert, solange du Mobilempfang hast '
        '— und den hat man näher an Land oft, als man denkt.',
    'Rødt faldskærmsblus eller rødt håndblus':
        'Rote Fallschirmrakete oder rote Handfackel',
    'Nød. Et hvidt blus er derimod en advarsel — ikke det samme.':
        'Not. Eine weiße Fackel ist dagegen eine Warnung — nicht '
        'dasselbe.',
    'Orange røgsignal':
        'Orangefarbenes Rauchsignal',
    'Nød, om dagen. Ses langt i klart vejr.':
        'Not, am Tag. Bei klarem Wetter weithin zu sehen.',
    'Langsomme bevægelser op og ned med begge arme':
        'Langsames Auf und Ab mit beiden ausgestreckten Armen',
    'Nød. Det er det signal, man kan give uden udstyr.':
        'Not. Das ist das Signal, das man ohne Ausrüstung geben kann.',
    'Orange dug med sort firkant og cirkel':
        'Orangefarbene Plane mit schwarzem Quadrat und Kreis',
    'Nød, set fra luften. Læg den, så et fly kan se den.':
        'Not, aus der Luft gesehen. Leg sie so, dass ein Flugzeug sie '
        'sehen kann.',
    'Vend, når vindpejlingen til målet er lige så stor til den anden '
        'side. Så sejler du ikke længere end nødvendigt.':
        'Wende, wenn die Windpeilung zum Ziel zur anderen Seite genauso '
        'groß ist. Dann segelst du nicht weiter als nötig.',
    'Fuldt sejl.':
        'Volles Tuch.',
    'Bommen':
        'Der Baum',
    'Kursen ligger tættere på vinden, end båden kan sejle. Strækket '
        'skal krydses — læg dig på den halse, der bringer dig nærmest '
        'målet, og trim som til bidevind.':
        'Der Kurs liegt höher am Wind, als das Boot segeln kann. Der '
        'Abschnitt muss gekreuzt werden — leg dich auf den Bug, der dich '
        'dem Ziel am nächsten bringt, und trimme wie am Wind.',
    'Overvej første reb, hvis båden lægger sig mere end tyve grader, '
        'eller hvis der er tryk i roret.':
        'Erwäge das erste Reff, wenn das Boot sich mehr als zwanzig Grad '
        'legt oder wenn Druck im Ruder ist.',
    'Første reb. Det koster ikke fart — en overtrimmet båd krænger og '
        'skrider sidelæns.':
        'Erstes Reff. Das kostet keine Fahrt — ein übertrimmtes Boot '
        'krängt und rutscht seitwärts.',
    'Andet reb og rullet genua. Kommer det over tredive knob, er det '
        'tredje reb eller en stormfok — og så er spørgsmålet, om turen '
        'skal sejles i dag.':
        'Zweites Reff und eingerollte Genua. Kommt es über dreißig '
        'Knoten, ist es das dritte Reff oder eine Sturmfock — und dann '
        'ist die Frage, ob der Törn heute gesegelt werden soll.',
    'Telltalerne på forsejlet skal strømme bagud på begge sider. '
        'Lifter de i luv, så fald af eller stram skødet. Øverste sejlpind '
        'i storsejlet omtrent parallel med bommen.':
        'Die Windfäden am Vorsegel sollen auf beiden Seiten nach achtern '
        'strömen. Flattern sie in Luv, dann falle ab oder hol die Schot '
        'dichter. Die oberste Latte im Großsegel etwa parallel zum Baum.',
    'Omtrent på midterlinjen. Kig op ad bommen — den skal pege lige '
        'agterud eller en anelse i læ.':
        'Etwa auf der Mittschiffslinie. Sieh am Baum entlang — er soll '
        'genau nach achtern zeigen oder eine Spur nach Lee.',
    'Løjgangsvognen':
        'Der Traveller',
    'Lidt til luv for midten. Så kan skødet holde bommen inde uden at '
        'trække sejlet fladt.':
        'Ein Stück nach Luv über die Mitte. So kann die Schot den Baum '
        'innen halten, ohne das Segel flach zu ziehen.',
    'Storskødet':
        'Die Großschot',
    'Løst nok til at agterliget hænger blødt. Et fladt sejl trækker '
        'ikke i let vind.':
        'Lose genug, dass das Achterliek weich hängt. Ein flaches Segel '
        'zieht bei wenig Wind nicht.',
    'Bomnedhalet':
        'Der Baumniederholer',
    'Løst. På kryds er det skødet, der holder bommen nede — nedhalet '
        'skal først bruges, når du skøder ud.':
        'Lose. Am Wind hält die Schot den Baum unten — der Niederholer '
        'kommt erst zum Einsatz, wenn du ausschotest.',
    'Udhalet':
        'Der Unterliekstrecker',
    'Løst, så der er dybde i underliget.':
        'Lose, damit Profiltiefe im Unterliek ist.',
    'Nedhalet':
        'Der Cunningham',
    'Helt løst. Rynker i forliget er i orden, når det blæser lidt.':
        'Ganz lose. Falten im Vorliek sind in Ordnung, wenn es etwas '
        'weht.',
    'Agterstaget':
        'Das Achterstag',
    'Løst.':
        'Lose.',
    'Forsejlet':
        'Das Vorsegel',
    'Skødevognen frem, så sejlet får dybde forneden. Skød blødt — '
        'genuaen skal ikke røre saling eller vant.':
        'Den Holepunkt nach vorn, damit das Segel unten Profiltiefe '
        'bekommt. Schote weich — die Genua soll Saling und Wanten nicht '
        'berühren.',
    'Midtskibs.':
        'Mittschiffs.',
    'Stramt. Øverste sejlpind parallel med bommen — i byger må den '
        'gerne falde en smule af.':
        'Dicht. Die oberste Latte parallel zum Baum — in Böen darf sie '
        'eine Spur abfallen.',
    'Stramt. Fladt sejl, mindre krængning.':
        'Dicht. Flaches Segel, weniger Krängung.',
    'Stram, til rynkerne langs masten lige forsvinder. Det flytter '
        'trykpunktet frem og flader sejlet.':
        'Hol so weit dicht, bis die Falten längs des Mastes gerade '
        'verschwinden. Das schiebt den Druckpunkt nach vorn und flacht '
        'das Segel ab.',
    'Skødevognen midt i sporet. Telltalerne skal lifte samtidig oppe '
        'og nede.':
        'Den Holepunkt in der Mitte der Schiene. Die Windfäden sollen '
        'oben und unten gleichzeitig flattern.',
    'Til læ, indtil båden retter sig op. Det åbner toppen og lader '
        'trykket gå ud foroven i stedet for at lægge båden ned.':
        'Nach Lee, bis das Boot sich aufrichtet. Das öffnet den Kopf und '
        'lässt den Druck oben heraus, statt das Boot zu legen.',
    'Stram. Masten bøjer, storsejlet flader ud, og forstaget bliver '
        'stivere — det er dét, der gør, at du kan holde højde.':
        'Dicht. Der Mast biegt sich, das Großsegel flacht ab, und das '
        'Vorstag wird steifer — das ist es, was dich Höhe halten lässt.',
    'Skødevognen agter. Toppen åbner, og båden retter sig op uden at '
        'du mister fart.':
        'Den Holepunkt nach achtern. Der Kopf öffnet, und das Boot '
        'richtet sich auf, ohne dass du Fahrt verlierst.',
    'Skød ud, til forkanten lige begynder at bagge, og stram så lidt '
        'til igen. Det er dér, sejlet trækker mest.':
        'Schote aus, bis das Vorliek gerade anfängt zu killen, und hol '
        'dann wieder eine Spur dicht. Dort zieht das Segel am meisten.',
    'Ud til omkring tyve-tredive grader fra midterlinjen.':
        'Auf etwa zwanzig bis dreißig Grad von der Mittschiffslinie.',
    'Til læ. Nu er det bomnedhalet, der styrer twisten — ikke vognen.':
        'Nach Lee. Jetzt steuert der Baumniederholer den Twist — nicht '
        'der Traveller.',
    'Skød ud, til forkanten lige begynder at bagge, og stram så lidt '
        'til.':
        'Schote aus, bis das Vorliek gerade anfängt zu killen, und hol '
        'dann eine Spur dicht.',
    'Stram nu. Uden det løfter bommen sig, toppen af sejlet falder '
        'af, og du mister det tryk, du troede du havde.':
        'Jetzt dicht. Ohne ihn hebt sich der Baum, der Kopf des Segels '
        'fällt ab, und du verlierst den Druck, den du zu haben glaubtest.',
    'Løsn en smule. Halvvind vil have dybde.':
        'Eine Spur lose. Halber Wind will Profiltiefe.',
    'Løsn, med mindre det blæser.':
        'Lose, außer es weht.',
    'Løsn. Du skal ikke bruge højde her.':
        'Lose. Höhe brauchst du hier nicht.',
    'Skødevognen lidt frem og ud. Slæk skødet, til telltalerne '
        'strømmer på begge sider.':
        'Den Holepunkt etwas nach vorn und außen. Fiere die Schot, bis '
        'die Windfäden auf beiden Seiten strömen.',
    'Telltalen agter på storsejlet skal strømme. Krøller den ind bag '
        'sejlet, er der for meget twist — stram bomnedhalet.':
        'Der Windfaden achtern am Großsegel soll strömen. Kringelt er '
        'sich hinter das Segel, ist zu viel Twist drin — hol den '
        'Baumniederholer dichter.',
    'Fra her og ned mod læns er der risiko for en utilsigtet '
        'bomvending. Sæt bomholder.':
        'Von hier an bis vor den Wind besteht die Gefahr einer '
        'unbeabsichtigten Patenthalse. Setze einen Bullenstander.',
    'Godt ud. Pas på, at den ikke ligger an mod vantet — det slider '
        'sejlet i stykker på en lang dag.':
        'Weit aus. Pass auf, dass er nicht an den Wanten anliegt — das '
        'zerscheuert das Segel an einem langen Tag.',
    'Helt i læ.':
        'Ganz nach Lee.',
    'Ud, til sejlet lige bagger i forkanten.':
        'Aus, bis das Segel im Vorliek gerade back steht.',
    'Hårdt. Det er nu, det tjener sig ind.':
        'Hart. Jetzt zahlt er sich aus.',
    'Løst. Dybt sejl.':
        'Lose. Tiefes Segel.',
    'Skødevognen helt frem og ud. Bliver genuaen dækket af '
        'storsejlet, så tag den over på den anden side med en bom — eller '
        'sæt spiler eller gennaker, hvis I har hænder til det.':
        'Den Holepunkt ganz nach vorn und außen. Wird die Genua vom '
        'Großsegel abgedeckt, dann nimm sie mit einem Baum auf die andere '
        'Seite — oder setze Spinnaker oder Gennaker, wenn ihr Hände dafür '
        'habt.',
    'Fuldt sejl. Hold øje med bygerne.':
        'Volles Tuch. Behalte die Böen im Auge.',
    'Første reb, hvis det er trættende at styre.':
        'Erstes Reff, wenn das Steuern anstrengend wird.',
    'Hold øje med vindviseren og med bølgerne agterfra. Ruller båden, '
        'så luf en smule op — læns er ikke det hurtigste, og sjældent det '
        'roligste.':
        'Behalte den Verklicker und die See von achtern im Auge. Rollt '
        'das Boot, dann luv eine Spur an — vor dem Wind ist nicht das '
        'Schnellste und selten das Ruhigste.',
    'Sæt bomholder, før du falder af. En utilsigtet bomvending på '
        'læns er dét, der slår folk ned og river rigge ned — og den '
        'kommer, når nogen kigger et andet sted hen.':
        'Setze den Bullenstander, bevor du abfällst. Eine unbeabsichtigte '
        'Patenthalse vor dem Wind ist das, was Leute niederschlägt und '
        'Riggs herunterreißt — und sie kommt, wenn jemand gerade woanders '
        'hinsieht.',
    'Helt ud.':
        'Ganz aus.',
    'Ude. Det er nedhalet og bomholderen, der holder bommen.':
        'Aus. Der Niederholer und der Bullenstander halten den Baum.',
    'Hårdt.':
        'Hart.',
    'Bom genuaen ud på modsat side af storsejlet, eller sæt spiler. '
        'Uden det står den og klapper i storsejlets læ og gør ingen '
        'nytte.':
        'Baume die Genua auf der dem Großsegel gegenüberliegenden Seite '
        'aus, oder setze den Spinnaker. Ohne das steht sie im '
        'Windschatten des Großsegels und klappert, ohne zu nützen.',
}
