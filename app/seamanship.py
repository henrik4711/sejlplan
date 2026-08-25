"""Sømærker og signaler — det, man skal kunne genkende undervejs.

Det her er et opslagsværk, ikke en advarselstjeneste. Forskellen er vigtig nok
til at stå først:

**Vi siger ikke, hvor farerne er.** Sejlplan kender land og vand, ikke dybder,
grunde, rev, spærrede områder eller skydeområder. Et program, der på grundlag
af det ville skrive "pas på grunden her", ville gætte — og et gæt, der ser ud
som en advarsel, er farligere end ingen advarsel. Farerne står i søkortet og i
Efterretninger for Søfarende. Dem skal du selv slå op.

**Vi siger, hvad du ser.** Et mærke i vandet betyder noget bestemt, og det
betyder det samme hver gang. Det kan man skrive ned én gang og have med. Det er
dét, der er her: afmærkningen, fyrkaraktererne, lanternerne, dagsignalerne,
lydsignalerne og nødsignalerne.

Afmærkningen er **IALA A**, som gælder i Danmark, Tyskland, Sverige, Norge og
resten af Europa. I Nord- og Sydamerika er sidemærkerne byttet om (IALA B) —
det står, hvor det hører hjemme.

Teksterne er en huskeseddel, ikke Søvejsreglerne. Er du i tvivl om en
vigepligt, er det reglerne, der gælder, ikke det her.
"""
from __future__ import annotations

from dataclasses import dataclass

# ── Farverne i tegningerne ───────────────────────────────────────────────────
# Sat som faste værdier og ikke som CSS-variabler: en rød bøje er rød, også i
# mørkt tema. Det er dét, der gør, at man kan genkende den på vandet.
RØD = '#C4362F'
GRØN = '#1E8E4E'
GUL = '#E8C33C'
SORT = '#1B1B1B'
HVID = '#F2F2F0'
BLÅ = '#2F6FC4'
LINJE = '#6B7280'


@dataclass(frozen=True)
class Mark:
    """Ét sømærke: hvad det ser ud som, og hvad det betyder."""
    id: str
    name: str
    meaning: str
    # Hvad man gør ved det. Én sætning, den man har brug for i cockpittet.
    action: str
    light: str
    svg: str
    # Huskeregel, hvis der findes en, der er værd at kunne.
    memo: str = ''


def _bøje(krop: str, top: str = '', bredde: int = 64) -> str:
    """Sæt en bøje sammen: en topbetegnelse over en krop.

    Tegningerne er små med vilje. De skal kunne kendes fra hinanden på en
    telefon i sollys, ikke være pæne på et skrivebord.
    """
    return (f'<svg viewBox="0 0 {bredde} 100" width="{bredde}" height="100" '
            f'role="img" aria-hidden="true">{top}{krop}</svg>')


def _krop(farve: str, bånd: str = '') -> str:
    """Selve bøjen: en tønde med en stage op."""
    return (f'<rect x="30" y="26" width="4" height="30" fill="{LINJE}"/>'
            f'<path d="M20 56 h24 l-3 26 h-18 z" fill="{farve}" '
            f'stroke="{SORT}" stroke-width="1.5" stroke-opacity=".35"/>'
            f'{bånd}'
            f'<path d="M17 82 h30 l-4 8 h-22 z" fill="{LINJE}" '
            f'fill-opacity=".35"/>')


def _stribet(a: str, b: str, lodret: bool = True) -> str:
    """En krop med striber — sikkert vand og ny fare."""
    if lodret:
        striber = ''.join(
            f'<rect x="{20 + i * 6}" y="56" width="6" height="26" '
            f'fill="{a if i % 2 == 0 else b}"/>' for i in range(4))
    else:
        striber = ''.join(
            f'<rect x="20" y="{56 + i * 9}" width="24" height="9" '
            f'fill="{a if i % 2 == 0 else b}"/>' for i in range(3))
    return (f'<g clip-path="url(#krop)">{striber}</g>'
            f'<path d="M20 56 h24 l-3 26 h-18 z" fill="none" '
            f'stroke="{SORT}" stroke-width="1.5" stroke-opacity=".35"/>'
            f'<rect x="30" y="26" width="4" height="30" fill="{LINJE}"/>'
            f'<path d="M17 82 h30 l-4 8 h-22 z" fill="{LINJE}" '
            f'fill-opacity=".35"/>')


def _bånd(farve: str, y: int, h: int = 8) -> str:
    return f'<rect x="20" y="{y}" width="24" height="{h}" fill="{farve}"/>'


# ── Topbetegnelser ───────────────────────────────────────────────────────────
def _kegle(op: bool, y: int, farve: str = SORT) -> str:
    """En kegle. `op` betyder spidsen opad."""
    return (f'<path d="M22 {y + 14} h20 l-10 -14 z" fill="{farve}"/>' if op
            else f'<path d="M22 {y} h20 l-10 14 z" fill="{farve}"/>')


def _kugle(y: int, farve: str = SORT) -> str:
    return f'<circle cx="32" cy="{y}" r="7" fill="{farve}"/>'


def _kryds(y: int, farve: str = GUL, stående: bool = False) -> str:
    if stående:
        return (f'<path d="M32 {y - 8} v16 M24 {y} h16" stroke="{farve}" '
                f'stroke-width="4" stroke-linecap="round"/>')
    return (f'<path d="M26 {y - 6} l12 12 M38 {y - 6} l-12 12" '
            f'stroke="{farve}" stroke-width="4" stroke-linecap="round"/>')


def _dåse(y: int, farve: str = RØD) -> str:
    return f'<rect x="23" y="{y}" width="18" height="14" fill="{farve}"/>'


_CLIP = ('<defs><clipPath id="krop">'
         '<path d="M20 56 h24 l-3 26 h-18 z"/></clipPath></defs>')


# ── Afmærkningen ─────────────────────────────────────────────────────────────
MARKS: tuple[Mark, ...] = (
    Mark(
        'bagbord', 'Bagbords sidemærke',
        meaning='Rød, dåseformet. Står i bagbords side af løbet, når du '
                'sejler ind — mod havn, op ad et løb, eller den vej '
                'afmærkningsretningen går på søkortet.',
        action='Hold det i bagbord, når du går ind. Ud igen: i styrbord.',
        light='Rødt. Enhver karakter.',
        memo='Rødt i bagbord, når du går ind. I Amerika er det omvendt — '
             'dér gælder IALA B.',
        svg=_bøje(_CLIP + _krop(RØD), _dåse(28, RØD))),
    Mark(
        'styrbord', 'Styrbords sidemærke',
        meaning='Grøn, spids som en kegle. Står i styrbords side af løbet, '
                'når du sejler ind.',
        action='Hold det i styrbord, når du går ind. Ud igen: i bagbord.',
        light='Grønt. Enhver karakter.',
        svg=_bøje(_CLIP + _krop(GRØN), _kegle(True, 28, GRØN))),
    Mark(
        'nord', 'Nordmærke',
        meaning='Sort øverst, gul nederst. To kegler med spidserne opad — '
                'de peger op mod det sorte.',
        action='Passér nord for mærket. Farvandet syd for det er ikke sikkert.',
        light='Hvidt, uafbrudt hurtigblink: Q eller VQ.',
        memo='Keglerne peger hen mod den side, du skal gå.',
        svg=_bøje(_CLIP + _krop(GUL, _bånd(SORT, 56, 13)),
                  _kegle(True, 6, SORT) + _kegle(True, 22, SORT))),
    Mark(
        'øst', 'Østmærke',
        meaning='Sort, gult bånd, sort. To kegler bund mod bund.',
        action='Passér øst for mærket.',
        light='Hvidt: Q(3) 10s eller VQ(3) 5s.',
        memo='Tre blink som klokken tre — øst.',
        svg=_bøje(_CLIP + _krop(SORT, _bånd(GUL, 66, 9)),
                  _kegle(True, 6, SORT) + _kegle(False, 22, SORT))),
    Mark(
        'syd', 'Sydmærke',
        meaning='Gul øverst, sort nederst. To kegler med spidserne nedad.',
        action='Passér syd for mærket.',
        light='Hvidt: Q(6) + langt blink 15s, eller VQ(6) + langt blink 10s.',
        memo='Seks blink som klokken seks — syd. Det lange blink er der, '
             'så du ikke kommer i tvivl om, hvor gruppen slutter.',
        svg=_bøje(_CLIP + _krop(SORT, _bånd(GUL, 56, 13)),
                  _kegle(False, 6, SORT) + _kegle(False, 22, SORT))),
    Mark(
        'vest', 'Vestmærke',
        meaning='Gul, sort bånd, gul. To kegler spids mod spids — som et '
                'timeglas.',
        action='Passér vest for mærket.',
        light='Hvidt: Q(9) 15s eller VQ(9) 10s.',
        memo='Ni blink som klokken ni — vest.',
        svg=_bøje(_CLIP + _krop(GUL, _bånd(SORT, 66, 9)),
                  _kegle(False, 6, SORT) + _kegle(True, 22, SORT))),
    Mark(
        'fare', 'Enkeltstående fare',
        meaning='Sort med et eller flere brede røde bånd. To sorte kugler '
                'over hinanden.',
        action='Der er farbart vand hele vejen rundt, men faren ligger lige '
               'dér. Gå udenom med god margen.',
        light='Hvidt: to blink, Fl(2) 5s.',
        svg=_bøje(_CLIP + _krop(SORT, _bånd(RØD, 62, 12)),
                  _kugle(10) + _kugle(28))),
    Mark(
        'sikkert', 'Sikkert vand',
        meaning='Røde og hvide lodrette striber. Én rød kugle.',
        action='Der er vand hele vejen rundt. Bruges midt i et løb og som '
               'landfaldsbøje — dén, man styrer efter, når man kommer ind '
               'fra søen.',
        light='Hvidt: Iso, Oc, langt blink hvert 10. sekund, eller morse A.',
        svg=_bøje(_CLIP + _stribet(RØD, HVID), _kugle(28, RØD))),
    Mark(
        'saerlig', 'Særligt mærke',
        meaning='Gult, med et liggende gult kryds.',
        action='Markerer noget andet end sejladsen: kabler, rørledninger, '
               'badeområder, opdræt, kapsejladsbaner. Slå op i søkortet, '
               'hvad det er, før du sejler henover.',
        light='Gult.',
        svg=_bøje(_CLIP + _krop(GUL), _kryds(30))),
    Mark(
        'nyfare', 'Ny fare',
        meaning='Blå og gule lodrette striber. Stående gult kryds.',
        action='Et vrag eller en fare, der lige er opstået, og som endnu '
               'ikke står i søkortet. Hold godt klar.',
        light='Skiftevis blåt og gult, ét sekund hver.',
        svg=_bøje(_CLIP + _stribet(BLÅ, GUL), _kryds(28, GUL, stående=True))),
)


# ── Fyrkarakterer ────────────────────────────────────────────────────────────
# Sådan læses den tekst, der står ved et fyr i søkortet.
LIGHTS: tuple[tuple[str, str], ...] = (
    ('Fl', 'Blink — lyset er kortere end mørket.'),
    ('LFl', 'Langt blink — mindst to sekunder.'),
    ('Oc', 'Formørkelse — lyset er længere end mørket.'),
    ('Iso', 'Lige lang tid tændt og slukket.'),
    ('Q', 'Hurtigblink, omkring 50–60 i minuttet.'),
    ('VQ', 'Meget hurtigt blink, omkring 100–120 i minuttet.'),
    ('F', 'Fast lys, der ikke blinker.'),
    ('Mo(A)', 'Morse A: kort-langt. Bruges på landfaldsbøjer.'),
    ('(3)', 'Tallet i parentes er antal blink i gruppen.'),
    ('10s', 'Sekundtallet er hele periodens længde — tag tid på den.'),
    ('W R G', 'Farven: hvid, rød, grøn.'),
)

LIGHT_EXAMPLE = ('Fl(3)WR.10s', 'Tre blink, hvidt i én retning og rødt i en '
                                'anden, og det hele gentager sig hvert '
                                'tiende sekund.')

SECTORS = ('Et sektorfyr viser forskellig farve i forskellige retninger. '
           'Hvidt betyder som regel, at du er i det rene løb; rødt og grønt, '
           'at du er ude af det til hver sin side. Hvilken side hvad er, '
           'står i søkortet — det er ikke det samme alle steder.')


# ── Lanterner ────────────────────────────────────────────────────────────────
@dataclass(frozen=True)
class Signal:
    """Ét signal: hvad man ser eller hører, og hvad det betyder."""
    what: str
    means: str


LANTERNS: tuple[Signal, ...] = (
    Signal('Rød og grøn side om side, ingen hvid over',
           'En sejlbåd for sejl, der kommer lige imod dig.'),
    Signal('Rød og grøn med ét hvidt lys over',
           'Et motorfartøj, der kommer lige imod dig.'),
    Signal('Rød og grøn med to hvide over hinanden',
           'Et motorfartøj over 50 meter — og det bagerste hvide lys er '
           'højest. Står de to hvide lodret over hinanden, kommer det lige '
           'imod dig.'),
    Signal('Kun grønt', 'Du ser dens styrbords side. Den går fra bagbord '
                        'mod styrbord foran dig.'),
    Signal('Kun rødt', 'Du ser dens bagbords side. Som udgangspunkt er det '
                       'dig, der viger — men se på pejlingen, ikke på '
                       'farven alene.'),
    Signal('Kun hvidt agter', 'Du ser den bagfra. Du indhenter den, og så '
                              'er det dig, der holder klar.'),
    Signal('Ét hvidt rundtlysende, ingen andet',
           'Et fartøj for anker — eller en lille båd under 7 meter.'),
    Signal('To røde over hinanden, rundtlysende',
           'Ikke under kommando. Den kan ikke styre. Hold klar.'),
    Signal('Rød–hvid–rød lodret',
           'Begrænset i sin evne til at manøvrere. Uddybning, bugsering, '
           'dykkerarbejde. Hold godt klar.'),
    Signal('Grønt over hvidt', 'Trawler. Der kan gå wire langt agterud.'),
)

DAY_SHAPES: tuple[Signal, ...] = (
    Signal('En sort kugle', 'For anker.'),
    Signal('En sort kegle med spidsen nedad',
           'En sejlbåd, der også har motoren i gang. Så gælder reglerne for '
           'motorfartøjer, ikke for sejlbåde — og det er dét, folk glemmer.'),
    Signal('To sorte kugler over hinanden', 'Ikke under kommando.'),
    Signal('Kugle – rombe – kugle',
           'Begrænset i sin evne til at manøvrere.'),
    Signal('En sort cylinder', 'Begrænset af sin dybgang.'),
    Signal('Tre sorte kugler over hinanden', 'Fartøjet står på grund.'),
)


# ── Lydsignaler ──────────────────────────────────────────────────────────────
# Et kort stød er omkring et sekund, et langt fire til seks.
SOUND_MANOEUVRE: tuple[Signal, ...] = (
    Signal('Ét kort stød', 'Jeg drejer til styrbord.'),
    Signal('To korte stød', 'Jeg drejer til bagbord.'),
    Signal('Tre korte stød', 'Jeg bakker.'),
    Signal('Fem korte stød eller flere',
           'Jeg forstår ikke, hvad du har tænkt dig — eller: du gør ikke '
           'nok for at holde klar. Det er advarslen.'),
    Signal('Ét langt stød',
           'Jeg nærmer mig et sving eller et sted, hvor jeg ikke kan se, '
           'hvad der kommer.'),
)

SOUND_FOG: tuple[Signal, ...] = (
    Signal('Ét langt hvert andet minut',
           'Motorfartøj med fart gennem vandet.'),
    Signal('To lange hvert andet minut',
           'Motorfartøj, der ligger stille i vandet.'),
    Signal('Ét langt og to korte hvert andet minut',
           'Sejlbåd for sejl. Det samme lyder fra en fisker, en bugserende '
           'og en manøvrehæmmet — så du ved ikke hvilken, kun at du skal '
           'holde klar.'),
    Signal('Klokke i fem sekunder hvert minut',
           'Fartøj for anker. Er det over 100 meter, kommer der en gongong '
           'agter bagefter.'),
)


# ── Nød ──────────────────────────────────────────────────────────────────────
DISTRESS: tuple[Signal, ...] = (
    Signal('VHF kanal 16 — MAYDAY',
           'Sig MAYDAY tre gange, bådens navn, position, hvad der er sket, '
           'og hvor mange I er. DSC-nødknappen sender position og kaldesignal '
           'af sig selv.'),
    Signal('112', 'Går videre til JRCC. Virker, når du har mobildækning, og '
                  'det har man tit tættere på land end man tror.'),
    Signal('Rødt faldskærmsblus eller rødt håndblus',
           'Nød. Et hvidt blus er derimod en advarsel — ikke det samme.'),
    Signal('Orange røgsignal', 'Nød, om dagen. Ses langt i klart vejr.'),
    Signal('Langsomme bevægelser op og ned med begge arme',
           'Nød. Det er det signal, man kan give uden udstyr.'),
    Signal('Orange dug med sort firkant og cirkel',
           'Nød, set fra luften. Læg den, så et fly kan se den.'),
)


# ── Til manualen ─────────────────────────────────────────────────────────────
# Teksten, der skal med i manualen og kunne hentes. Formen er den, help.py
# bruger, så der kun findes én kilde — retter man her, er det rettet begge
# steder.
HELP: tuple[tuple[str, str, str, tuple[str, ...]], ...] = (
    ('afmaerkning', 'Sømærker',
     'Hvad mærkerne i vandet betyder, og hvad du gør ved dem.',
     ('Afmærkningen er IALA A. Den gælder i Danmark, Tyskland, Sverige, '
      'Norge og resten af Europa. I Nord- og Sydamerika er de røde og grønne '
      'sidemærker byttet om.',
      'Sidemærkerne siger, hvor løbet er: rødt og dåseformet i bagbord, '
      'grønt og spidst i styrbord, når du sejler ind. Ud igen er det '
      'omvendt.',
      'Kardinalmærkerne siger, hvilken side du skal gå på. Keglerne øverst '
      'peger hen mod den side, der er ren: to kegler opad er et nordmærke, '
      'og så skal du nord om. Antallet af blink følger uret — tre for øst, '
      'seks for syd, ni for vest.',
      'Enkeltstående fare er sort med røde bånd og to kugler. Der er vand '
      'hele vejen rundt, men gå ikke tæt på. Sikkert vand er rød-hvidt '
      'stribet med en rød kugle — dér er der vand hele vejen rundt.',
      'Under bogikonet i toppen ligger tegningerne af dem alle sammen, med '
      'fyrkarakter og huskeregel.')),
    ('fyr', 'Fyr og karakterer',
     'Sådan læser du Fl(3)WR.10s — og hvad et sektorfyr fortæller.',
     ('Bogstaverne siger, hvordan lyset opfører sig: Fl er blink, Oc er '
      'formørkelse, Iso er lige lang tid tændt og slukket, Q er hurtigblink. '
      'Tallet i parentes er antal blink i gruppen, og sekundtallet er hele '
      'periodens længde.',
      'Fl(3)WR.10s er altså tre blink, hvidt i én retning og rødt i en '
      'anden, gentaget hvert tiende sekund. Tag tid på perioden med et ur — '
      'det er dét, der skiller to fyr, der ellers ligner hinanden.',
      'Et sektorfyr viser forskellig farve i forskellige retninger. Hvidt '
      'betyder som regel det rene løb. Hvilken side rødt og grønt dækker, '
      'står i søkortet — det er ikke det samme alle steder.')),
    ('lanterner', 'Lanterner og dagsignaler',
     'Hvad du ser om natten, og hvad det siger om, hvem der viger.',
     ('Ser du både rødt og grønt uden hvidt over, er det en sejlbåd, der '
      'kommer lige imod dig. Er der ét hvidt lys over, er det et '
      'motorfartøj. Ser du kun hvidt, ser du den bagfra — og så er det dig, '
      'der indhenter og skal holde klar.',
      'To røde over hinanden betyder, at fartøjet ikke er under kommando. '
      'Rød-hvid-rød betyder, at det er begrænset i sin evne til at '
      'manøvrere. Begge dele betyder: hold godt klar.',
      'Om dagen: en sort kugle er for anker. En sort kegle med spidsen '
      'nedad er en sejlbåd, der også har motoren i gang — og så gælder '
      'reglerne for motorfartøjer. Den kegle glemmer næsten alle, og den '
      'ændrer, hvem der viger.')),
    ('lydsignaler', 'Lyd- og nødsignaler',
     'Ét kort er styrbord, fem korte er en advarsel.',
     ('Når I kan se hinanden: ét kort stød betyder "jeg drejer til '
      'styrbord", to korte "til bagbord", tre korte "jeg bakker". Fem korte '
      'eller flere er advarslen — jeg forstår dig ikke, eller du gør ikke '
      'nok for at holde klar.',
      'I tåge lyder det hvert andet minut: ét langt fra et motorfartøj med '
      'fart i, to lange fra et, der ligger stille, og ét langt plus to korte '
      'fra en sejlbåd — og fra en fisker og en manøvrehæmmet. Så du ved '
      'ikke hvilken, kun at du skal holde klar.',
      'I nød: MAYDAY på kanal 16 eller DSC-nødknappen. 112 går videre til '
      'JRCC og virker, så længe du har mobildækning. Røde blus er nød; et '
      'hvidt blus er en advarsel og noget helt andet.')),
    ('vhf', 'VHF — opkald og nødopkald',
     'Kanal 16 til nød og opkald. Og MAYDAY ord for ord.',
     ('Til daglig kræver en VHF et SRC-bevis, og anlægget skal være tilladt '
      'til båden. Men er nogen i fare, må enhver ombord bruge ethvert middel '
      'til at tilkalde hjælp. Så tag mikrofonen — ingen er nogensinde blevet '
      'straffet for at kalde MAYDAY, når der var brug for det.',
      'Kanal 16 er til nød og til at kalde hinanden op. Har I fået fat i '
      'hinanden, så aftal en arbejdskanal — 06, 08, 72 eller 77 — og flyt '
      'derover, så 16 er fri. Kanal 13 er skib til skib om manøvrer; det er '
      'dér, du kalder færgen i et smalt løb. På 70 tales der aldrig — den er '
      'radioens egen til DSC.',
      'Et opkald lyder: modtagerens navn to gange, "dette er" og dit eget '
      'navn to gange, og så Skift. Skift betyder "nu venter jeg svar". Slut '
      'betyder "samtalen er forbi".',
      'Et nødopkald har en fast rækkefølge, og det er rækkefølgen, der gør, '
      'at redningen ved, hvor de skal hen og hvad de skal have med: MAYDAY '
      'tre gange, bådens navn tre gange, MAYDAY og navnet igen, position, '
      'hvad der er sket, hvad du beder om, hvor mange I er, hvordan båden '
      'ser ud — og Skift. Svarer ingen, så gentag det hele.',
      'PAN-PAN er den, der ikke er livstruende endnu: motoren er død i et '
      'sejlløb, nogen er syg men ikke i fare. SÉCURITÉ er en advarsel til '
      'alle andre om noget i vandet.',
      'Den røde knap under klappen er DSC. Hold den nede i fem sekunder — '
      'radioen sender bådens MMSI og positionen af sig selv. Følg altid op '
      'med stemmen på 16: alarmen siger, at nogen har brug for hjælp, ikke '
      'hvad der er sket. Hele opkaldet står ord for ord under bogikonet på '
      'kortet.')),
    ('ikke-farer', 'Hvorfor vi ikke advarer om grunde',
     'Sejlplan kender land og vand — ikke dybder. Farerne står i søkortet.',
     ('Ruten lægges uden om land med en maske over de skandinaviske '
      'farvande. Masken kender kysten. Den kender ikke dybder, grunde, rev, '
      'sten, spærrede områder, skydeområder eller sejlrender.',
      'Vi kunne godt skrive "pas på grunden her" ud fra et gæt. Vi lader '
      'være. En advarsel, der ser rigtig ud og er forkert, er farligere end '
      'ingen advarsel — for så holder man op med at kigge i søkortet.',
      'Farerne står i søkortet og i Efterretninger for Søfarende. Læg ruten '
      'her, og gå den efter dér. Særligt i smalt farvand, tæt på kysten og '
      'omkring pynter og rev.')),
)


def help_topics():
    """Emnerne til manualen — som `help.Topic` forventer dem."""
    return HELP


# ── VHF ──────────────────────────────────────────────────────────────────────
# Om beviset: i Danmark kræver det et SRC-certifikat at betjene en VHF, og
# anlægget skal være tilladt til fartøjet. Det gælder den daglige brug.
#
# Det gælder ikke, når nogen er i fare. I nød må enhver ombord bruge et hvilket
# som helst middel til at tilkalde hjælp — det er derfor, det her står her, og
# derfor det står med ordene, man skal sige, og ikke som en henvisning til et
# kursus. Den, der står med en bevidstløs ombord, skal ikke først finde ud af,
# om han må.
VHF_CERTIFICATE = (
    'Til daglig kræver en VHF et SRC-bevis, og anlægget skal være tilladt til '
    'båden. Men er nogen i fare, må enhver ombord bruge ethvert middel til at '
    'tilkalde hjælp. Så tag mikrofonen. Ingen er nogensinde blevet straffet '
    'for at kalde MAYDAY, når der var brug for det.')

CHANNELS: tuple[tuple[str, str], ...] = (
    ('16', 'Nød, hastemeddelelser og opkald. Lyt her, når du sejler. Flyt '
           'over på en arbejdskanal, så snart I har fået fat i hinanden.'),
    ('70', 'DSC — den digitale nødknap. Her tales der aldrig. Radioen bruger '
           'kanalen selv.'),
    ('13', 'Skib til skib om manøvrer. Det er her, du kalder færgen eller '
           'coasteren, der kommer imod dig i et smalt løb.'),
    ('06 · 08 · 72 · 77', 'Arbejdskanaler mellem både. Aftal en, når I har '
                          'kaldt hinanden op på 16.'),
    ('Lyngby Radio', 'Den danske kystradio. Nødtrafik, farvandsudsigter og '
                     'efterretninger. Kalder du 16, hører de med.'),
    ('Havnens kanal', 'Mange havne og broer lytter på deres egen kanal. Den '
                      'står i havnelodsen — slå den op, før du kommer.'),
)

PROWORDS: tuple[tuple[str, str], ...] = (
    ('SKIFT', 'Jeg er færdig, og jeg venter svar. På engelsk: OVER.'),
    ('SLUT', 'Samtalen er slut. Jeg venter ikke svar. OUT.'),
    ('MODTAGET', 'Jeg har hørt og forstået. ROGER.'),
    ('GENTAG', 'Sig det igen. SAY AGAIN.'),
    ('VENT', 'Bliv på kanalen, jeg kommer tilbage. STAND BY.'),
    ('STAVER', 'Nu bogstaverer jeg. I SPELL.'),
)

# Selve opkaldet. Tre gange var reglen dengang, forbindelserne var dårlige;
# to er nok i dag, og på kanal 16 er kortere altid bedre.
CALL_SCRIPT = (
    'Marstal Havn, Marstal Havn — dette er Havfruen, Havfruen. Skift.',
    'Når I har svaret hinanden: aftal en arbejdskanal og flyt derover. '
    'Kanal 16 skal være fri.',
)


@dataclass(frozen=True)
class Line:
    """Én linje i et opkald: hvad man siger, og hvad man fylder i."""
    say: str
    note: str = ''


MAYDAY: tuple[Line, ...] = (
    Line('MAYDAY — MAYDAY — MAYDAY',
         'Kun når der er fare for liv eller for at båden går tabt.'),
    Line('Dette er Havfruen, Havfruen, Havfruen',
         'Bådens navn tre gange. Sig også kaldesignal eller MMSI, hvis du '
         'har det.'),
    Line('MAYDAY, Havfruen', 'Én gang mere, så den, der skriver ned, ved, '
                             'hvem meldingen er fra.'),
    Line('Min position er …',
         'Bredde og længde, hvis du har dem. Ellers: pejling og afstand til '
         'noget, alle kender — "to sømil nord for Sprogø".'),
    Line('Jeg har …',
         'Hvad der er sket. Brand, vand i båden, mand overbord, alvorlig '
         'tilskadekomst, grundstødning.'),
    Line('Jeg har brug for …',
         'Hvad du beder om. Redning, lægehjælp, slæbning.'),
    Line('Vi er … personer ombord',
         'Antallet. Det er dét, der afgør, hvad de sender.'),
    Line('… og båden er …',
         'Kort: længde, farve, sejlbåd eller motorbåd. Nok til at finde jer.'),
    Line('Skift', 'Slip knappen og lyt. Svarer ingen, så gentag det hele.'),
)

PAN_PAN = (
    'PAN-PAN, tre gange, er den, der ikke er livstruende endnu: motoren er '
    'død i et sejlløb, nogen er syg, men ikke i fare, I er drevet på grund i '
    'roligt vejr. Ellers er formen den samme som MAYDAY.',
    'SÉCURITÉ, tre gange, er en advarsel til alle andre — en drivende '
    'genstand, et sømærke der er væk. Sig den på 16 og flyt over på en '
    'arbejdskanal med selve meldingen.')

DSC = (
    'Den røde knap under klappen er DSC-nødalarmen. Hold den nede i fem '
    'sekunder. Radioen sender bådens MMSI og — er den koblet til en GPS — '
    'positionen, til alle skibe og kyststationer i nærheden.',
    'Følg altid op med stemmen på kanal 16. Alarmen siger, at nogen har '
    'brug for hjælp; den siger ikke, hvad der er sket.',
    'Hører du en andens nødalarm og ingen svarer, så svar. Kan du ikke '
    'hjælpe selv, så giv den videre: "MAYDAY RELAY" og hvad du har hørt.')
