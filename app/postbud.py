"""Postbuddet: beskeder og både bliver leveret, ikke hentet.

Før spurgte hver browser databasen hvert tyvende sekund, om der var sket
noget. Det er tre ting på én gang: en besked kan ligge og vente i tyve
sekunder, en båd kan flytte sig uden at nogen ser det, og ti browsere åbne
laver tredive opslag i minuttet, hvor svaret næsten altid er "nej, ingenting".

Her vender vi det om. Den, der sender en besked, siger til. Den, der flytter
sig, siger til. De browsere, der lytter, får det at vide i samme øjeblik —
over den forbindelse, de har i forvejen.

**Det her er én proces.** Køen ligger i hukommelsen, så to servere ville ikke
kunne se hinandens hændelser. Derfor bliver det langsomme opslag stående som
sikkerhedsnet: det kører sjældnere end før, og det er dét, der ville bære, hvis
vi en dag kører flere. Skal det virke rigtigt over flere processer, er det
databasen eller en rigtig kø, der skal bære det — ikke det her modul.

**Hvem der må høre hvad.** En besked går kun til modtagerens mærke. Hændelsen
om, at flåden har flyttet sig, siger ikke *hvor* nogen er — den siger kun "kig
efter igen", og opslaget bagefter går gennem de samme regler som altid: man ser
kun andre, hvis man selv er synlig.
"""
from __future__ import annotations

import asyncio
from dataclasses import dataclass, field

# Så mange hændelser må ligge og vente til én browser, før vi smider de
# ældste væk. En browser, der ikke har hentet sine hændelser, er væk — og så
# skal den ikke holde hukommelse i live.
KØ_MAX = 32

BESKED = 'besked'
FLÅDE = 'flåde'


@dataclass
class Hændelse:
    """Noget, der er sket. Aldrig hvad — kun at der er sket noget."""
    slags: str
    # Kun sat på beskeder: hvem der skrev. Nok til at åbne den rigtige samtale
    # uden at teksten skal gennem køen.
    fra_mærke: str = ''
    fra_navn: str = ''


@dataclass(eq=False)          # hver lytter er sig selv, også med samme mærke
class _Abonnent:
    mærke: str
    kø: asyncio.Queue = field(default_factory=lambda: asyncio.Queue(KØ_MAX))


_abonnenter: dict[str, set[_Abonnent]] = {}


def subscribe(mærke: str) -> _Abonnent | None:
    """Lyt efter hændelser til det her mærke."""
    if not mærke:
        return None
    a = _Abonnent(mærke)
    _abonnenter.setdefault(mærke, set()).add(a)
    return a


def unsubscribe(a: _Abonnent | None) -> None:
    """Hold op med at lytte. Skal altid kaldes — ellers vokser tabellen."""
    if a is None:
        return
    hold = _abonnenter.get(a.mærke)
    if not hold:
        return
    hold.discard(a)
    if not hold:
        _abonnenter.pop(a.mærke, None)


def _læg(a: _Abonnent, h: Hændelse) -> None:
    """Læg en hændelse i køen. Er den fuld, ryger den ældste.

    En fuld kø betyder, at ingen har hentet i lang tid. Så er de gamle
    hændelser alligevel uden værdi — det er den nyeste, der betyder noget.
    """
    try:
        a.kø.put_nowait(h)
    except asyncio.QueueFull:
        try:
            a.kø.get_nowait()
            a.kø.put_nowait(h)
        except (asyncio.QueueEmpty, asyncio.QueueFull):
            pass


def besked_til(mærke: str, fra_mærke: str = '', fra_navn: str = '') -> int:
    """Sig til modtageren, at der er kommet en besked.

    Kun til det ene mærke. Ingen andre får at vide, at der blev skrevet.
    """
    h = Hændelse(BESKED, fra_mærke=fra_mærke, fra_navn=fra_navn)
    ramt = list(_abonnenter.get(mærke, ()))
    for a in ramt:
        _læg(a, h)
    return len(ramt)


def flåden_flyttede_sig(undtagen: str = '') -> int:
    """Sig til alle, der lytter, at der er noget nyt at kigge efter.

    Hændelsen bærer ingen position. Den siger "kig igen", og opslaget bagefter
    går gennem de samme regler som altid. Det er med vilje: så kan en hændelse
    aldrig komme til at sige mere, end den, der modtager den, må vide.

    Vi sender til alle, ikke kun dem i nærheden. Med de tal, det her har — et
    par hundrede både på det højeste — er det ingenting, og alternativet ville
    kræve, at postbuddet kendte alles positioner. Bliver det en dag til
    tusinder, er det her, der skal filtreres.
    """
    h = Hændelse(FLÅDE)
    n = 0
    for mærke, hold in list(_abonnenter.items()):
        if mærke == undtagen:
            continue
        for a in list(hold):
            _læg(a, h)
            n += 1
    return n


def lyttere(mærke: str = '') -> int:
    """Hvor mange browsere lytter. Til /api/status og til prøverne."""
    if mærke:
        return len(_abonnenter.get(mærke, ()))
    return sum(len(h) for h in _abonnenter.values())
