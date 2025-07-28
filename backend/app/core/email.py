import smtplib
from email.message import EmailMessage

from app.core.config import settings


def send_email(to: str, subject: str, body: str) -> None:
    """Send an email using SMTP.

    If SMTP_HOST is not configured, the message is printed to stdout instead of
    being sent. This allows tests to run without a mail server configured.
    """
    host = settings.SMTP_HOST
    port = settings.SMTP_PORT
    user = settings.SMTP_USER
    password = settings.SMTP_PASSWORD
    from_addr = settings.EMAIL_FROM

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = to
    msg.set_content(body)

    if not host:
        print(f"Email (mock) to {to}: {subject}\n{body}")
        return

    with smtplib.SMTP(host, port) as server:
        server.starttls()
        if user and password:
            server.login(user, password)
        server.send_message(msg)
