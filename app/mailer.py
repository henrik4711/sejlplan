"""Afsendelse af mail.

Kun to slags: bekræft din adresse, og nu er der vejr. Ikke nyhedsbreve, ikke
tilbud, ikke noget man skal frameldes bagefter — hver mail bærer sit eget link
til at stoppe vagten, og en vagt sender én besked og er så brugt.

Vi skriver aldrig til en adresse, der ikke selv har bekræftet den. Det er både
loven og almindelig anstændighed: uden bekræftelse kan enhver sætte naboens
adresse på en vagt.

Sendes med almindelig SMTP, så det virker med den udbyder, du nu har. Uden
opsætning er vejrvagten slået fra, og fladen siger det i stedet for at lade som
om, den virker.
"""
from __future__ import annotations

import asyncio
import smtplib
from email.message import EmailMessage
from email.utils import formataddr

from .config import settings
from .mishap import report

SENDER_NAME = 'Sejlplan'


def _send_blocking(msg: EmailMessage) -> None:
    port = settings.smtp_port
    # 465 er SMTP over TLS fra første byte; 587 begynder klart og løfter sig
    # med STARTTLS. Begge dele findes i naturen.
    if port == 465:
        with smtplib.SMTP_SSL(settings.smtp_host, port, timeout=25) as s:
            if settings.smtp_user:
                s.login(settings.smtp_user, settings.smtp_password)
            s.send_message(msg)
        return

    with smtplib.SMTP(settings.smtp_host, port, timeout=25) as s:
        s.ehlo()
        try:
            s.starttls()
            s.ehlo()
        except smtplib.SMTPException:
            # Nogle interne servere kører uden TLS. Så gør vi det, de kan.
            pass
        if settings.smtp_user:
            s.login(settings.smtp_user, settings.smtp_password)
        s.send_message(msg)


async def send(to: str, subject: str, text: str, html: str = '') -> bool:
    """Send én mail. Falsk hvis det ikke lykkedes — aldrig en undtagelse opad.

    En mail, der ikke kan sendes, må ikke vælte den baggrundsopgave, der er i
    gang med at kigge på tyve andre vagter.
    """
    if not settings.mail_available:
        return False

    msg = EmailMessage()
    msg['From'] = formataddr((SENDER_NAME, settings.mail_from))
    msg['To'] = to
    msg['Subject'] = subject
    msg.set_content(text)
    if html:
        msg.add_alternative(html, subtype='html')

    try:
        # smtplib er synkron. Den lægges i en tråd, så serveren kan svare
        # brugere imens.
        await asyncio.to_thread(_send_blocking, msg)
        return True
    except Exception as exc:      # noqa: BLE001 — vi vil have alle slags
        report(exc, f'afsendelse til {to}')
        return False
