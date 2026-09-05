"""Fladens sidste tekster på tysk.

Knapper, beskeder og de sætninger, der bliver bygget med tal i. Nøglen er den
danske sætning fra `app/ui/`. Pladsholderne skal være de samme i begge sprog.
"""

WORDS: dict[str, str] = {
    'Tryk Find bedste afgangstider først, og vælg en afgang. Så '
        'skriver vi sejlplanen.':
        'Drücke zuerst Beste Abfahrtszeiten finden und wähle eine '
        'Abfahrt. Dann schreiben wir den Segelplan.',
    '{sm} sømil · kurs {grader}° {retning}':
        '{sm} Seemeilen · Kurs {grader}° {retning}',
    'Lægger ruten udenom land…':
        'Die Route wird um das Land herum gelegt…',
    'Klik på kortet, eller søg efter en havn, for at sætte '
        'afgangshavnen':
        'Klicke auf die Karte oder suche einen Hafen, um den '
        'Abfahrtshafen zu setzen',
    'Klik igen for at sætte destinationen':
        'Klicke noch einmal, um das Ziel zu setzen',
    'Læg først en rute med mindst to punkter — så kan vi regne '
        'afgangstider ud.':
        'Lege zuerst eine Route mit mindestens zwei Punkten — dann können '
        'wir Abfahrtszeiten rechnen.',
    'Hele sejlplanen er kopieret':
        'Der ganze Segelplan ist kopiert',
    'Punkt {nr} flyttet til {navn}':
        'Punkt {nr} verschoben nach {navn}',
    'Ruten er vendt om':
        'Die Route ist umgekehrt',
    '"{navn}" er åbnet':
        '„{navn}“ ist geöffnet',
    'Henter vejrudsigt for hvert ben…':
        'Wetterbericht für jede Etappe wird geholt…',
    'Finder havne undervejs og gennemsejler alle afgangstider…':
        'Häfen unterwegs werden gesucht und alle Abfahrtszeiten '
        'durchgerechnet…',
    'Claude læser vejrudsigten…':
        'Claude liest den Wetterbericht…',
    'Delelink kopieret — send det til gasterne':
        'Freigabe-Link kopiert — schick ihn der Crew',
    'Søkortsymboler vist':
        'Seezeichen eingeblendet',
    'Søkortsymboler skjult':
        'Seezeichen ausgeblendet',
    'Havnene vises, når du zoomer ind. Klik på en for at lægge den i '
        'ruten.':
        'Die Häfen erscheinen, wenn du hineinzoomst. Klicke einen an, um '
        'ihn in die Route zu legen.',
    'Havnene er skjult':
        'Die Häfen sind ausgeblendet',
    '{sm} sm udenom land':
        '{sm} sm ums Land herum',
    '{kn} kn vind · {m} m bølger':
        '{kn} kn Wind · {m} m Wellen',
    'Kunne ikke finde positionen.':
        'Wir konnten die Position nicht finden.',
    'Ruten er ændret — find afgangstiderne igen':
        'Die Route hat sich geändert — suche die Abfahrtszeiten neu',
    '{navn} tilføjet':
        '{navn} hinzugefügt',
    '{navn} lagt ind som stop nr. {nr}':
        '{navn} als Zwischenstopp Nr. {nr} eingefügt',
    'Som ny destination, efter {navn}':
        'Als neues Ziel, nach {navn}',
    'Som ny afgang, før {navn}':
        'Als neue Abfahrt, vor {navn}',
    'Ruten kunne ikke åbnes':
        'Die Route konnte nicht geöffnet werden',
    'Tilføj mindst to punkter først':
        'Füge zuerst mindestens zwei Punkte hinzu',
    'Ingen afgange passer til dine grænser. Prøv et bredere '
        'datointerval, et længere sejldøgn eller en højere vindgrænse.':
        'Keine Abfahrt passt zu deinen Grenzen. Versuche einen größeren '
        'Datumsbereich, ein längeres Etmal oder eine höhere Windgrenze.',
    'Turen kan ikke nås inden kl. {tid}:00. Se forslagene — de fleste '
        'kræver en overnatning undervejs.':
        'Der Törn ist nicht vor {tid}:00 Uhr zu schaffen. Sieh dir die '
        'Vorschläge an — die meisten brauchen eine Übernachtung '
        'unterwegs.',
    'Der er ingen rute at dele endnu':
        'Es gibt noch keine Route zum Teilen',
    'Der er ingen rute at eksportere endnu':
        'Es gibt noch keine Route zum Exportieren',
    'Ingen steder hedder "{navn}". Prøv et andet navn, eller tast en '
        'position som 55.69, 12.60.':
        'Kein Ort heißt „{navn}“. Versuche einen anderen Namen, oder '
        'tippe eine Position wie 55.69, 12.60 ein.',
    '{afgange} at vælge imellem, fordelt på {dage}. Vi vil pege på '
        '<b>{bedste}</b> — men vælg selv.':
        '{afgange} zur Auswahl, verteilt auf {dage}. Wir empfehlen '
        '<b>{bedste}</b> — aber wähle selbst.',
    'stræk':
        'Abschnitte',
    'Kraftigst omkring {tid}: {kn} kn ({styrke}) fra {retning}, kast '
        'op til {kast} kn.':
        'Am stärksten gegen {tid}: {kn} kn ({styrke}) aus {retning}, Böen '
        'bis {kast} kn.',
    'Der er land her. Vælg et sted i vandet, eller søg efter en havn.':
        'Hier ist Land. Wähle eine Stelle im Wasser, oder suche einen '
        'Hafen.',
    'Som nyt punkt':
        'Als neuer Punkt',
    'Mellem {a} og {b}':
        'Zwischen {a} und {b}',
    '{afgange} fundet. Turen kræver {overnatninger} undervejs — '
        'første stop i {havn}.':
        '{afgange} gefunden. Der Törn braucht {overnatninger} unterwegs — '
        'erster Stopp in {havn}.',
    '{n} afgangstider fundet':
        '{n} Abfahrtszeiten gefunden',
    'Havkort med dybdeforhold':
        'Seekarte mit Tiefenangaben',
    'Almindeligt kort med veje og byer':
        'Gewöhnliche Karte mit Straßen und Orten',
    'Vis alle lystbådehavne — klik på en for at lægge den i ruten':
        'Alle Sportboothäfen zeigen — klicke einen an, um ihn in die '
        'Route zu legen',
    'Bøjer, fyr og sejlløb fra OpenSeaMap':
        'Tonnen, Feuer und Fahrwasser von OpenSeaMap',
    'Zoom ud, så hele ruten er i billedet':
        'Herauszoomen, bis die ganze Route im Bild ist',
    'Fremme efter sejldøgnet':
        'Nach dem Etmal am Ziel',
    '{n} t frarådes':
        '{n} Std abgeraten',
    '{n} t skærpet':
        '{n} Std anspruchsvoll',
    'Planen står til højre. Vælg en anden afgang her, så skrives den '
        'om med det samme.':
        'Der Plan steht rechts. Wähle hier eine andere Abfahrt, dann wird '
        'er sofort neu geschrieben.',
    'sm':
        'sm',
    'Farten er over grunden — strømmen er regnet med, og står i '
        'søjlen Strøm: {kn} knob {retning} i snit. Tallene kommer fra en '
        'global havmodel, der ikke opløser de danske bælter helt. I '
        'Storebælt og Grønsund kan der løbe mere, end den viser.':
        'Die Fahrt ist über Grund — der Strom ist eingerechnet und steht '
        'in der Spalte Strom: {kn} Knoten {retning} im Schnitt. Die '
        'Zahlen stammen aus einem globalen Meeresmodell, das die '
        'dänischen Belte nicht vollständig auflöst. Im Großen Belt und im '
        'Grønsund kann mehr laufen, als es zeigt.',
    'Meld om der er plads i en havn omkring dig':
        'Melde, ob in einem Hafen um dich herum Platz ist',
    'Søger…':
        'Wird gesucht…',
    'Et ben kunne ikke lægges sikkert udenom land — kontrollér det '
        'selv på søkortet.':
        'Eine Etappe ließ sich nicht sicher um das Land herum legen — '
        'prüfe sie selbst auf der Seekarte.',
    'også nat':
        'auch nachts',
    'Gå tilbage til Rute og tryk "Find bedste afgangstider".':
        'Geh zurück zu Route und drücke „Beste Abfahrtszeiten finden“.',
    'afgang':
        'Abfahrt',
    'afgange':
        'Abfahrten',
    'dag':
        'Tag',
    'dage':
        'Tage',
    '{n} t mørke':
        '{n} Std Dunkelheit',
    'når {nået} af {ialt} sømil':
        'schafft {nået} von {ialt} Seemeilen',
    'ankomst {tid}':
        'Ankunft {tid}',
    'l':
        'l',
    'Ingen bølgeprognose for dette farvand — vurder søgangen ud fra '
        'vind og stræk.':
        'Keine Wellenvorhersage für dieses Revier — schätze den Seegang '
        'aus Wind und Streichlänge ab.',
    'Få en skippervurdering':
        'Hol dir eine Skipper-Einschätzung',
    'En erfaren sejlkonsulent gennemgår ruten ben for ben og '
        'anbefaler, hvornår du bør kaste los.':
        'Ein erfahrener Segelberater geht die Route Etappe für Etappe '
        'durch und empfiehlt, wann du ablegen solltest.',
    '{punkter} og den beregnede plan forsvinder. Det kan ikke '
        'fortrydes.':
        '{punkter} und der berechnete Plan verschwinden. Das lässt sich '
        'nicht rückgängig machen.',
    '{n} t motor':
        '{n} Std Motor',
    'under vejs':
        'unterwegs',
    '{båd} · afgang {tid} · {hale}':
        '{båd} · Abfahrt {tid} · {hale}',
    'Overnatning i {havn}, {sted}. {sm} sømil ind fra ruten. Videre '
        '{tid} næste morgen.':
        'Übernachtung in {havn}, {sted}. {sm} Seemeilen von der Route ab. '
        'Weiter {tid} am nächsten Morgen.',
    'med':
        'mit',
    'imod':
        'gegen',
    'punkt':
        'Punkt',
    '{sm} sømil ekstra':
        '{sm} Seemeilen extra',
    'Vælg en anden afgang':
        'Eine andere Abfahrt wählen',
    'Læs om havnen i havnelods.dk →':
        'Über den Hafen nachlesen bei havnelods.dk →',

    # ── Anden runde: dialoger og sider ─────────────────────────
    'Tak — {havn} står nu som "{svar}".':
        'Danke — {havn} steht jetzt als „{svar}“.',
    'Du har meldt rigeligt i dag. Prøv igen i morgen.':
        'Du hast heute genug gemeldet. Versuche es morgen wieder.',
    '{havn} — din melding hjælper den, der kommer i eftermiddag. Den '
        'står i halvandet døgn og forsvinder så af sig selv.':
        '{havn} — deine Meldung hilft dem, der heute Nachmittag kommt. '
        'Sie steht anderthalb Tage und verschwindet dann von selbst.',
    'Meldingen er anonym, og der er ikke andet at skrive: kun havnen, '
        'svaret og hvornår. Så findes der ikke et sted i Sejlplan, hvor '
        'nogen kan skrive noget til nogen — og dermed heller ikke noget '
        'at moderere.':
        'Die Meldung ist anonym, und es gibt nichts weiter zu schreiben: '
        'nur den Hafen, die Antwort und den Zeitpunkt. So gibt es in '
        'Segelplan keine Stelle, an der jemand jemandem etwas schreiben '
        'kann — und damit auch nichts zu moderieren.',
    'Sejlplan fra ende til anden. Det samme står i boblerne ude i '
        'programmet — her er det bare samlet.':
        'Segelplan von vorn bis hinten. Dasselbe steht in den Blasen '
        'draußen im Programm — hier ist es nur gesammelt.',
    '{navn} er gemt og valgt':
        '{navn} ist gespeichert und ausgewählt',
    'Anslået {kn} knob for halvvind i 10 knobs vind, regnet af '
        'sejlareal, deplacement og vandlinje. Kender du din båds rigtige '
        'tal, så ret det nedenfor.':
        'Geschätzte {kn} Knoten bei halbem Wind und 10 Knoten, errechnet '
        'aus Segelfläche, Verdrängung und Wasserlinie. Kennst du die '
        'echten Werte deines Bootes, dann ändere sie unten.',
    'Længde, fart og forbrug. Så regner planen på din båd i stedet '
        'for på et eksempel.':
        'Länge, Fahrt und Verbrauch. Dann rechnet der Plan mit deinem '
        'Boot statt mit einem Beispiel.',
    'Over de her værdier markerer planen timerne som skærpede.':
        'Über diesen Werten markiert der Plan die Stunden als '
        'anspruchsvoll.',
    'Skroget afgør, hvor meget søen tager af farten. En planende båd '
        'taber mest.':
        'Der Rumpf entscheidet, wie viel der Seegang von der Fahrt nimmt. '
        'Ein Gleiter verliert am meisten.',
    'Det ene tal skalerer et almindeligt polardiagram, så farten '
        'passer til din båd. Ved du det ikke, så gæt på en god dag med '
        'fuld sejlføring.':
        'Diese eine Zahl skaliert ein gewöhnliches Polardiagramm so, dass '
        'die Fahrt zu deinem Boot passt. Weißt du sie nicht, dann schätze '
        'einen guten Tag unter vollen Segeln.',
    'Ingen båd med det navn i registret. Tast målene ind nedenfor i '
        'stedet.':
        'Kein Boot dieses Namens im Register. Trage die Maße stattdessen '
        'unten ein.',
    'i dag':
        'heute',
    'Der er ingen rute at gemme':
        'Es gibt keine Route zum Speichern',
    'tidligere':
        'früher',
    '"{navn}" er gemt':
        '„{navn}“ ist gespeichert',
    '{punkter} · {sm} sømil':
        '{punkter} · {sm} Seemeilen',
    'Læg en rute, og tryk Gem. Så ligger den her næste gang — også '
        'hvis du lukker fanen.':
        'Lege eine Route und drücke Speichern. Dann liegt sie beim '
        'nächsten Mal hier — auch wenn du den Tab schließt.',
    '{punkter} · {sm} sømil · gemt {hvornår}':
        '{punkter} · {sm} Seemeilen · gespeichert {hvornår}',
    '"{navn}" forsvinder. Det kan ikke fortrydes.':
        '„{navn}“ verschwindet. Das lässt sich nicht rückgängig machen.',
    'Uden navn':
        'Ohne Namen',
    'Sejlplan – find den bedste afgang':
        'Segelplan – finde die beste Abfahrt',
    'Rute åbnet: {fra} → {til}':
        'Route geöffnet: {fra} → {til}',
    'Delelinket kunne ikke læses':
        'Der Freigabe-Link ließ sich nicht lesen',
    'Indstillingerne er sat tilbage til standard':
        'Die Einstellungen sind auf den Standard zurückgesetzt',
    'Browseren kunne ikke installere appen herfra.':
        'Der Browser konnte die App von hier aus nicht installieren.',
    'Slået til lægges der ingen overnatninger ind — turen sejles i ét '
        'stræk, og mørketimerne tælles for sig.':
        'Eingeschaltet werden keine Übernachtungen eingelegt — der Törn '
        'wird in einem Rutsch gesegelt, und die Dunkelstunden werden '
        'gesondert gezählt.',
    'Under 3 knobs fart tændes motoren i beregningen.':
        'Unter drei Knoten Fahrt wird der Motor in der Berechnung '
        'angeworfen.',
    'Tidligst ud af havn':
        'Frühestens aus dem Hafen',
    'Senest i havn igen':
        'Spätestens wieder im Hafen',
    'Farten kommer fra polardiagrammet.':
        'Die Fahrt kommt aus dem Polardiagramm.',
    'Farten er marchfarten, minus det søen tager.':
        'Die Fahrt ist die Marschfahrt, minus dem, was die See nimmt.',
    'Over disse værdier markeres timerne som skærpede, og et stykke '
        'over dem som frarådede. Bølgehøjden vejes efter hvor søen kommer '
        'fra — modsø tæller hårdere end medsø.':
        'Über diesen Werten werden die Stunden als anspruchsvoll '
        'markiert, ein gutes Stück darüber als abgeraten. Die Wellenhöhe '
        'wird danach gewichtet, woher die See kommt — Gegensee zählt '
        'härter als mitlaufende See.',
    'Vejrudsigten rækker til og med {dato}.':
        'Die Vorhersage reicht bis einschließlich {dato}.',
    'Det tidsrum, du vil ligge og sejle i. Slutklokkeslættet er ikke '
        'et ønske om at afgå senest da — det er hvornår du vil ligge '
        'fortøjet. Rækker turen ikke, deler planlæggeren den og finder en '
        'havn undervejs at overnatte i.':
        'Der Zeitraum, in dem du segeln willst. Die Endzeit ist kein '
        'Wunsch, spätestens dann abzulegen — sie ist, wann du festgemacht '
        'liegen willst. Reicht der Törn nicht, teilt der Planer ihn und '
        'sucht einen Hafen unterwegs zum Übernachten.',
    'Vælg den, der ligner din mest, hvis du ikke vil taste din egen '
        'ind.':
        'Wähle das, welches deinem am ähnlichsten ist, wenn du deins '
        'nicht eintragen willst.',
    'Det giver {n} timers sejlads i døgnet.':
        'Das ergibt {n} Stunden Fahrt am Tag.',
    'Så åbner Sejlplan i sit eget vindue — og den seneste sejlplan '
        'kan læses uden dækning.':
        'Dann öffnet sich Segelplan in einem eigenen Fenster — und der '
        'letzte Segelplan lässt sich ohne Empfang lesen.',
    '{sm} sømil sejlet':
        '{sm} Seemeilen gesegelt',
    '{sm} tilbage':
        'noch {sm}',
    '{kn} knob i snit':
        '{kn} Knoten im Schnitt',
    'Du er {n} minutter {dom}':
        'Du bist {n} Minuten {dom}',
    'Du er {n} timer {dom}':
        'Du bist {n} Stunden {dom}',
    'Med den fart er du fremme {tid}.':
        'Mit dieser Fahrt bist du {tid} da.',
    'Du er {sm} sømil fra ruten. Så længe det er sådan, kan vi ikke '
        'sige, om du er foran eller bagud.':
        'Du bist {sm} Seemeilen von der Route entfernt. Solange das so '
        'ist, können wir nicht sagen, ob du voraus oder zurück bist.',
    'Læg først en rute med mindst to punkter':
        'Lege zuerst eine Route mit mindestens zwei Punkten',
    'Skriv en mailadresse, vi kan skrive til':
        'Schreibe eine E-Mail-Adresse, an die wir schreiben können',
    'Vinduet ligger i fortiden':
        'Das Fenster liegt in der Vergangenheit',
    'Vi har skrevet til {adresse}. Bekræft i mailen, så går vagten i '
        'gang.':
        'Wir haben an {adresse} geschrieben. Bestätige in der Mail, dann '
        'läuft die Wache los.',
    'Mailen kunne ikke sendes. Prøv igen om lidt.':
        'Die Mail konnte nicht gesendet werden. Versuche es gleich noch '
        'einmal.',
    'Vælg to datoer':
        'Wähle zwei Daten',
    'Vi holder øje med {rute} og skriver til dig, når der er et '
        'vindue, du kan sejle i. Én mail — ikke en strøm af dem.':
        'Wir behalten {rute} im Auge und schreiben dir, wenn sich ein '
        'Fenster auftut, in dem du segeln kannst. Eine Mail — kein Strom '
        'davon.',
    'Prognosen rækker {døgn} døgn frem — til og med {dato}. Ligger '
        'dit vindue længere ude, venter vagten, til prognosen når derhen.':
        'Die Vorhersage reicht {døgn} Tage voraus — bis einschließlich '
        '{dato}. Liegt dein Fenster weiter draußen, wartet die Wache, bis '
        'die Vorhersage dort hinkommt.',
    'Målt mod dine egne grænser: {kn} knob og {m} meter, sejldøgn '
        '{fra}–{til}. Vi skriver kun, hvis du også kan komme hjem igen.':
        'Gemessen an deinen eigenen Grenzen: {kn} Knoten und {m} Meter, '
        'Etmal {fra}–{til}. Wir schreiben nur, wenn du auch wieder nach '
        'Hause kommst.',
    'Vi bruger din adresse til denne ene besked og sletter vagten '
        'bagefter. Du kan stoppe den når som helst med linket i mailen.':
        'Wir benutzen deine Adresse für diese eine Nachricht und löschen '
        'die Wache danach. Du kannst sie jederzeit mit dem Link in der '
        'Mail stoppen.',
    'Vejrvagt er ikke slået til':
        'Die Wetterwache ist nicht eingeschaltet',
    'Serveren har ingen postkasse at skrive fra endnu. Når den har, '
        'kan du bede Sejlplan holde øje med vejret til en tur og skrive, '
        'når der er et vindue.':
        'Der Server hat noch keinen Briefkasten, aus dem er schreiben '
        'kann. Wenn er einen hat, kannst du Segelplan bitten, für einen '
        'Törn das Wetter im Auge zu behalten und zu schreiben, wenn sich '
        'ein Fenster auftut.',
    'Vi holder øje med {rute} mellem {fra} og {til}. Du hører fra os, '
        'når der er et vindue, du kan sejle i — og kun den ene gang.':
        'Wir behalten {rute} zwischen {fra} und {til} im Auge. Du hörst '
        'von uns, wenn sich ein Fenster auftut, in dem du segeln kannst — '
        'und nur das eine Mal.',
    'Vi holder ikke længere øje med {rute}, og vi skriver ikke til '
        'dig om den igen.':
        'Wir behalten {rute} nicht länger im Auge und schreiben dir nicht '
        'wieder darüber.',
    'Linket er forkert, eller vagten er allerede stoppet.':
        'Der Link ist falsch, oder die Wache ist bereits gestoppt.',

    # ── Breve, fejlbeskeder og bådenes væsen ───────────────────
    'AI-analysen er ikke slået til på denne server. Sæt '
        'ANTHROPIC_API_KEY i .env og genstart.':
        'Die KI-Analyse ist auf diesem Server nicht eingeschaltet. Setze '
        'ANTHROPIC_API_KEY in .env und starte neu.',
    'Serverens API-nøgle blev afvist. Tjek ANTHROPIC_API_KEY.':
        'Der API-Schlüssel des Servers wurde abgelehnt. Prüfe '
        'ANTHROPIC_API_KEY.',
    'For mange forespørgsler lige nu. Prøv igen om et øjeblik.':
        'Gerade zu viele Anfragen. Versuche es gleich noch einmal.',
    'AI-tjenesten svarede med fejl {kode}.':
        'Der KI-Dienst antwortete mit Fehler {kode}.',
    'Kunne ikke få forbindelse til AI-tjenesten.':
        'Es kam keine Verbindung zum KI-Dienst zustande.',
    'sejl':
        'Segel',
    'dybgang':
        'Tiefgang',
    '{n} pladser':
        '{n} Liegeplätze',
    '{detalje} · ved {sted}':
        '{detalje} · bei {sted}',
    'Lystbådehavn':
        'Sportboothafen',
    'Position':
        'Position',
    'Ud for {sted}':
        'Vor {sted}',
    'Ukendt område':
        'Unbekanntes Gebiet',
    '{hilsen}\n\nNu er der vejr til {rute}.\n\nAfgang     {afgang}\nAnkomst    {ankomst}\nDistance   {sm} sømil\nUnder vejs {timer} timer, snit {snit} knob\nVind       op til {vind} knob\nBølger     op til {boelger} meter{ophold}\n\nÅbn turen i Sejlplan, så kan du se hele planen — dag for dag, stræk for stræk\nog time for time:\n{link}\n\nPrognosen kan nå at flytte sig. Se den efter igen dagen før, du kaster los.\n\nVagten er hermed brugt. Vil du holde øje med en ny tur, så læg en ny vagt.\nVil du stoppe den her med det samme: {stop}\n\nGod tur.\nSejlplan\n':
        '{hilsen}\n\nJetzt gibt es Wetter für {rute}.\n\nAbfahrt    {afgang}\nAnkunft    {ankomst}\nDistanz    {sm} Seemeilen\nUnterwegs  {timer} Stunden, Schnitt {snit} Knoten\nWind       bis zu {vind} Knoten\nWellen     bis zu {boelger} Meter{ophold}\n\nÖffne den Törn in Segelplan, dann siehst du den ganzen Plan — Tag für Tag,\nAbschnitt für Abschnitt und Stunde für Stunde:\n{link}\n\nDie Vorhersage kann sich noch verschieben. Sieh sie am Tag vor dem Ablegen\nnoch einmal durch.\n\nDamit ist die Wache verbraucht. Willst du einen neuen Törn im Auge behalten,\ndann lege eine neue Wache.\nWillst du diese hier sofort stoppen: {stop}\n\nGuten Törn.\nSegelplan\n',
    'Nu er der vejr til {rute}':
        'Jetzt gibt es Wetter für {rute}',
    '{hilsen}\n\nDu har bedt Sejlplan holde øje med vejret til {rute}\nmellem {fra} og {til}.\n\nBekræft, at adressen er din, så går vagten i gang:\n{ja}\n\nVi skriver én gang — når der er et vindue, du kan sejle i. Ikke oftere.\n\nVar det ikke dig, skal du ingenting gøre. Så bliver vagten aldrig aktiv, og\nden ryger af sig selv. Vil du være sikker: {stop}\n\nSejlplan\n':
        '{hilsen}\n\nDu hast Segelplan gebeten, für {rute}\nzwischen {fra} und {til} das Wetter im Auge zu behalten.\n\nBestätige, dass die Adresse deine ist, dann läuft die Wache los:\n{ja}\n\nWir schreiben ein einziges Mal — wenn sich ein Fenster auftut, in dem du\nsegeln kannst. Nicht öfter.\n\nWarst du das nicht, brauchst du nichts zu tun. Dann wird die Wache nie aktiv\nund verfällt von selbst. Willst du sichergehen: {stop}\n\nSegelplan\n',
    'Bekræft vejrvagt: {rute}':
        'Wetterwache bestätigen: {rute}',
    'Hej {navn}':
        'Hallo {navn}',
    'Hej':
        'Hallo',
    'Undervejs ligger du i {havne}.':
        'Unterwegs liegst du in {havne}.',
    'Noget gik galt her — det er ikke dig. Prøv igen, og skriv fejl '
        '{ref}, hvis det bliver ved.':
        'Hier ist etwas schiefgegangen — es liegt nicht an dir. Versuche '
        'es noch einmal, und nenne Fehler {ref}, wenn es dabei bleibt.',
    'Under vejs':
        'Unterwegs',
    'Gemt om bord {tid} · virker uden dækning':
        'An Bord gespeichert {tid} · funktioniert ohne Empfang',
    'Hentet {tid} og gemt i telefonen. Åbn Sejlplan med dækning for '
        'at regne den om.':
        'Abgerufen {tid} und im Telefon gespeichert. Öffne Segelplan mit '
        'Empfang, um ihn neu zu rechnen.',
    'for {n} dage siden':
        'vor {n} Tagen',
    'for {n} timer siden':
        'vor {n} Stunden',
    'Knæk {nr}':
        'Knick {nr}',
    'Vejrtjenesten svarer ikke. Prøv igen om lidt.':
        'Der Wetterdienst antwortet nicht. Versuche es gleich noch '
        'einmal.',
    'Vejrtjenesten returnerede ingen data for ruten.':
        'Der Wetterdienst lieferte keine Daten für die Route.',
    'Kunne ikke hente vejrdata: {fejl}':
        'Wetterdaten konnten nicht geholt werden: {fejl}',
    'Familiekrydser':
        'Familienkreuzer',
    'Klassisk krydser':
        'Klassischer Fahrtenkreuzer',
    'Fortrængningsbåd':
        'Verdränger',
    'Langturssejler':
        'Fahrtensegler',
    'Lille krydser':
        'Kleiner Fahrtenkreuzer',
    'Stor planende':
        'Großer Gleiter',
    'Weekendbåd':
        'Wochenendboot',
    'den brede middelvej':
        'der breite Mittelweg',
    'hurtig i smult vande, hård i sø':
        'schnell im glatten Wasser, hart im Seegang',
    'komfort og rækkevidde':
        'Komfort und Reichweite',
    'langsom, men uanfægtet':
        'langsam, aber unbeirrt',
    'lille, men sødygtig':
        'klein, aber seetüchtig',
    'nem at have med at gøre':
        'unkompliziert im Umgang',
    'rolig og tilgivende':
        'ruhig und nachsichtig',
    'rummelig og hurtig nok':
        'geräumig und schnell genug',
    'tåler mest af dem alle':
        'steckt am meisten weg',
    'tung':
        'schwer',
    'solid':
        'solide',
    'moderat':
        'mäßig',
    'let':
        'leicht',
    'rigeligt sejl':
        'reichlich Segel',
    'godt sejlført':
        'gut besegelt',
    'almindeligt sejlført':
        'normal besegelt',
    'beskedent sejlført':
        'knapp besegelt',
    'Min båd':
        'Mein Boot',
    'Din egen':
        'Dein eigenes',
    'Tur':
        'Törn',

    # ── Din egen båd, position og pladsmelding ─────────────────────
    'Havne omkring dig':
        'Häfen um dich herum',
    'Søgeresultater':
        'Suchergebnisse',
    'Søg havnen frem, eller vælg en af dem omkring dig.':
        'Suche den Hafen, oder wähle einen aus deiner Umgebung.',
    'Ingen havne med det navn. Prøv en anden stavemåde.':
        'Kein Hafen dieses Namens. Versuche eine andere Schreibweise.',
    'Vi ved ikke, hvor du er. Søg havnen frem foroven — eller slå "Jeg er '
        'undervejs" til.':
        'Wir wissen nicht, wo du bist. Suche den Hafen oben — oder schalte '
        '„Ich bin unterwegs“ ein.',
    'Søg efter en havn…':
        'Nach einem Hafen suchen…',
    '{km} km':
        '{km} km',
    '{m} meter':
        '{m} Meter',
    'Din båd':
        'Dein Boot',
    'Browseren giver ikke adgang til position':
        'Der Browser gibt keinen Zugriff auf die Position',
    'Uden en position er der ingen båd at vise. Prøv i en anden browser, '
        'eller på telefonen.':
        'Ohne Position gibt es kein Boot zu zeigen. Versuche es in einem '
        'anderen Browser oder auf dem Telefon.',
    'Du har sagt nej til position for den her side':
        'Du hast die Position für diese Seite abgelehnt',
    'Browseren spørger ikke igen af sig selv. Slå det til i indstillingerne '
        'for siden — i Chrome ligger det bag hængelåsen i adresselinjen.':
        'Der Browser fragt von selbst nicht noch einmal. Schalte es in den '
        'Einstellungen für die Seite ein — in Chrome liegt das hinter dem '
        'Schloss in der Adresszeile.',
    'Du sidder ved en computer':
        'Du sitzt an einem Computer',
    'En computer har ingen GPS. Den gætter positionen ud fra wifi og '
        'netværk, og det kan være kilometer ved siden af — de andre ser din '
        'båd et sted, du ikke er. På telefonen er den på få meter. Vil du '
        'vises rigtigt undervejs, så åbn Sejlplan på telefonen.':
        'Ein Computer hat kein GPS. Er schätzt die Position aus WLAN und '
        'Netzwerk, und das kann Kilometer danebenliegen — die anderen sehen '
        'dein Boot an einer Stelle, an der du nicht bist. Auf dem Telefon '
        'sind es wenige Meter. Willst du unterwegs richtig angezeigt werden, '
        'dann öffne Segelplan auf dem Telefon.',
    'Din position er kun kendt på ±{afstand}. Det er et gæt fra nettet, ikke '
        'GPS — på telefonen er den på få meter.':
        'Deine Position ist nur auf ±{afstand} genau. Das ist eine Schätzung '
        'aus dem Netz, kein GPS — auf dem Telefon sind es wenige Meter.',
    'Du er ikke synlig for andre, før browseren har fundet dig. Sig ja til '
        'position, hvis den spørger.':
        'Du bist für andere nicht sichtbar, bevor der Browser dich gefunden '
        'hat. Erlaube die Position, wenn er fragt.',
    'Beskeder fra andre både':
        'Nachrichten von anderen Booten',
    'Gode forhold':
        'Gute Bedingungen',

    '{svar} — meldt {hvornår}':
        '{svar} — gemeldet {hvornår}',
    'efter {sm} sm · {omvej} sm ind fra ruten':
        'nach {sm} sm · {omvej} sm abseits der Route',

    # ── Oversigten over både, og postbuddet ────────────────────────
    'Både i nærheden':
        'Boote in der Nähe',
    'Se hvem der er i nærheden':
        'Sieh, wer in der Nähe ist',
    'En anden båd':
        'Ein anderes Boot',
    '{navn} har skrevet til dig':
        '{navn} hat dir geschrieben',
    'har skrevet':
        'hat geschrieben',
    'båd':
        'Boot',
    'både':
        'Boote',
    'både|flertal':
        'Boote',
    'båd her':
        'Boot hier',
    'både her':
        'Boote hier',
    'både her|flertal':
        'Boote hier',
    '{sm} sm mod {retning}':
        '{sm} sm Richtung {retning}',
    'Ingen andre både i nærheden':
        'Keine anderen Boote in der Nähe',
    'Der er ingen inden for tres sømil, der har gjort sig synlig lige nu.':
        'Innerhalb von sechzig Seemeilen hat sich gerade niemand sichtbar '
        'gemacht.',
    'Du ser kun både, der også har gjort sig synlige.':
        'Du siehst nur Boote, die sich ebenfalls sichtbar gemacht haben.',
    'Vi ved ikke, hvor du er endnu':
        'Wir wissen noch nicht, wo du bist',
    'Uden en position kan vi ikke sige, hvem der er i nærheden. Sig ja til '
        'position, hvis browseren spørger.':
        'Ohne Position können wir nicht sagen, wer in der Nähe ist. Erlaube '
        'die Position, wenn der Browser fragt.',
}
