"""Sejlplanens egen tekst på tysk.

Nøglen er den danske sætning fra `app/narrative.py`. Pladsholderne i tuborg-
parenteser skal være de samme i begge sprog — er de ikke det, falder t()
tilbage til dansk, og så står tallene rigtigt, men sproget forkert.

Sætningerne er bygget hele. Tysk bøjer efter køn og kasus, så en sætning kan
ikke limes sammen af stumper: "i modsø" bliver ikke til "in Gegensee" ved at
oversætte "i" og "modsø" hver for sig.
"""

WORDS: dict[str, str] = {
    'vendepunktet':
        'dem Wendepunkt',
    '{sm} sømil · ca. {tid} {hvordan}':
        '{sm} Seemeilen · ca. {tid} {hvordan}',
    'Kræver {sejldøgn} — altså {overnatninger} undervejs, medmindre du '
        'slår mørkesejlads til.':
        'Erfordert {sejldøgn} — also {overnatninger} unterwegs, sofern du '
        'nicht Nachtfahrt einschaltest.',
    'Ruten {navne} er på {sm} sømil fordelt på {ben}. ':
        'Die Route {navne} ist {sm} Seemeilen lang, verteilt auf {ben}. ',
    'Vinden ligger mellem {fra} og {til} knob ({styrke} på det '
        'kraftigste)':
        'Der Wind liegt zwischen {fra} und {til} Knoten ({styrke} in der '
        'Spitze)',
    'ud for {sted}':
        'vor {sted}',
    'kurs {grader}° {retning}':
        'Kurs {grader}° {retning}',
    'ved marchfart':
        'bei Marschfahrt',
    'i jævn vind':
        'bei mäßiger Brise',
    'Kan nås inden for ét sejldøgn ({fra}–{til}).':
        'Innerhalb eines Etmals zu schaffen ({fra}–{til} Uhr).',
    'Søen er til at leve med, og turen bør være behagelig.':
        'Mit der See lässt sich leben, und der Törn dürfte angenehm werden.',
    'Marchfarten er {kn} knob, men søen tager omkring {tab} knob af den '
        '— du kommer frem med {snit} i snit':
        'Die Marschfahrt liegt bei {kn} Knoten, aber die See nimmt davon '
        'rund {tab} Knoten — du kommst mit {snit} im Schnitt voran',
    'Marchfarten er {kn} knob, og den kan holdes stort set hele vejen '
        '({snit} i snit)':
        'Die Marschfahrt liegt bei {kn} Knoten, und sie lässt sich fast den '
        'ganzen Weg halten ({snit} im Schnitt)',
    'Vandet er så småt, at turen bliver stille og hurtig.':
        'Das Wasser ist so glatt, dass der Törn ruhig und schnell wird.',
    ' — med {overnatninger} undervejs i {havne}.':
        ' — mit {overnatninger} unterwegs in {havne}.',
    ' og drejer fra {fra} til {til} undervejs.':
        ' und dreht unterwegs von {fra} nach {til}.',
    ' fra {retning} hele vejen.':
        ' aus {retning} den ganzen Weg.',
    ' Bølgerne når op på {m} meter.':
        ' Die Wellen erreichen {m} Meter.',
    ' Der er ingen nævneværdig søgang i prognosen.':
        ' In der Vorhersage steht kein nennenswerter Seegang.',
    'Du bliver formentlig blæst inde i {sted}. Efter ankomsten viser '
        'prognosen {døgn} i træk uden et vindue, du kan sejle i — op til '
        '{kn} knobs vind og {m} meter sø. ':
        'Du wirst in {sted} vermutlich vom Wind festgesetzt. Nach der '
        'Ankunft zeigt die Vorhersage {døgn} am Stück ohne ein Fenster, in '
        'dem du segeln kannst — bis zu {kn} Knoten Wind und {m} Meter '
        'Seegang.  ',
    'Du bliver formentlig blæst inde i {sted}. Efter ankomsten viser '
        'prognosen {døgn} i træk uden et vindue, du kan sejle i — op til '
        '{kn} knobs vind. ':
        'Du wirst in {sted} vermutlich vom Wind festgesetzt. Nach der '
        'Ankunft zeigt die Vorhersage {døgn} am Stück ohne ein Fenster, in '
        'dem du segeln kannst — bis zu {kn} Knoten Wind.  ',
    'Først {tidspunkt} er der noget at sejle i igen. Skal du på arbejde '
        'inden da, så vælg en anden afgang — eller en havn, du kommer hjem '
        'fra.':
        'Erst {tidspunkt} gibt es wieder etwas, worin sich segeln lässt. '
        'Musst du vorher zur Arbeit, dann wähle eine andere Abfahrt — oder '
        'einen Hafen, von dem du wieder nach Hause kommst.',
    'Ankomst':
        'Ankunft',
    'Varighed':
        'Dauer',
    'Ophold':
        'Aufenthalt',
    'OVERBLIK':
        'ÜBERBLICK',
    'VÆR OPMÆRKSOM PÅ':
        'DARAUF ACHTEN',
    'STRÆK FOR STRÆK':
        'ABSCHNITT FÜR ABSCHNITT',
    'TIME FOR TIME':
        'STUNDE FÜR STUNDE',
    'Tid            Vind        Bølger  Fart   Sejlføring':
        'Zeit           Wind        Wellen  Fahrt  Segelführung',
    'kn':
        'kn',
    'm':
        'm',
    'Prognoser er prognoser. Planen erstatter ikke søkort, '
        'farvandsudsigt eller almindelig sømandskab.':
        'Vorhersagen sind Vorhersagen. Der Plan ersetzt weder Seekarte noch '
        'Seewetterbericht oder gewöhnliche Seemannschaft.',
    '{sm} sømil, {tid} undervejs.':
        '{sm} Seemeilen, {tid} unterwegs.',
    'Der er næsten ingen sø. Det bliver en behagelig tur.':
        'Es steht so gut wie kein Seegang. Das wird ein angenehmer Törn.',
    'Søen kommer ind forfra det meste af vejen. Båden stamper, og der '
        'bliver vådt på fordækket — hold godt fast under skiftene.':
        'Die See kommt den größten Teil des Weges von vorn. Das Boot '
        'stampft, und das Vordeck wird nass — bei den Wachwechseln gut '
        'festhalten.',
    'Der er sø nok til at man mærker den. Sørg for at alt er surret, og '
        'at kabyssen kan bruges med én hånd.':
        'Es steht genug See, um sie zu spüren. Sorge dafür, dass alles '
        'verzurrt ist und die Pantry sich mit einer Hand bedienen lässt.',
    'Der går omkring {liter} liter brændstof på turen.':
        'Für den Törn gehen rund {liter} Liter Kraftstoff drauf.',
    'Vejrudsigten rækker ikke hele vejen. Kaster du los {afgang}, når '
        'du {nået} sømil på {tid} under vejs med {båd}, før prognosen '
        'slipper op {slut}':
        'Die Vorhersage reicht nicht den ganzen Weg. Legst du {afgang} ab, '
        'schaffst du {nået} Seemeilen in {tid} unterwegs mit {båd}, bevor '
        'die Vorhersage {slut} endet',
    'Med {båd} tager den beregnet {tid} under vejs. Du kaster los '
        '{afgang} og er fremme {ankomst}':
        'Mit {båd} dauert sie berechnet {tid} unterwegs. Du legst {afgang} '
        'ab und bist {ankomst} am Ziel',
    ' i én stræk.':
        ', ohne Zwischenstopp.',
    '{n} af timerne er så vindsvage, at motoren må hjælpe':
        '{n} der Stunden sind so windschwach, dass der Motor helfen muss',
    '{n} timer ligger uden for dit sejldøgn':
        '{n} Stunden liegen außerhalb deines Etmals',
    'vindstødene går op til {kn} knob, altså noget over middelvinden':
        'die Böen gehen bis {kn} Knoten, also deutlich über den mittleren '
        'Wind',
    'Dag {nr} · {dato}: {fra} → {til}, {sm} sømil, {afgang}–{ankomst} '
        '({tid} under vejs).':
        'Tag {nr} · {dato}: {fra} → {til}, {sm} Seemeilen, '
        '{afgang}–{ankomst} ({tid} unterwegs).',
    'Og det holder ikke op, før prognosen gør: den rækker til {dato}, '
        'og der blæser det stadig. Regn med at ligge stille, til vejret '
        'vender, og læg hjemturen som en tur for sig.':
        'Und es hört nicht auf, bevor die Vorhersage aufhört: Sie reicht '
        'bis {dato}, und da weht es immer noch. Rechne damit, still zu '
        'liegen, bis das Wetter dreht, und plane den Rückweg als eigenen '
        'Törn.',
    '{sm} sømil':
        '{sm} Seemeilen',
    '{tid} under vejs · snitfart {kn} knob':
        '{tid} unterwegs · Schnitt {kn} Knoten',
    'DAG FOR DAG':
        'TAG FÜR TAG',
    'Vinden står {kn} knob fra {retning}.':
        'Der Wind steht mit {kn} Knoten aus {retning}.',
    'Vinden står {fra}–{til} knob fra {retning}.':
        'Der Wind steht mit {fra}–{til} Knoten aus {retning}.',
    '{tid} af det for motor.':
        'Davon {tid} unter Motor.',
    'Strækket brydes af natten i {havn} — timerne dér er ikke talt med.':
        'Der Abschnitt wird von der Nacht in {havn} unterbrochen — die '
        'Stunden dort sind nicht mitgezählt.',
    'Søen står ind forfra. Det banker i skroget, og det bliver en tur, '
        'hvor man tager farten af og sætter den på igen.':
        'Die See steht von vorn. Es schlägt in den Rumpf, und es wird ein '
        'Törn, auf dem man die Fahrt herausnimmt und wieder aufnimmt.',
    'Søen står ind forfra. Der er stampen i det, men båden bliver ved.':
        'Die See steht von vorn. Es stampft, aber das Boot macht weiter.',
    'Søen kommer skråt ind. Regn med rulning — sørg for at alt står '
        'fast.':
        'Die See kommt schräg ein. Rechne mit Rollen — sorge dafür, dass '
        'alles fest steht.',
    'Der er lidt sø, men ikke nok til at det bliver ubehageligt.':
        'Es steht etwas See, aber nicht genug, um unangenehm zu werden.',
    ' Store dele af turen ligger i vindøjet og skal krydses.':
        ' Große Teile des Törns liegen im Wind und müssen gekreuzt werden.',
    ' Det meste sejles for {sejlføring}.':
        ' Das meiste wird {sejlføring} gesegelt.',
    'Turen slutter {døgn} ude i prognosen. Så langt frem er en '
        'vejrudsigt en tendens, ikke en tidsplan: retningen holder tit, men '
        'styrken og timerne rykker sig. Læg planen, og se den efter igen et '
        'par dage før afgang.':
        'Der Törn endet {døgn} weit draußen in der Vorhersage. So weit '
        'voraus ist eine Vorhersage eine Tendenz, kein Fahrplan: Die '
        'Richtung hält oft, aber die Stärke und die Stunden verschieben '
        'sich. Lege den Plan, und sieh ihn ein paar Tage vor der Abfahrt '
        'noch einmal durch.',
    'Turen når ikke frem inden for den vejrudsigt, vi har. Du kommer '
        '{nået} af {ialt} sømil — de sidste {rest} sømil kan først '
        'planlægges, når prognosen rækker så langt. Læg turen tidligere, '
        'eller planlæg den sidste del om nogle dage.':
        'Der Törn kommt innerhalb der Vorhersage, die wir haben, nicht ans '
        'Ziel. Du schaffst {nået} von {ialt} Seemeilen — die letzten {rest} '
        'Seemeilen lassen sich erst planen, wenn die Vorhersage so weit '
        'reicht. Lege den Törn früher, oder plane das letzte Stück in ein '
        'paar Tagen.',
    'Turen kan ikke sejles inden for ét sejldøgn. Planen lægger '
        '{overnatninger} ind — første gang i {havn} kl. {tid}. Vil du hele '
        'vejen i én stræk, skal du slå mørkesejlads til.':
        'Der Törn lässt sich nicht innerhalb eines Etmals segeln. Der Plan '
        'legt {overnatninger} ein — das erste Mal in {havn} um {tid} Uhr. '
        'Willst du den ganzen Weg in einem Rutsch, musst du Nachtfahrt '
        'einschalten.',
    'Du ligger fortøjet i {havn} allerede kl. {tid}, og der er timer '
        'tilbage af dagen. Det er med vilje: næste stræk er for langt til '
        'at nås inden kl. {slut}:00, og der er ingen havn imellem. Sejler '
        'du videre nu, ender du i mørke.':
        'Du liegst schon um {tid} Uhr in {havn} fest, und vom Tag sind noch '
        'Stunden übrig. Das ist Absicht: Der nächste Abschnitt ist zu lang, '
        'um ihn vor {slut}:00 Uhr zu schaffen, und dazwischen liegt kein '
        'Hafen. Segelst du jetzt weiter, endest du im Dunkeln.',
    '{n} timer ligger over dine grænser — fra {hvornår}. Der er op til '
        '{kn} knob og {m} meter bølger. Overvej at udskyde eller søge havn '
        'undervejs.':
        '{n} Stunden liegen über deinen Grenzen — ab {hvornår}. Es sind bis '
        'zu {kn} Knoten und {m} Meter Wellen. Erwäge, zu verschieben oder '
        'unterwegs einen Hafen anzulaufen.',
    '{n} timer sejles uden for sejldøgnet, første gang omkring {tid}. '
        'Sørg for lanterner, vagtplan og at besætningen er udhvilet.':
        '{n} Stunden werden außerhalb des Etmals gesegelt, das erste Mal '
        'gegen {tid} Uhr. Sorge für Lichterführung, Wachplan und eine '
        'ausgeruhte Crew.',
    'Vindstødene når {kn} knob. Middelvinden holder sig lavere, men '
        '{hvad} skal passe til stødene, ikke til middelværdien.':
        'Die Böen erreichen {kn} Knoten. Der mittlere Wind bleibt darunter, '
        'aber {hvad} muss zu den Böen passen, nicht zum Mittelwert.',
    'Regn med omkring {liter} liter brændstof. Læg en fjerdedel oveni '
        'til reserve og til at ligge og vente.':
        'Rechne mit rund {liter} Litern Kraftstoff. Lege ein Viertel '
        'obendrauf für Reserve und fürs Warten.',
    'Den længste dag er på {tid} i træk. Aftal hvem der styrer hvornår, '
        'og hvor I kan afbryde undervejs.':
        'Der längste Tag ist {tid} am Stück. Sprecht ab, wer wann steuert '
        'und wo ihr unterwegs abbrechen könnt.',
    'Prognosen holder sig inden for dine grænser hele vejen, og du er i '
        'havn inden sejldøgnet er omme. Det ser ud til at blive en god tur.':
        'Die Vorhersage bleibt den ganzen Weg innerhalb deiner Grenzen, und '
        'du bist im Hafen, bevor das Etmal um ist. Das sieht nach einem '
        'guten Törn aus.',
    'SEJLPLAN':
        'SEGELPLAN',
    'ca. {liter} liter':
        'ca. {liter} Liter',
    'Farten svinger mellem {fra} og {til} knob.':
        'Die Fahrt schwankt zwischen {fra} und {til} Knoten.',
    'Der holdes {kn} knob.':
        'Es werden {kn} Knoten gehalten.',
    'Der er for lidt vind til at sejle strækket — motoren må trække det '
        'meste af vejen.':
        'Es ist zu wenig Wind für diesen Abschnitt — der Motor muss den '
        'größten Teil des Weges ziehen.',
    'Bølger op til {m} meter.':
        'Wellen bis {m} Meter.',
    'Bølger op til {m} meter i {sø}.':
        'Wellen bis {m} Meter, {sø}.',
    'Du er først fortøjet i {havn} kl. {tid} — efter dit sejldøgn, der '
        'slutter {slut}:00. Der var ingen havn tættere på, du kunne nå. '
        'Overvej at afgå tidligere, eller at lægge et stop ind før.':
        'Du machst in {havn} erst um {tid} Uhr fest — nach deinem Etmal, '
        'das um {slut}:00 Uhr endet. Es gab keinen näheren Hafen, den du '
        'erreichen konntest. Erwäge, früher abzulegen oder vorher einen '
        'Stopp einzulegen.',
    '{n} timer nærmer sig dine grænser ({kn} knob og {m} meter). {råd}, '
        'og hold øje med om prognosen flytter sig.':
        '{n} Stunden nähern sich deinen Grenzen ({kn} Knoten und {m} '
        'Meter). {råd}, und behalte im Auge, ob die Vorhersage sich '
        'verschiebt.',
    'Kursen ligger så tæt på vinden, at strækket skal krydses.':
        'Der Kurs liegt so dicht am Wind, dass der Abschnitt gekreuzt '
        'werden muss.',
    'Det sejles for {sejlføring} på {halse}.':
        'Gesegelt wird {sejlføring} auf {halse}.',
    'farten':
        'die Fahrt',
    'rebningen':
        'das Reffen',
    'Sæt farten ned i tide':
        'Nimm rechtzeitig Fahrt heraus',
    'Reb i god tid':
        'Reffe rechtzeitig',
}
