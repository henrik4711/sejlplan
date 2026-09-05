"""Forsiden, robots.txt og sitemap — og at delelinks stadig virker.

Forsiden findes, fordi `/` indtil nu serverede en tom Vue-skal: NiceGUI tegner
fladen over en websocket, så en crawler fik nul ord udleveret. Prøverne her
holder fast i de tre ting, der er lette at komme til at bryde igen:

* at der faktisk står tekst i svaret — ikke bare et tomt skelet
* at de mærker, Google læser, er der og peger rigtigt
* at et gammelt delelink til `/?rute=…` ikke holder op med at virke, fordi
  vi har flyttet appen
"""
from __future__ import annotations

import json
import re

import pytest
from fastapi.testclient import TestClient

from app import i18n, landing

pytestmark = pytest.mark.module_under_test('main')


@pytest.fixture
def klient():
    import main  # noqa: F401 — registrerer ruterne
    from nicegui import app as nicegui_app
    return TestClient(nicegui_app)


# ── Der skal stå noget ────────────────────────────────────────────────────────
@pytest.mark.parametrize('sti', list(landing.PATHS.values()))
def test_forsiden_har_rigtig_tekst(klient, sti):
    """En crawler skal få indholdet i selve svaret, ikke efter en websocket."""
    svar = klient.get(sti)
    assert svar.status_code == 200
    krop = svar.text
    # Overskriften, brødteksten og knappen skal stå i HTML'en.
    assert '<h1' in krop
    assert krop.count('<h2') >= 3
    # Grov måling af, hvor meget læsbar tekst der er uden mærker. En tom
    # skal ville lande på nul; forsiden ligger langt over tusind tegn.
    ren = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', krop, flags=re.S)
    ren = re.sub(r'<[^>]+>', ' ', ren)
    assert len(ren.split()) > 250, 'forsiden har for lidt tekst til at blive fundet'


@pytest.mark.parametrize('kode,sti', list(landing.PATHS.items()))
def test_forsiden_har_de_maerker_google_laeser(klient, kode, sti):
    krop = klient.get(sti).text
    assert f'<html lang="{i18n.LANGUAGES and landing.TEXT[kode]["lang"]}"' in krop
    assert '<meta name="description" content="' in krop
    assert 'rel="canonical"' in krop
    assert 'property="og:title"' in krop
    assert 'name="twitter:card"' in krop
    # Hvert sprog skal pege på de andre, ellers ser Google tre løsrevne sider.
    for anden in landing.PATHS:
        assert f'hreflang="{anden}"' in krop
    assert 'hreflang="x-default"' in krop


@pytest.mark.parametrize('sti', list(landing.PATHS.values()))
def test_strukturerede_data_er_gyldig_json(klient, sti):
    """JSON-LD skal kunne læses. Et citationstegn i teksten må ikke brække den."""
    krop = klient.get(sti).text
    blokke = re.findall(
        r'<script type="application/ld\+json">(.*?)</script>', krop, flags=re.S)
    assert blokke, 'ingen strukturerede data'
    data = json.loads(blokke[0])
    typer = {n['@type'] for n in data['@graph']}
    assert {'WebSite', 'SoftwareApplication', 'FAQPage'} <= typer
    faq = next(n for n in data['@graph'] if n['@type'] == 'FAQPage')
    assert len(faq['mainEntity']) >= 5


# ── robots og sitemap ─────────────────────────────────────────────────────────
def test_robots_findes_og_peger_paa_sitemap(klient):
    svar = klient.get('/robots.txt')
    assert svar.status_code == 200
    assert 'Sitemap: ' in svar.text
    # Planlæggeren er en levende flade bag en websocket — der er intet at
    # indeksere, og en crawler ville åbne en session pr. besøg.
    assert f'Disallow: {landing.APP_PATH}' in svar.text


def test_sitemap_har_alle_sprog(klient):
    svar = klient.get('/sitemap.xml')
    assert svar.status_code == 200
    for sti in landing.PATHS.values():
        assert sti in svar.text or sti == '/'
    assert svar.text.count('<url>') == len(landing.PATHS)


# ── Intet må holde op med at virke ────────────────────────────────────────────
def test_gammelt_delelink_sendes_videre(klient):
    """`/?rute=…` er dét, folk har liggende. Det må ikke lande på forsiden."""
    svar = klient.get('/?rute=abc123', follow_redirects=False)
    assert svar.status_code in (302, 307)
    mål = svar.headers['location']
    assert mål.startswith(landing.APP_PATH)
    assert 'rute=abc123' in mål


def test_forsiden_uden_rute_er_forsiden(klient):
    svar = klient.get('/', follow_redirects=False)
    assert svar.status_code == 200


def test_appen_er_registreret_paa_sin_egen_sti(klient):
    """Planlæggeren skal stadig findes — bare et andet sted.

    Selve opbygningen prøves i `test_side.py` med en rigtig browser-klient;
    en almindelig TestClient kan ikke tegne en NiceGUI-side. Her hævder vi
    kun det, forsiden kunne komme til at tage fra den: at ruten findes.
    """
    from nicegui import app as nicegui_app
    stier = {getattr(r, 'path', None) for r in nicegui_app.routes}
    assert landing.APP_PATH in stier
    assert '/' in stier
