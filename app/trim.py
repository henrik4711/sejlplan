"""Hvordan sejlene skal stå på det stræk, du er på vej ud på.

Planen ved to ting, der er nok til at give et rigtigt råd: hvilken vinkel
vinden kommer ind i, og hvor hårdt det blæser. Ud af dem falder det meste af
trimmet — hvor bommen står, hvor løjgangsvognen skal ligge, om nedhalene skal
strammes eller løsnes, og hvornår der skal rebes.

Det er et udgangspunkt, ikke en facitliste. Sejlene er dine, deres alder er
din, og en tiårig dacronsæk vil noget andet end et nyt laminatsejl. Rådene er
skrevet til en almindelig krydser med storsejl og rullegenua, fordi det er dét,
de fleste står med.

En ting, der ikke er til forhandling, står for sig: på læns skal der bomholder
på. Det er dér, folk får bommen over hovedet.
"""
from __future__ import annotations

from dataclasses import dataclass

from .boats import Boat

# Grænserne mellem sejlstillingerne. De samme tal som i `sailing.point_of_sail`,
# så teksten og farven i timetabellen aldrig kan komme til at være uenige.
I_VINDØJET = 35
SKARP_BIDEVIND = 55
BIDEVIND = 80
HALVVIND = 100
RUMSKØDS = 150

# Vindstyrker, hvor rådet skifter. Sande knob, ikke tilsyneladende.
LET = 8
JÆVN = 14
FRISK = 20
HÅRD = 26


@dataclass(frozen=True)
class Trim:
    """Ét råd, delt op efter det man rører ved."""
    sail: str                # sejlstillingen, som den hedder i planen
    boom: str                # hvor bommen står
    traveller: str           # løjgangsvognen
    mainsheet: str           # storskødet
    vang: str                # bomnedhalet
    outhaul: str             # udhalet
    cunningham: str          # nedhalet i forliget
    backstay: str            # agterstaget
    headsail: str            # forsejlet og skødevognen
    watch: str               # hvad man kigger på for at se, om det passer
    reef: str                # rebning ved den her vindstyrke
    warning: str = ''        # det, der kan gøre ondt

    @property
    def rows(self) -> tuple[tuple[str, str], ...]:
        """Rådene som (hvad, hvordan) — til en tabel."""
        return tuple((navn, tekst) for navn, tekst in (
            ('Bommen', self.boom),
            ('Løjgangsvognen', self.traveller),
            ('Storskødet', self.mainsheet),
            ('Bomnedhalet', self.vang),
            ('Udhalet', self.outhaul),
            ('Nedhalet', self.cunningham),
            ('Agterstaget', self.backstay),
            ('Forsejlet', self.headsail),
        ) if tekst)


def _styrke(kn: float) -> str:
    if kn < LET:
        return 'let'
    if kn < JÆVN:
        return 'jævn'
    if kn < FRISK:
        return 'frisk'
    if kn < HÅRD:
        return 'hård'
    return 'meget hård'


def _reb(kn: float, twa: float) -> str:
    """Hvornår der skal rebes.

    Tallene er for en almindelig krydser. På kryds mærkes vinden hårdere end
    på læns, fordi bådens egen fart lægges til — derfor rebes der tidligere
    op mod vinden end ned med den.
    """
    op = twa < HALVVIND
    if kn < JÆVN:
        return 'Fuldt sejl.'
    if kn < FRISK:
        return ('Overvej første reb, hvis båden lægger sig mere end tyve '
                'grader, eller hvis der er tryk i roret.' if op else
                'Fuldt sejl. Hold øje med bygerne.')
    if kn < HÅRD:
        return ('Første reb. Det koster ikke fart — en overtrimmet båd '
                'krænger og skrider sidelæns.' if op else
                'Første reb, hvis det er trættende at styre.')
    return ('Andet reb og rullet genua. Kommer det over tredive knob, er det '
            'tredje reb eller en stormfok — og så er spørgsmålet, om turen '
            'skal sejles i dag.')


def _watch(twa: float) -> str:
    if twa < BIDEVIND:
        return ('Telltalerne på forsejlet skal strømme bagud på begge sider. '
                'Lifter de i luv, så fald af eller stram skødet. Øverste '
                'sejlpind i storsejlet omtrent parallel med bommen.')
    if twa < HALVVIND:
        return ('Skød ud, til forkanten lige begynder at bagge, og stram så '
                'lidt til igen. Det er dér, sejlet trækker mest.')
    if twa < RUMSKØDS:
        return ('Telltalen agter på storsejlet skal strømme. Krøller den ind '
                'bag sejlet, er der for meget twist — stram bomnedhalet.')
    return ('Hold øje med vindviseren og med bølgerne agterfra. Ruller båden, '
            'så luf en smule op — læns er ikke det hurtigste, og sjældent '
            'det roligste.')


def advise(twa: float, wind_kn: float, boat: Boat | None = None) -> Trim | None:
    """Trimråd for én vindvinkel og én vindstyrke.

    `twa` er vinklen mellem kursen og vinden: 0 er lige i stævnen, 180 lige
    agterind. Motorbåde får ingenting — der er ikke noget at trimme.
    """
    if boat is not None and boat.is_motor:
        return None

    twa = abs(float(twa))
    kn = max(0.0, float(wind_kn))
    styrke = _styrke(kn)
    let = styrke == 'let'
    hårdt = styrke in ('frisk', 'hård', 'meget hård')

    if twa < I_VINDØJET:
        return Trim(
            sail='i vindøjet',
            boom='Kursen ligger tættere på vinden, end båden kan sejle. '
                 'Strækket skal krydses — læg dig på den halse, der bringer '
                 'dig nærmest målet, og trim som til bidevind.',
            traveller='', mainsheet='', vang='', outhaul='', cunningham='',
            backstay='', headsail='',
            watch='Vend, når vindpejlingen til målet er lige så stor til den '
                  'anden side. Så sejler du ikke længere end nødvendigt.',
            reef=_reb(kn, twa))

    if twa < BIDEVIND:
        skarp = twa < SKARP_BIDEVIND
        return Trim(
            sail='skarp bidevind' if skarp else 'bidevind',
            boom='Omtrent på midterlinjen. Kig op ad bommen — den skal pege '
                 'lige agterud eller en anelse i læ.',
            traveller=('Lidt til luv for midten. Så kan skødet holde bommen '
                       'inde uden at trække sejlet fladt.' if let else
                       'Midtskibs.' if styrke == 'jævn' else
                       'Til læ, indtil båden retter sig op. Det åbner toppen '
                       'og lader trykket gå ud foroven i stedet for at '
                       'lægge båden ned.'),
            mainsheet=('Løst nok til at agterliget hænger blødt. Et fladt '
                       'sejl trækker ikke i let vind.' if let else
                       'Stramt. Øverste sejlpind parallel med bommen — i '
                       'byger må den gerne falde en smule af.'),
            vang='Løst. På kryds er det skødet, der holder bommen nede — '
                 'nedhalet skal først bruges, når du skøder ud.',
            outhaul=('Løst, så der er dybde i underliget.' if let else
                     'Stramt. Fladt sejl, mindre krængning.'),
            cunningham=('Helt løst. Rynker i forliget er i orden, når det '
                        'blæser lidt.' if let else
                        'Stram, til rynkerne langs masten lige forsvinder. '
                        'Det flytter trykpunktet frem og flader sejlet.'),
            backstay=('Løst.' if not hårdt else
                      'Stram. Masten bøjer, storsejlet flader ud, og '
                      'forstaget bliver stivere — det er dét, der gør, at '
                      'du kan holde højde.'),
            headsail=('Skødevognen frem, så sejlet får dybde forneden. Skød '
                      'blødt — genuaen skal ikke røre saling eller vant.'
                      if let else
                      'Skødevognen agter. Toppen åbner, og båden retter sig '
                      'op uden at du mister fart.' if hårdt else
                      'Skødevognen midt i sporet. Telltalerne skal lifte '
                      'samtidig oppe og nede.'),
            watch=_watch(twa), reef=_reb(kn, twa))

    if twa < HALVVIND:
        return Trim(
            sail='halvvind',
            boom='Ud til omkring tyve-tredive grader fra midterlinjen.',
            traveller='Til læ. Nu er det bomnedhalet, der styrer twisten — '
                      'ikke vognen.',
            mainsheet='Skød ud, til forkanten lige begynder at bagge, og '
                      'stram så lidt til.',
            vang='Stram nu. Uden det løfter bommen sig, toppen af sejlet '
                 'falder af, og du mister det tryk, du troede du havde.',
            outhaul='Løsn en smule. Halvvind vil have dybde.',
            cunningham='Løsn, med mindre det blæser.',
            backstay='Løsn. Du skal ikke bruge højde her.',
            headsail='Skødevognen lidt frem og ud. Slæk skødet, til '
                     'telltalerne strømmer på begge sider.',
            watch=_watch(twa), reef=_reb(kn, twa))

    if twa < RUMSKØDS:
        return Trim(
            sail='rumskøds',
            boom='Godt ud. Pas på, at den ikke ligger an mod vantet — det '
                 'slider sejlet i stykker på en lang dag.',
            traveller='Helt i læ.',
            mainsheet='Ud, til sejlet lige bagger i forkanten.',
            vang='Hårdt. Det er nu, det tjener sig ind.',
            outhaul='Løst. Dybt sejl.',
            cunningham='Løst.',
            backstay='Løst.',
            headsail='Skødevognen helt frem og ud. Bliver genuaen dækket af '
                     'storsejlet, så tag den over på den anden side med en '
                     'bom — eller sæt spiler eller gennaker, hvis I har '
                     'hænder til det.',
            watch=_watch(twa), reef=_reb(kn, twa),
            warning='Fra her og ned mod læns er der risiko for en '
                    'utilsigtet bomvending. Sæt bomholder.')

    return Trim(
        sail='læns',
        boom='Helt ud.',
        traveller='Helt i læ.',
        mainsheet='Ude. Det er nedhalet og bomholderen, der holder bommen.',
        vang='Hårdt.',
        outhaul='Løst.',
        cunningham='Løst.',
        backstay='Løst.',
        headsail='Bom genuaen ud på modsat side af storsejlet, eller sæt '
                 'spiler. Uden det står den og klapper i storsejlets læ og '
                 'gør ingen nytte.',
        watch=_watch(twa), reef=_reb(kn, twa),
        warning='Sæt bomholder, før du falder af. En utilsigtet bomvending '
                'på læns er dét, der slår folk ned og river rigge ned — og '
                'den kommer, når nogen kigger et andet sted hen.')
