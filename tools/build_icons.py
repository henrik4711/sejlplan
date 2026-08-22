"""Tegn appens ikoner.

En app på hjemmeskærmen kendes på sit ikon, længe før nogen læser navnet. Så
det skal tegnes, ikke lånes: en sejlbåd i guld på dybt marineblåt, de samme to
farver som resten af fladen.

Ikonet findes i to udgaver. Den almindelige har afrundede hjørner og lidt luft
omkring sig. Den maskerbare fylder hele fladen, fordi Android selv klipper den
til den form, telefonen bruger — rund, firkantet eller noget derimellem — og
klipper den halvanden gang så tæt som man tror. Derfor står båden i den midterste
trediedel, hvor der ikke kan klippes.

Kør:  python tools/build_icons.py
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

OUT = Path(__file__).resolve().parent.parent / 'app' / 'static'

NAVY = (13, 27, 42, 255)
NAVY_TOP = (26, 48, 71, 255)
GOLD = (200, 147, 59, 255)
GOLD_LIGHT = (232, 185, 106, 255)

# Overprøvning: alt tegnes fire gange så stort og skaleres ned til sidst.
# Diagonale kanter bliver ellers trappede, og et ikon med trappede sejl ser
# billigt ud i netop den størrelse, hvor folk kigger på det.
SS = 4


def _background(size: int, full_bleed: bool) -> Image.Image:
    """Marineblå flade med et svagt lysere skær foroven, som en himmel."""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    sky = Image.new('RGBA', (size, size), NAVY)
    d = ImageDraw.Draw(sky)
    for y in range(size):
        f = 1.0 - y / size
        f = f * f                      # skæret samler sig i toppen
        d.line([(0, y), (size, y)],
               fill=tuple(round(a + (b - a) * f)
                          for a, b in zip(NAVY, NAVY_TOP)))

    if full_bleed:
        return sky

    mask = Image.new('L', (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        [0, 0, size - 1, size - 1], radius=round(size * 0.22), fill=255)
    img.paste(sky, (0, 0), mask)
    return img


def _boat(d: ImageDraw.ImageDraw, size: int, scale: float) -> None:
    """Sejlbåden: storsejl, fok og skrog. Alt i andele af fladen.

    `scale` er, hvor stor en del af ikonet båden må fylde. Den maskerbare
    udgave skal holde sig inde i midten, hvor telefonen ikke klipper.
    """
    c = size / 2
    u = size * scale                  # bådens egen bredde
    x = lambda f: c + (f - 0.5) * u   # noqa: E731 — kort er klarere her
    y = lambda f: c + (f - 0.5) * u   # noqa: E731

    # Storsejlet står agten for masten og fylder mest.
    d.polygon([(x(0.52), y(0.03)), (x(0.52), y(0.66)), (x(0.94), y(0.66))],
              fill=GOLD)
    # Fokken er mindre og lidt lysere, så de to sejl kan skelnes.
    d.polygon([(x(0.46), y(0.13)), (x(0.46), y(0.66)), (x(0.10), y(0.66))],
              fill=GOLD_LIGHT)

    # Skroget: en flad skål under sejlene.
    # Hjørnerne skal rundt om skroget i rækkefølge — agter, for, for, agter.
    # Bytter man de to nederste om, krydser kanterne, og skroget bliver til et
    # timeglas.
    hull_top = y(0.73)
    hull_bot = y(0.89)
    d.polygon([(x(0.03), hull_top), (x(0.97), hull_top),
               (x(0.72), hull_bot), (x(0.28), hull_bot)], fill=GOLD)
    # En flad bue lagt hen over bunden, så kølen ikke ender i en skarp kant.
    d.ellipse([x(0.28), hull_bot - u * 0.07, x(0.72), hull_bot + u * 0.05],
              fill=GOLD)


def build(size: int, name: str, *, maskable: bool = False) -> Path:
    big = size * SS
    img = _background(big, full_bleed=maskable)
    d = ImageDraw.Draw(img)
    # 0,62 til det almindelige ikon; 0,46 til det maskerbare, så båden bliver
    # inde i den sikre midte, uanset hvilken form telefonen klipper efter.
    _boat(d, big, 0.46 if maskable else 0.62)

    img = img.resize((size, size), Image.LANCZOS)
    path = OUT / name
    img.save(path, 'PNG', optimize=True)
    return path


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    made = [
        build(192, 'icon-192.png'),
        build(512, 'icon-512.png'),
        build(512, 'icon-maskable-512.png', maskable=True),
        # iOS bruger sit eget ikon og lægger selv afrundingen på, så det skal
        # være firkantet og uden gennemsigtighed.
        build(180, 'apple-touch-icon.png', maskable=True),
        build(32, 'favicon-32.png'),
    ]
    for p in made:
        print(f'{p.name:26} {p.stat().st_size / 1024:6.1f} kB')


if __name__ == '__main__':
    main()
