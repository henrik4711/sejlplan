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

import math

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

# ── Tegningen ────────────────────────────────────────────────────────────────
# Set lige oppefra, med stævnen opad. "Bommen ud til tyve-tredive grader" er
# en sætning, man kan læse forkert; en tegning kan man ikke.
#
# Bomvinklerne er ikke en formel — de er slået op punkt for punkt og
# interpoleret imellem. En formel ville ramme pænt ét sted og forkert to
# andre, og det er netop de yderpunkter, folk er i tvivl om.
_BOM = ((30, 0), (45, 8), (60, 16), (90, 28), (120, 46), (150, 66), (180, 84))

BÅD_BREDDE = 200
BÅD_HØJDE = 190
_MIDTE_X = 100.0
_MAST_Y = 68.0
_STÆVN_Y = 24.0
_BOM_LÆNGDE = 70.0


def boom_angle(twa: float) -> float:
    """Bommens vinkel fra midterlinjen ved en given vindvinkel."""
    twa = min(180.0, max(0.0, abs(float(twa))))
    if twa <= _BOM[0][0]:
        return 0.0
    for (a1, v1), (a2, v2) in zip(_BOM, _BOM[1:]):
        if twa <= a2:
            k = (twa - a1) / (a2 - a1)
            return v1 + k * (v2 - v1)
    return _BOM[-1][1]


def _punkt(x: float, y: float) -> str:
    return f'{x:.1f},{y:.1f}'


def _bue(fra: tuple, til: tuple, bug: float) -> str:
    """En kurve fra et punkt til et andet, buet `bug` ud til siden.

    Det er dét, der gør, at et sejl ligner et sejl og ikke en pind: det står
    med bugen i læ, og bugen er den halve grund til, at båden går fremad.
    """
    (x1, y1), (x2, y2) = fra, til
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    dx, dy = x2 - x1, y2 - y1
    længde = math.hypot(dx, dy) or 1.0
    # Vinkelret ud fra linjen.
    px, py = -dy / længde, dx / længde
    return (f'M{_punkt(x1, y1)} Q{_punkt(mx + px * bug, my + py * bug)} '
            f'{_punkt(x2, y2)}')


def diagram(twa: float, tack: str = 'styrbords halse') -> str:
    """Sejlføringen tegnet oppefra. Stævnen opad, vinden markeret.

    `tack` siger, hvilken side vinden kommer ind fra. Kommer den ind fra
    styrbord, står sejlene ud til bagbord — og tegningen skal vende samme vej
    som virkeligheden, ellers gør den mere skade end gavn.
    """
    twa = min(180.0, max(0.0, abs(float(twa))))
    # +1 betyder, at vinden kommer fra styrbord, og sejlene står i bagbord.
    fra_styrbord = 'bagbord' not in (tack or '')
    side = 1.0 if fra_styrbord else -1.0
    krydser = twa < I_VINDØJET

    vinkel = math.radians(boom_angle(twa))
    # Bommen peger agterud og ud i læ — altså modsat den side, vinden
    # kommer fra.
    bom_x = _MIDTE_X - side * _BOM_LÆNGDE * math.sin(vinkel)
    bom_y = _MAST_Y + _BOM_LÆNGDE * math.cos(vinkel)

    # Forsejlet skødes tættere end storsejlet på kryds og næsten lige så
    # åbent på læns. Det er derfor forholdet ikke er fast.
    for_vinkel = math.radians(boom_angle(twa) * (0.55 if twa < HALVVIND
                                                 else 0.9))
    for_x = _MIDTE_X - side * 46 * math.sin(for_vinkel)
    for_y = _MAST_Y - 6 + 46 * math.cos(for_vinkel)

    dele = [_skrog(), _vind(twa, side)]

    if krydser:
        dele.append(_i_vindøjet())
    else:
        bug = 9.0 if twa < BIDEVIND else 13.0
        dele.append(
            f'<path d="{_bue((_MIDTE_X, _MAST_Y), (bom_x, bom_y), -side * bug)}"'
            f' fill="none" stroke="{_SEJL}" stroke-width="7" '
            f'stroke-linecap="round" stroke-opacity=".9"/>')
        dele.append(
            f'<line x1="{_MIDTE_X}" y1="{_MAST_Y}" x2="{bom_x:.1f}" '
            f'y2="{bom_y:.1f}" stroke="{_BOM_F}" stroke-width="2.5" '
            f'stroke-linecap="round"/>')
        dele.append(
            f'<path d="{_bue((_MIDTE_X, _STÆVN_Y + 4), (for_x, for_y), -side * 8)}"'
            f' fill="none" stroke="{_FORSEJL}" stroke-width="6" '
            f'stroke-linecap="round" stroke-opacity=".85"/>')

    dele.append(f'<circle cx="{_MIDTE_X}" cy="{_MAST_Y}" r="3.5" '
                f'fill="{_BOM_F}"/>')

    return (f'<svg viewBox="0 0 {BÅD_BREDDE} {BÅD_HØJDE}" '
            f'width="100%" height="auto" role="img" aria-hidden="true" '
            f'class="trim-svg">{"".join(dele)}</svg>')


_SKROG = '#8A94A6'
_SEJL = '#C8933B'
_FORSEJL = '#0F9B8E'
_BOM_F = '#3A4252'
_VIND_F = '#6B7280'


def _skrog() -> str:
    return (f'<path d="M{_MIDTE_X},{_STÆVN_Y} '
            f'C78,52 70,100 76,146 Q{_MIDTE_X},160 124,146 '
            f'C130,100 122,52 {_MIDTE_X},{_STÆVN_Y} Z" '
            f'fill="{_SKROG}" fill-opacity=".16" stroke="{_SKROG}" '
            f'stroke-width="2"/>')


def _i_vindøjet() -> str:
    """Sejlene står og slår. Der er ingen sejlføring at tegne — der er en
    beslutning at træffe."""
    return (f'<path d="M{_MIDTE_X},{_MAST_Y} l-8,26 l8,-8 l8,8 z" '
            f'fill="{_SEJL}" fill-opacity=".45"/>'
            f'<path d="M{_MIDTE_X},{_MAST_Y} l-5,52 l5,-10 l5,10 z" '
            f'fill="{_SEJL}" fill-opacity=".3"/>')


def _vind(twa: float, side: float) -> str:
    """Pilen, der viser hvor vinden kommer fra."""
    v = math.radians(twa)
    # Enhedsvektor hen imod dét, vinden kommer fra: opad er negativ y.
    ux, uy = side * math.sin(v), -math.cos(v)
    cx, cy = _MIDTE_X, 92.0
    x1, y1 = cx + ux * 86, cy + uy * 86
    x2, y2 = cx + ux * 52, cy + uy * 52
    return (f'<defs><marker id="vindspids" markerWidth="7" markerHeight="7" '
            f'refX="5.5" refY="3" orient="auto">'
            f'<path d="M0,0 L6,3 L0,6 z" fill="{_VIND_F}"/></marker></defs>'
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{_VIND_F}" stroke-width="2.5" stroke-dasharray="5 4" '
            f'marker-end="url(#vindspids)"/>')
