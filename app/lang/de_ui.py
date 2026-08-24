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
}
