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
}
