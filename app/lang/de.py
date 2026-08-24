"""Tysk.

Nøglen er den danske sætning, præcis som den står i koden. Mangler en, står
den danske i stedet — fladen virker, den er bare ikke oversat dér endnu.
`tools/check_translations.py` siger hvilke.

Oversat, ikke maskinoversat. Sejlplan skriver som en sejler taler, og tysk
sømandssprog er ikke ord-for-ord det samme som dansk: en havn er ein Hafen, men
"sejldøgn" hedder ikke "Segeltag" — det hedder Etmal på begge sprog, og der er
ingen tysk sejler, der siger "Segelrunde". Hvor der ikke findes et tysk ord,
bruges omskrivningen, ikke en opfindelse.
"""

WORDS: dict[str, str] = {

    # ── Trinnene og hovedknapperne ──────────────────────────────────
    'Rute': 'Route',
    'Afgangstid': 'Abfahrtszeit',
    'Sejlplan': 'Segelplan',
    'Find bedste afgangstider': 'Beste Abfahrtszeiten finden',
    'Se sejlplanen': 'Segelplan ansehen',
    'Kortet': 'Karte',
    'Udskriv': 'Drucken',
    'Kopiér': 'Kopieren',
    'Gem': 'Speichern',
    'Fortryd': 'Abbrechen',
    'Annullér': 'Abbrechen',
    'Færdig': 'Fertig',
    'Luk': 'Schließen',
    'Nulstil': 'Zurücksetzen',
    'Ret': 'Ändern',
    'Slet': 'Löschen',
    'Omdøb': 'Umbenennen',
    'Behold': 'Behalten',
    'Ryd': 'Leeren',
    'Se alle': 'Alle ansehen',
    'Installér': 'Installieren',
    'Hent': 'Herunterladen',
    'Stop': 'Stopp',
    'Tilbage til ruten': 'Zurück zur Route',

    # ── Søgning og ruten ────────────────────────────────────────────
    'Søg havn, ø eller position…': 'Hafen, Insel oder Position suchen…',
    'Ruten': 'Die Route',
    'Turen': 'Die Reise',
    'Afgang': 'Abfahrt',
    'Destination': 'Ziel',
    'Mellemstop': 'Zwischenstopp',
    'Læg din rute': 'Route anlegen',
    'Kom hurtigt i gang': 'Schnell loslegen',
    'Vis på kortet': 'Auf der Karte zeigen',
    'Søkort': 'Seekarte',
    'Landkort': 'Landkarte',
    'Havne': 'Häfen',
    'Sømærker': 'Seezeichen',
    'Hele ruten': 'Ganze Route',
    'Søg efter en havn foroven, klik direkte på kortet, eller slå '
    'havnelaget til og vælg en havn. Du skal bruge mindst to punkter.':
        'Suche oben nach einem Hafen, klicke direkt auf die Karte oder '
        'schalte die Hafenebene ein. Du brauchst mindestens zwei Punkte.',
    'Tilføj mindst ét punkt mere for at kunne beregne afgangstider.':
        'Füge mindestens einen weiteren Punkt hinzu, damit Abfahrtszeiten '
        'berechnet werden können.',

    # ── Båden ───────────────────────────────────────────────────────
    'Båd': 'Boot',
    'Din båd': 'Dein Boot',
    'Sejlbåd': 'Segelboot',
    'Motorbåd': 'Motorboot',
    'Navn': 'Name',
    'Type': 'Typ',
    'Længde overalt': 'Länge über alles',
    'Marchfart i smult vande': 'Marschfahrt in ruhigem Wasser',
    'Skrogtype': 'Rumpfform',
    'Fortrængning': 'Verdränger',
    'Halvplanende': 'Halbgleiter',
    'Planende': 'Gleiter',
    'Forbrug ved marchfart': 'Verbrauch bei Marschfahrt',
    'Forbrug for motor': 'Verbrauch unter Motor',
    'Fart for motor': 'Geschwindigkeit unter Motor',
    'Fart for halvvind i 10 knobs vind':
        'Geschwindigkeit auf halbem Wind bei 10 Knoten',
    'Find din båd': 'Dein Boot finden',
    'Læg din egen båd ind': 'Eigenes Boot anlegen',
    'Gem båden': 'Boot speichern',
    'Eller et eksempel': 'Oder ein Beispiel',
    'Sejlbåde': 'Segelboote',
    'Motorbåde': 'Motorboote',
    'Hvad du kan holde til': 'Was du aushältst',
    'Højeste vind': 'Höchster Wind',
    'Højeste bølger': 'Höchste Wellen',
    'Komfortgrænser': 'Komfortgrenzen',
    'Grænser': 'Grenzen',
    'Giv båden et navn': 'Gib dem Boot einen Namen',

    # ── Tid ─────────────────────────────────────────────────────────
    'Hvornår': 'Wann',
    'Sejldøgn': 'Etmal',
    'Hvornår kan du afgå': 'Wann kannst du ablegen',
    'Tidligst afgang': 'Frühestens',
    'Senest afgang': 'Spätestens',
    'Tidligst': 'Frühestens',
    'Senest': 'Spätestens',
    'Sejlads': 'Fahrt',
    'Sejl også om natten': 'Auch nachts segeln',
    'Brug motor i svag vind': 'Motor bei wenig Wind',

    # ── Sejlplanen ──────────────────────────────────────────────────
    'Overblik': 'Überblick',
    'Vær opmærksom på': 'Zu beachten',
    'Nøgletal': 'Kennzahlen',
    'Dag for dag': 'Tag für Tag',
    'Stræk for stræk': 'Schlag für Schlag',
    'Time for time': 'Stunde für Stunde',
    'Skippervurdering': 'Skipper-Einschätzung',
    'Havne undervejs': 'Häfen unterwegs',
    'Sejltid': 'Fahrzeit',
    'Gns. fart': 'Ø-Fahrt',
    'Distance': 'Distanz',
    'Frarådet': 'Abgeraten',
    'Brændstof': 'Kraftstoff',
    'God': 'Gut',
    'Skærpet': 'Verschärft',
    'Frarådes': 'Abgeraten',
    'Tid': 'Zeit',
    'Vind': 'Wind',
    'Fra': 'Aus',
    'Bølger': 'Wellen',
    'Fart': 'Fahrt',
    'Strøm': 'Strom',
    'Sejlføring': 'Segelstellung',
    'Søen': 'Seegang',
    'Ingen beregning endnu': 'Noch keine Berechnung',
    'Steder du kan søge ind, hvis vejret skifter. Klik for at lægge '
    'en ind som mellemstop.':
        'Häfen, in die du bei Wetterumschwung einlaufen kannst. Klicke, um '
        'einen als Zwischenstopp einzufügen.',
    'Havneguide ↗': 'Hafenführer ↗',
    'Ruten er delt op efter kursskift, så hvert stykke gælder præcis '
    'dér, hvor du styrer den kurs.':
        'Die Route ist nach Kurswechseln geteilt, damit jeder Abschnitt genau '
        'dort gilt, wo du diesen Kurs steuerst.',

    # ── Mine ruter ──────────────────────────────────────────────────
    'Mine ruter': 'Meine Routen',
    'Mine gemte ruter': 'Meine gespeicherten Routen',
    'Gem ruten': 'Route speichern',
    'Gem ændringer': 'Änderungen speichern',
    'Gem som ny': 'Als neue speichern',
    'Slet ruten?': 'Route löschen?',
    'Ingen gemte ruter endnu': 'Noch keine gespeicherten Routen',
    'Omdøb ruten': 'Route umbenennen',
    'Ruten er slettet': 'Route gelöscht',
    'Ruten er ryddet': 'Route geleert',
    'Ryd hele ruten?': 'Ganze Route löschen?',
    'Ryd hele ruten': 'Ganze Route löschen',
    'Vend ruten om': 'Route umkehren',
    'Kopiér delelink': 'Teilen-Link kopieren',
    'Hent GPX til kortplotter': 'GPX für den Kartenplotter',
    'Del eller eksportér ruten': 'Route teilen oder exportieren',

    # ── Appen ───────────────────────────────────────────────────────
    'Appen': 'Die App',
    'Manual': 'Handbuch',
    'Manual og hjælp': 'Handbuch und Hilfe',
    'Indstillinger': 'Einstellungen',
    'Båd, grænser og sejldøgn': 'Boot, Grenzen und Etmal',
    'Skift mellem lyst og mørkt': 'Hell oder dunkel',
    'Sprog': 'Sprache',
    'Læg på hjemmeskærmen': 'Zum Startbildschirm',
    'Sejlplan kører allerede som app.': 'Segelplan läuft bereits als App.',
    'Tryk på Del nederst i Safari, og vælg "Føj til hjemmeskærm".':
        'Tippe unten in Safari auf Teilen und wähle "Zum Home-Bildschirm".',

    # ── Havnemeldinger ──────────────────────────────────────────────
    'Er der plads?': 'Ist ein Platz frei?',
    'Meld plads': 'Platz melden',
    'God plads': 'Viel Platz',
    'Få pladser': 'Wenige Plätze',
    'Fuld': 'Belegt',
    'lige nu': 'gerade eben',
    'for en time siden': 'vor einer Stunde',
    'i går': 'gestern',

    # ── Vejrvagt ────────────────────────────────────────────────────
    'Vejrvagt': 'Wetterwache',
    'Hold øje med vejret': 'Aufs Wetter achten',
    'Hold øje': 'Achten',
    'Dit navn (valgfrit)': 'Dein Name (freiwillig)',
    'Din mailadresse': 'Deine E-Mail-Adresse',
    'Hvornår kan I komme afsted?': 'Wann könnt ihr los?',
    'Hvor godt skal det være?': 'Wie gut soll es sein?',
    'Kun gode forhold': 'Nur gute Bedingungen',
    'Også skærpede': 'Auch verschärfte',
    'Vagten er i gang': 'Die Wache läuft',
    'Vagten er stoppet': 'Die Wache ist beendet',
    'Vagten findes ikke': 'Diese Wache gibt es nicht',
    'Stop vagten': 'Wache beenden',
    'Åbn Sejlplan': 'Segelplan öffnen',

    # ── Undervejs ───────────────────────────────────────────────────
    'Undervejs': 'Unterwegs',
    'Jeg er undervejs': 'Ich bin unterwegs',
    'Følg med i, om du er foran eller bagud.':
        'Verfolge, ob du vor oder hinter dem Plan liegst.',
    'Leder efter positionen…': 'Position wird gesucht…',
    'Du følger planen': 'Du liegst im Plan',
    'foran': 'voraus',
    'bagud': 'zurück',
    'Du er fremme. God tur — og velkommen i havn.':
        'Du bist da. Gute Fahrt — und willkommen im Hafen.',
    'Turen er ikke begyndt endnu — afgangen ligger frem i tiden. '
    'Når du har kastet los, står der her, om du er foran eller '
    'bagud.':
        'Die Reise hat noch nicht begonnen — die Abfahrt liegt in der '
        'Zukunft. Sobald du abgelegt hast, steht hier, ob du vor oder hinter '
        'dem Plan liegst.',
    'Positionen bliver på din telefon. Den gemmes ikke, og ingen '
    'andre kan se den.':
        'Die Position bleibt auf deinem Telefon. Sie wird nicht gespeichert, '
        'und niemand sonst kann sie sehen.',

    # ── Andre både ──────────────────────────────────────────────────
    'Vis din båd på kortet': 'Dein Boot auf der Karte zeigen',
    'Vis min båd for andre': 'Mein Boot für andere sichtbar machen',
    'Bådens navn': 'Name des Bootes',
    'Vis mig': 'Zeig mich',
    'Skjul mig': 'Verbergen',
    'Du er synlig som': 'Du bist sichtbar als',
    'Ingen andre både i nærheden lige nu.':
        'Gerade keine anderen Boote in der Nähe.',
    '{n} andre både i nærheden.': '{n} andere Boote in der Nähe.',
    'Giv båden et navn, de andre kan se':
        'Gib dem Boot einen Namen, den die anderen sehen',
    'Så kan andre, der også er synlige, se hvor du er — og '
    'du kan se dem. Kun jer, der har slået det til.':
        'Dann sehen andere, die ebenfalls sichtbar sind, wo du bist — und du '
        'siehst sie. Nur ihr, die es eingeschaltet habt.',
    'Skriv bådens navn, ikke dit eget. Det er dét, de '
    'andre ser.':
        'Schreibe den Namen des Bootes, nicht deinen eigenen. Das ist es, was '
        'die anderen sehen.',
    'Du er usynlig, indtil du selv tænder — og du '
    'forsvinder igen i samme øjeblik, du slukker.':
        'Du bist unsichtbar, bis du selbst einschaltest — und du verschwindest '
        'wieder in dem Moment, in dem du ausschaltest.',
    'Positionen udløber af sig selv efter en halv time '
    'uden opdatering.':
        'Die Position läuft nach einer halben Stunde ohne Aktualisierung von '
        'selbst ab.',
    'Der gemmes ingen historik. Hver ny position skriver '
    'den forrige over, så ingen kan slå op, hvor du var '
    'i går.':
        'Es wird kein Verlauf gespeichert. Jede neue Position überschreibt die '
        'vorige, sodass niemand nachsehen kann, wo du gestern warst.',
    'Du ser kun andre, mens du selv er synlig. Ingen kan '
    'kigge uden at være der selv.':
        'Du siehst andere nur, solange du selbst sichtbar bist. Niemand kann '
        'zusehen, ohne selbst dabei zu sein.',
    'Din båd er nu synlig for andre, der også er det.':
        'Dein Boot ist jetzt für andere sichtbar, die es ebenfalls sind.',
    'Du er ikke længere synlig, og din position er slettet.':
        'Du bist nicht mehr sichtbar, und deine Position wurde gelöscht.',

    # ── Beskeder ────────────────────────────────────────────────────
    'Beskeder': 'Nachrichten',
    'Skriv en kort besked…': 'Kurze Nachricht schreiben…',
    'Send': 'Senden',
    'Anmeld': 'Melden',
    'Bloker': 'Blockieren',
    'Bloker denne båd': 'Dieses Boot blockieren',
    'er blokeret': 'ist blockiert',
    'Ingen beskeder': 'Keine Nachrichten',
    'Ingen beskeder endnu. Skriv den første.':
        'Noch keine Nachrichten. Schreib die erste.',
    'Beskeder forsvinder efter et døgn.':
        'Nachrichten verschwinden nach einem Tag.',
    'Tryk på en båd på kortet for at skrive til den.':
        'Tippe auf ein Boot auf der Karte, um ihm zu schreiben.',
    'I kan ikke længere skrive til hinanden, og I kan '
    'ikke se hinanden på kortet. Det gælder begge veje.':
        'Ihr könnt einander nicht mehr schreiben und seht euch nicht mehr auf '
        'der Karte. Das gilt in beide Richtungen.',
    'Beskeden er anmeldt. Vi gemmer den, så den kan ses '
    'efter.':
        'Die Nachricht wurde gemeldet. Wir bewahren sie auf, damit sie geprüft '
        'werden kann.',
    'Venter på din position…': 'Warte auf deine Position…',
    'Du er ikke synlig for andre, før telefonen '
    'har fundet dig. Sig ja til position, hvis '
    'browseren spørger.':
        'Du bist für andere nicht sichtbar, bevor das Telefon dich gefunden '
        'hat. Erlaube den Standort, wenn der Browser fragt.',
    'Meld plads': 'Platz melden',
    'Havnene omkring dig, nærmeste først. Vælg den, du '
    'ligger i.':
        'Die Häfen um dich herum, der nächste zuerst. Wähle den, in dem du '
        'liegst.',

    # ── Enheder og småord ───────────────────────────────────────────
    'sømil': 'Seemeilen',
    'knob': 'Knoten',
    'meter': 'Meter',
    'timer': 'Stunden',
    'time': 'Stunde',
    'døgn': 'Tage',
    'nat': 'Nacht',
    'nætter': 'Nächte',
    'overnatning': 'Übernachtung',
    'overnatninger': 'Übernachtungen',
    'punkter': 'Punkte',
    'motor': 'Motor',
    'i alt': 'insgesamt',

    # ── Manualens ramme og småting ──────────────────────────────────
    'Manual': 'Handbuch',
    'Hentet': 'Abgerufen',
    'Sprog / Sprache': 'Sprache',
    'Find den bedste afgang, og tag sejlplanen med til søs. Her står, hvad '
    'tallene betyder, og hvad du selv skal tage stilling til.':
        'Finde die beste Abfahrt und nimm den Segelplan mit an Bord. Hier '
        'steht, was die Zahlen bedeuten und worüber du selbst entscheiden '
        'musst.',
    'sejldøgn': 'Etmal',
    'ben': 'Etappe',
    'Ingen havne i nærheden': 'Keine Häfen in der Nähe',
    'Vi ved ikke, hvor du er. Slå "Jeg er undervejs" til, eller læg en rute '
    'først.':
        'Wir wissen nicht, wo du bist. Schalte „Ich bin unterwegs“ ein oder '
        'lege zuerst eine Route.',
    'Beskeden findes ikke længere.': 'Die Nachricht gibt es nicht mehr.',
    'Kunne ikke sendes': 'Konnte nicht gesendet werden',

    # ── Ugedage, måneder og tidsenheder ─────────────────────────────
    'mandag': 'Montag', 'tirsdag': 'Dienstag', 'onsdag': 'Mittwoch',
    'torsdag': 'Donnerstag', 'fredag': 'Freitag', 'lørdag': 'Samstag',
    'søndag': 'Sonntag',
    'man': 'Mo', 'tir': 'Di', 'ons': 'Mi', 'tor': 'Do', 'fre': 'Fr',
    'lør': 'Sa', 'søn': 'So',
    'januar': 'Januar', 'februar': 'Februar', 'marts': 'März',
    'april': 'April', 'maj': 'Mai', 'juni': 'Juni', 'juli': 'Juli',
    'august': 'August', 'september': 'September', 'oktober': 'Oktober',
    'november': 'November', 'december': 'Dezember',
    'jan': 'Jan', 'feb': 'Feb', 'mar': 'Mär', 'apr': 'Apr', 'jun': 'Jun',
    'jul': 'Jul', 'aug': 'Aug', 'sep': 'Sep', 'okt': 'Okt', 'nov': 'Nov',
    'dec': 'Dez',
    # Timer, døgn og minutter. Korte af en grund: de står inde i sætninger.
    't': 'Std', 'd': 'T', 'min': 'Min',

    # ── Kompasset ───────────────────────────────────────────────────
    # Dansk skriver Ø for øst og V for vest; tysk skriver O og W.
    'NNØ': 'NNO', 'NØ': 'NO', 'ØNØ': 'ONO', 'Ø': 'O', 'ØSØ': 'OSO',
    'SØ': 'SO', 'SSØ': 'SSO', 'SSV': 'SSW', 'SV': 'SW', 'VSV': 'WSW',
    'V': 'W', 'VNV': 'WNW', 'NV': 'NW', 'NNV': 'NNW',

    # ── Vindstyrke ──────────────────────────────────────────────────
    # Beauforts skala har sine egne tyske navne. De er ikke oversættelser
    # af de danske — de er de ord, der står i en tysk farvandsudsigt.
    'Stille': 'Windstille',
    'Svag vind': 'leiser Zug',
    'Let vind': 'leichte Brise',
    'Let brise': 'schwache Brise',
    'Jævn vind': 'mäßige Brise',
    'Frisk vind': 'frische Brise',
    'Kuling': 'starker Wind',
    'Hård kuling': 'steifer Wind',
    'Stormende kuling': 'stürmischer Wind',
    'Storm': 'Sturm',
    'Orkan': 'Orkan',

    # ── Sejlføring, halse og sø ─────────────────────────────────────
    'i vindøjet': 'im Wind',
    'skarp bidevind': 'hart am Wind',
    'bidevind': 'am Wind',
    'halvvind': 'halber Wind',
    'rumskøds': 'raumer Wind',
    'læns': 'vor dem Wind',
    'styrbords halse': 'Steuerbordbug',
    'bagbords halse': 'Backbordbug',
    'lige forfra': 'genau von vorn',
    'lige agterfra': 'genau von achtern',
    'modsø': 'Gegensee',
    'tværsø': 'querlaufende See',
    'medsø': 'mitlaufende See',
    'smult vande': 'glattes Wasser',

    # ── Timernes dom ────────────────────────────────────────────────
    'God': 'Gut',
    'Skærpet': 'Anspruchsvoll',
    'Frarådes': 'Abgeraten',

    # ── Flertalsformer ──────────────────────────────────────────────
    # Dansk siger "to sejldøgn", tysk siger "zwei Etmale". Nøglen med
    # |flertal slås op, når tallet er større end ét.
    'sejldøgn|flertal': 'Etmale',
    'ben|flertal': 'Etappen',
    'døgn': 'Tag',
    'døgn|flertal': 'Tage',
    'time': 'Stunde',
    'timer|flertal': 'Stunden',
    'timer': 'Stunden',
    'sømil': 'Seemeilen',
    'knob': 'Knoten',
    'meter': 'Meter',

    # ── Sejlføringen inde i en sætning ──────────────────────────────
    # "halber Wind" hedder "bei halbem Wind", når det står i en sætning.
    # Dansk bøjer ikke, så dér er der intet at slå op.
    'i vindøjet|sætning': 'im Wind',
    'skarp bidevind|sætning': 'hart am Wind',
    'bidevind|sætning': 'am Wind',
    'halvvind|sætning': 'bei halbem Wind',
    'rumskøds|sætning': 'bei raumem Wind',
    'læns|sætning': 'vor dem Wind',

    # ── Bådtyper og skrog ───────────────────────────────────────────
    'Sejlbåd': 'Segelboot',
    'Motorbåd': 'Motorboot',
    'fortrængning': 'Verdränger',
    'halvplanende': 'Halbgleiter',
    'planende': 'Gleiter',

    # ── Timetabellens kolonner ──────────────────────────────────────
    'Tid': 'Zeit',
    'Vind': 'Wind',
    'Bølger': 'Wellen',
    'Fart': 'Fahrt',
    'Sejlføring': 'Segelführung',
}
