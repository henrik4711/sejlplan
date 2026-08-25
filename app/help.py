"""Hjælpen — ét sted, to udgaver.

Teksterne her vises to steder: som et lille spørgsmålstegn ved siden af det, de
handler om, og samlet i en manual, man kan hente og printe. Begge dele læses af
den samme liste, så de aldrig kan komme til at sige noget forskelligt. Retter
man et afsnit, er det rettet begge steder.

Skrevet til den, der står med båden og ikke har lyst til at læse en manual.
Derfor: hvad tallet betyder, hvad det gør ved planen, og hvad man selv skal
tage stilling til. Ikke hvor man klikker.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Topic:
    """Ét emne. `short` er det, der står i boblen først."""
    id: str
    title: str
    short: str
    body: tuple[str, ...] = field(default_factory=tuple)
    group: str = ''


TOPICS: tuple[Topic, ...] = (
    # ── Sådan hænger det sammen ─────────────────────────────────────
    Topic(
        'sadan', 'Sådan bruges Sejlplan', group='Kom i gang',
        short='Tre trin: læg ruten, vælg hvornår du kaster los, læs planen.',
        body=(
            'Først lægger du ruten — mindst to punkter. Søg efter en havn, '
            'klik på kortet, eller slå havnelaget til og vælg en havn. '
            'Sejlplan lægger selv vejen uden om land.',
            'Så trykker du Find bedste afgangstider. Vi regner hver eneste '
            'afgangstime igennem i det vindue, du har valgt, og viser dem, '
            'der giver noget forskelligt. Vi peger på én, men du vælger.',
            'Til sidst står sejlplanen: hvad turen bliver, dag for dag, stræk '
            'for stræk og time for time. Den kan printes, kopieres og læses '
            'uden dækning.',
        )),
    Topic(
        'rute', 'Ruten og havvejen', group='Kom i gang',
        short='Stregen følger vandet, ikke luftlinjen — derfor er den længere.',
        body=(
            'Sejlplan lægger ruten uden om land med en søkortsagtig maske over '
            'de danske og skandinaviske farvande. Derfor står der tit "3,7 sm '
            'udenom land" ved et ben: det er, hvad det koster at komme rundt '
            'om pynten i stedet for at sejle gennem den.',
            'Masken kender land og vand — den kender ikke dybder, sømærker, '
            'ruser eller sejlrender. Kontrollér altid benene på søkortet, især '
            'i smalt farvand og tæt på kysten.',
            'Du kan trække et punkt på kortet, flytte det op og ned i listen, '
            'og vende hele ruten om under dele-ikonet.',
        )),

    # ── Din båd ─────────────────────────────────────────────────────
    Topic(
        'baad', 'Din båd', group='Din båd',
        short='Planen er kun din, hvis den regner på din båds fart.',
        body=(
            'De faste både er eksempler. Ingen ejer et eksempel, og en plan, '
            'der regner på en anden båds fart, er ikke din plan. Læg din egen '
            'ind under Indstillinger.',
            'For en sejlbåd kan du søge den i registret — omkring 130 både, '
            'man møder i danske og nordiske havne. Så udfyldes længde og fart '
            'af fabrikantens mål.',
            'For en motorbåd spørger vi om marchfart, skrogtype og forbrug. '
            'Skroget afgør, hvor meget søen tager af farten: en planende båd '
            'taber mest, fordi den må ned i fortrængning i en stejl modsø.',
        )),
    Topic(
        'halvvind', 'Fart for halvvind i 10 knobs vind', group='Din båd',
        short='Ét tal, der skalerer et polardiagram op eller ned til din båd.',
        body=(
            'Et rigtigt polardiagram er en måling af netop din båd med netop '
            'dine sejl. Det har de færreste liggende. Så vi spørger om ét tal, '
            'enhver sejler kender — farten med vinden ind fra siden i en jævn '
            'brise — og skalerer en almindelig krydsers diagram, så det rammer '
            'dit tal.',
            'Vælger du din båd i registret, regnes tallet af sejlareal, '
            'deplacement og vandlinje. Det er et kvalificeret skøn, ikke en '
            'måling, og du kan altid rette det.',
            'Ligger kursen tættere på vinden, end båden kan sejle, regner '
            'planen med, at du krydser: fremdriften mod målet, ikke farten '
            'gennem vandet.',
        )),
    Topic(
        'graenser', 'Komfortgrænser', group='Din båd',
        short='Over dem markeres timerne — det er dine grænser, ikke bådens.',
        body=(
            'Vind og bølger over grænsen giver skærpede timer, og et stykke '
            'over dem frarådede. Det handler om, hvad du og besætningen kan '
            'holde til, ikke om hvad båden kan bære.',
            'Bølgehøjden vejes efter, hvor søen kommer fra. Modsø tæller '
            'hårdere end tværsø, og medsø mildest — det er dét, man mærker.',
            'Grænserne bruges også til at afgøre, om du bliver blæst inde på '
            'destinationen. Sætter du dem urealistisk højt, forsvinder den '
            'advarsel.',
        )),

    # ── Tid ─────────────────────────────────────────────────────────
    Topic(
        'sejldogn', 'Sejldøgn', group='Tid og vejr',
        short='Sluttidspunktet er, hvornår du vil ligge fortøjet — ikke afgå.',
        body=(
            'Siger du 07–20, betyder det ikke "afgå senest kl. 20". Det '
            'betyder: ligge fortøjet kl. 20. Rækker turen ikke inden for '
            'døgnet, deler Sejlplan den og finder en havn undervejs at '
            'overnatte i.',
            'Derfor kan planen finde på at lægge til i en havn midt på dagen. '
            'Det er med vilje: er næste stræk for langt til at nås inden '
            'lukketid, og er der ingen havn imellem, ender man i mørke.',
            'Vil du hele vejen i ét stræk, så slå mørkesejlads til under '
            'Indstillinger. Så lægges der ingen overnatninger ind, og '
            'mørketimerne tælles for sig.',
        )),
    Topic(
        'afgange', 'Afgangstiderne', group='Tid og vejr',
        short='Alle de afgange, der giver noget forskelligt. Du vælger.',
        body=(
            'Vi regner hver afgangstime igennem i dit vindue og viser dem, '
            'der ender forskelligt — forskellig ankomst, forskellige havne '
            'undervejs eller forskellige forhold. To afgange en time fra '
            'hinanden, der giver præcis det samme, står kun én gang.',
            'Hver dag, du overhovedet kan sejle, er med. Ellers kunne en hel '
            'dag forsvinde, fordi en anden havde bedre vejr, og så vidste du '
            'ikke, at muligheden fandtes.',
            'Rækkefølgen er vores anbefaling — vi vægter frarådede timer '
            'tungest, så korte passager, og til sidst hvornår du er hjemme. '
            'Det er en anbefaling, ikke en afgørelse.',
        )),
    Topic(
        'strom', 'Strøm', group='Tid og vejr',
        short='Farten er over grunden. Strømmen er regnet med.',
        body=(
            'Farten i planen er over grunden — dét, der flytter båden — ikke '
            'gennem vandet. Strømmen langs kursen lægges til eller trækkes '
            'fra, og står i søjlen Strøm: grøn med, rød imod.',
            'Står strømmen tværs, tæller den ikke på farten. Til gengæld '
            'sætter den af til siden, og det skal styres op — planen regner '
            'ikke afdriften ud for dig.',
            'Tallene kommer fra en global havmodel, og den opløser ikke de '
            'danske bælter helt. I Storebælt og Grønsund kan der løbe to-tre '
            'knob, hvor modellen viser under én. Brug den som en retning, og '
            'slå strømtabellen op, når det gælder en smal passage.',
        )),
    Topic(
        'prognose', 'Hvor langt frem vi kan se', group='Tid og vejr',
        short='Ti døgn. Bølgerne er loftet, ikke vinden.',
        body=(
            'Vinden rækker fjorten døgn frem, bølgerne ti. En sejlplan uden '
            'søen er en halv plan, så ti døgn er grænsen.',
            'De første tre-fire døgn holder ret godt. Derefter er det '
            'retningen, der overlever, ikke timerne — og det står i planen, '
            'når turen slutter fem døgn eller mere ude.',
            'Rækker prognosen ikke hele vejen, siger planen, hvor langt du '
            'når, i stedet for at påstå en ankomst. Læg turen tidligere, '
            'eller planlæg den sidste del om nogle dage.',
        )),
    Topic(
        'blaest-inde', 'Blæst inde', group='Tid og vejr',
        short='Om du kommer væk igen — ikke kun om du kommer derhen.',
        body=(
            'Man kigger på vejret frem til man er fremme, og ikke længere. Så '
            'sejler man til Marstal i det pæneste vejr og opdager i havnen, at '
            'det blæser femogtyve knob i tre døgn.',
            'Sejlplan kigger videre for dig. Fra ankomsten og til prognosen '
            'slipper op tælles det efter, om der er et sejlbart døgn tilbage. '
            'Er der to eller flere døgn i træk uden, står det i planen — med '
            'hvornår vinduet åbner igen.',
            'Holder det ikke op, før prognosen gør, får du det at vide som '
            'dét: vi ved ikke hvornår. Så er hjemturen en tur for sig.',
        )),

    # ── Planen ──────────────────────────────────────────────────────
    Topic(
        'straek', 'Stræk for stræk', group='Sejlplanen',
        short='Delt op dér, hvor kursen skifter — ikke hvor du satte et kryds.',
        body=(
            'Sætter du Køge og Præstø ind, er det ét ben. Men det sejles mod '
            'øst, så mod syd og til sidst mod vest, og en plan, der giver én '
            'kurs for det hele, passer ingen af stederne.',
            'Derfor deles turen dér, hvor du faktisk skal dreje. Hvert stræk '
            'har sin kurs, sin vind, sin sø og sin sejlføring — og de gælder '
            'præcis dér, hvor du styrer den kurs.',
            'Bliver et stræk brudt af en overnatning, står det i teksten. '
            'Timerne ved kaj tæller ikke med.',
        )),
    Topic(
        'nogletal', 'Nøgletallene', group='Sejlplanen',
        short='Under vejs er den rigtige tid fra kaj til kaj.',
        body=(
            '"Under vejs" er tiden fra du kaster los, til du ligger fortøjet, '
            'lagt sammen for alle døgnene. Havnetimerne tæller ikke med.',
            'Gennemsnitsfarten er distancen delt med den tid. Distance, tid og '
            'fart passer sammen — du kan regne efter.',
            'Frarådede timer er dem, der ligger et stykke over dine grænser. '
            'Er der nogen, skal du tage stilling til dem, før du kaster los.',
        )),
    Topic(
        'time-for-time', 'Time for time', group='Sejlplanen',
        short='Grøn er god, gul er skærpet, rød frarådes — efter dine grænser.',
        body=(
            'Hver række er én sejltime på det sted, du er nået til: vinden, '
            'hvor den kommer fra, bølgerne, farten og sejlføringen.',
            'Farven kommer af dine egne komfortgrænser. Grøn er inden for '
            'dem, gul er lidt over, rød er et stykke over.',
            'Står der "motor", er der for lidt vind til at sejle — under tre '
            'knobs fart tændes motoren i beregningen, hvis du har slået det '
            'til.',
        )),
    Topic(
        'havne', 'Havne undervejs', group='Sejlplanen',
        short='Steder du kan søge ind, hvis vejret skifter.',
        body=(
            'Listen er de havne, der ligger tæt nok på ruten til at være et '
            'rimeligt sted at gå ind — op til seks sømil fra vejen. Klik på '
            'en for at lægge den ind som mellemstop.',
            'Vi tjekker, at man kan sejle lige ind til dem fra ruten, så et '
            'forslag aldrig kræver, at du sejler uden om en ø.',
            'Har havnen en side i havnelods.dk, er der et lille ikon ved '
            'siden af. Dér står pladser, priser, faciliteter og indsejling. '
            'Mangler ikonet, kender vi ikke havnens side — så er det bedre at '
            'lade være end at sende dig det forkerte sted hen.',
        )),

    # ── Gemme og tage med ───────────────────────────────────────────
    Topic(
        'plads', 'Er der plads i havnen?', group='Sejlplanen',
        short='Det eneste, ingen model kan svare på. Kun dem, der ligger der.',
        body=(
            'Vejret kommer fra en model og afstanden fra et søkort. Om der er '
            'en plads tilbage ved ydermolen klokken fire, ved kun den, der '
            'ligger der klokken to.',
            'Derfor kan man melde: god plads, få pladser, eller fuld. Det tager '
            'to sekunder, det er anonymt, og der gemmes kun havnen, svaret og '
            'hvornår. Der er ikke noget at skrive — og dermed heller ikke et '
            'sted, hvor nogen kan skrive noget til nogen.',
            'Alderen står altid med, for den er halvdelen af oplysningen. '
            '"Fuld" for tre timer siden er noget andet end "fuld" i går aftes. '
            'Efter halvandet døgn forsvinder meldingen af sig selv.',
            'Ligger du i en havn, så meld. Det koster dig ingenting og er det '
            'eneste, den næste ikke kan finde ud af på egen hånd.',
        )),
    # ── Undervejs og de andre ───────────────────────────────────────
    Topic(
        'undervejs', 'Undervejs: foran eller bagud?', group='Undervejs',
        short='Telefonens position mod planens — hvornår er du så fremme?',
        body=(
            'Planen bliver lagt i havnen. Undervejs er spørgsmålet et andet: '
            'er jeg foran eller bagud, og hvornår er jeg så fremme i '
            'virkeligheden. Tryk "Jeg er undervejs" i sejlplanen.',
            'Vi finder det punkt på ruten, du er tættest på, og slår op i '
            'planens eget spor, hvor langt du skulle have været på det '
            'klokkeslæt. Ligger du mere end tre sømil fra ruten, siger vi '
            'ingenting — så betyder et forspring heller ingenting.',
            'Positionen bliver på din telefon og i den ene beregning. Den '
            'gemmes ikke, og ingen andre kan se den. At vise sig for andre er '
            'en anden funktion, man selv skal tænde.',
            'På iPhone virker positionen kun, mens skærmen er tændt og '
            'Sejlplan er fremme. Låser du telefonen, holder den op. Det er '
            'iOS, der bestemmer det.',
        )),
    Topic(
        'andre-baade', 'Se andre både', group='Undervejs',
        short='Usynlig til du selv tænder — og du ser kun dem, der også har.',
        body=(
            'Tryk "Vis min båd for andre" og vælg et bådnavn. Så kan andre, '
            'der også er synlige, se hvor du er, og du kan se dem. Kun jer, '
            'der har slået det til.',
            'Du ser kun andre, mens du selv er synlig. Ingen kan ligge og '
            'kigge uden at være der selv. Slukker du, forsvinder du fra deres '
            'kort og de fra dit i samme øjeblik — og din position bliver '
            'slettet, ikke skjult.',
            'Positionen udløber af sig selv efter en halv time uden '
            'opdatering. Der gemmes ingen historik: hver ny position skriver '
            'den forrige over, så ingen kan slå op, hvor du var i går.',
            'Skriv bådens navn, ikke dit eget — det er dét, de andre ser. Ser '
            'du ingen både, er der ingen inden for tres sømil, der har tændt.',
        )),
    Topic(
        'hvem-er-her', 'Hvem er der lige nu', group='Undervejs',
        short='Listen over både, delt op efter havn. Nemmere end kortet.',
        body=(
            'Kortet er godt til at vise, hvor nogen er. Det er dårligt til at '
            'svare på, hvem der overhovedet er der: en båd er en lille '
            'trekant, og zoomer man ud så hele farvandet er med, kan man ikke '
            'se dem.',
            'Tryk "Se hvem der er i nærheden". De både, der ligger i en havn, '
            'står under havnens navn — for det er dét, man vil vide, når man '
            'leder efter nogen at drikke kaffe med. Resten står under '
            'Undervejs med afstand og pejling.',
            'Havnene på ruten får også et mærke, når der ligger nogen: "3 '
            'både her". Tryk på det, og du er i listen.',
            'Tryk på en båd for at skrive til den. Du ser kun både, der også '
            'har gjort sig synlige — den regel gælder her som alle andre '
            'steder.',
        )),
    Topic(
        'beskeder', 'Beskeder mellem både', group='Undervejs',
        short='Tryk på en båd på kortet og skriv. Kun mellem synlige både.',
        body=(
            'Det er ikke en indbakke med fremmede og ikke en opslagstavle — '
            'det er en samtale mellem to, der ligger i det samme farvand lige '
            'nu, og som begge har valgt at være synlige.',
            'Har nogen skrevet, står der en prik på båden på kortet og et tal '
            'i panelet. Beskeder forsvinder efter et døgn.',
            'Bloker sidder i samtalens menu og virker begge veje med det '
            'samme: I kan hverken skrive til hinanden eller se hinanden på '
            'kortet. Anmeld sidder på selve beskeden — anmelder du en, gemmer '
            'vi teksten, for ellers ville den dø efter et døgn, og så stod ord '
            'mod ord.',
            'Skriver du tre gange til en, der ikke svarer, må du vente. Det er '
            'med vilje.',
        )),

    Topic(
        'vejrvagt', 'Vejrvagt', group='Gem og tag med',
        short='Sig til, når vejret er der — også om fjorten dage.',
        body=(
            'Skal turen først gå om tre uger, er der ingen prognose at kigge '
            'i endnu, og så skal man ikke sidde og trykke opdater hver dag. '
            'Læg en vagt på ruten, og få én mail, når der er et vindue.',
            'Vagten venter, til prognosen når frem til dine datoer, og regner '
            'så turen igennem med din egen båd og dine egne grænser. Vi '
            'skriver kun, hvis du også kan komme hjem igen — er du blæst inde '
            'i tre døgn på destinationen, er det ikke en gevinst.',
            'Én vagt giver én besked. Ikke en strøm af mails, hver gang '
            'modellen flytter sig en halv knob. Kommer beskeden, er vagten '
            'brugt, og du lægger en ny.',
            'Vi skriver aldrig til en adresse, der ikke selv har bekræftet '
            'den, og hver mail bærer sit eget link til at stoppe.',
        )),
    Topic(
        'sprog', 'Sprog', group='Gem og tag med',
        short='Dansk og tysk. Flaget i toppen skifter.',
        body=(
            'Flaget øverst på siden skifter sprog — tryk på det og vælg. Det '
            'står også under Indstillinger. Siden hentes forfra på det nye '
            'sprog.',
            'Første besøg følger browserens eget førstevalg af sprog — er '
            'det ikke dansk eller tysk, får du dansk. Derefter vinder dit '
            'valg, og det gemmes hos dig selv, så det holder, også når vi '
            'lægger en ny udgave af Sejlplan ud.',
            'Er en tekst ikke oversat endnu, står den på dansk. Det er med '
            'vilje: en halvt oversat flade er brugbar, en flade med huller i '
            'er ikke.',
        )),
    Topic(
        'mine-ruter', 'Mine ruter', group='Gem og tag med',
        short='Gem turen, og hent den frem igen, når prognosen når så langt.',
        body=(
            'En sommertur på fjorten dage kan ikke planlægges på én gang — '
            'prognosen rækker ti døgn. Men ruten kan lægges nu: afstande, '
            'ben, havne undervejs og hvor mange sejldøgn den kræver, regnes '
            'uden et gram vejr.',
            'Gem den, og hent den frem igen, efterhånden som prognosen ruller '
            'frem over din rute. Ét tryk på Gem opdaterer den, du arbejder i; '
            'vil du have en kopi, er der Gem som ny.',
            'Ruterne ligger i din browser og i din session. De overlever, at '
            'vi lægger en ny version af Sejlplan ud.',
        )),
    Topic(
        'app', 'Appen og uden dækning', group='Gem og tag med',
        short='Den seneste sejlplan kan læses uden forbindelse.',
        body=(
            'Læg Sejlplan på hjemmeskærmen under Indstillinger, så åbner den '
            'i sit eget vindue uden browserlinje. På iPhone gør du det selv: '
            'åbn siden i Safari, tryk Del, vælg "Føj til hjemmeskærm".',
            'Du kan ikke lægge en rute uden dækning — beregningen sker på '
            'serveren. Men hver gang du åbner en sejlplan, lægges den ned i '
            'telefonen som et dokument, der kan stå alene. Går dækningen, '
            'kommer den frem: overblik, advarsler, dag for dag, stræk for '
            'stræk og hele timetabellen.',
            'De kortfliser, du har set på, gemmes også, så kortet kan vise '
            'det farvand, du lige har kigget på.',
        )),
    Topic(
        'gpx', 'GPX til kortplotteren', group='Gem og tag med',
        short='Hele havvejen med, ikke bare dine punkter.',
        body=(
            'Under dele-ikonet ligger Hent GPX til kortplotter. Filen '
            'indeholder dine egne punkter som waypoints, hele havvejen som '
            'rute med knækpunkterne uden om land, og den samme vej som spor.',
            'Både rute og spor er med, fordi der findes plottere, der kun '
            'læser det ene.',
            'Samme sted kan du kopiere et delelink. Det åbner ruten hos den, '
            'du sender det til — også hvis de aldrig har brugt Sejlplan før.',
        )),
    Topic(
        'skipper', 'Skippervurdering', group='Gem og tag med',
        short='En erfaren sejlkonsulent læser planen igennem.',
        body=(
            'Vurderingen gennemgår ruten ben for ben og kommenterer det, '
            'tallene ikke siger: hvornår du bør reve, hvad der er værd at '
            'holde øje med, og om afgangen er den rigtige.',
            'Den skrives af en sprogmodel ud fra din plan. Den er god til at '
            'få øje på det, der ikke hænger sammen — men den erstatter ikke '
            'din egen vurdering.',
        )),
)

DISCLAIMER = (
    'Sejlplan er et planlægningsværktøj. Prognoser er prognoser, og en '
    'landmaske er ikke et søkort. Planen erstatter ikke søkort, '
    'farvandsudsigt, efterretninger for søfarende eller almindelig '
    'sømandskab. Ansvaret for sejladsen er skipperens.'
)


def by_id(topic_id: str) -> Topic | None:
    return next((t for t in TOPICS if t.id == topic_id), None)


# Sømandskabet står i sit eget modul sammen med tegningerne, så teksten og
# billedet af det samme mærke ikke kan komme til at sige noget forskelligt.
# Her hentes teksten ind, så den også står i manualen og kan hentes ned.
def _fra_soemandskab() -> tuple[Topic, ...]:
    from . import seamanship
    return tuple(Topic(id, titel, kort, krop, group='Til søs')
                 for id, titel, kort, krop in seamanship.HELP)


TOPICS = TOPICS + _fra_soemandskab()


def groups() -> list[tuple[str, list[Topic]]]:
    """Emnerne samlet i den rækkefølge, de står — til manualen."""
    out: list[tuple[str, list[Topic]]] = []
    for t in TOPICS:
        if not out or out[-1][0] != t.group:
            out.append((t.group, []))
        out[-1][1].append(t)
    return out
