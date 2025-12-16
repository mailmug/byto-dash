import smtplib
from email.message import EmailMessage
from app.core.config import settings


def send_message(message: EmailMessage):
    with smtplib.SMTP(settings.MAIL_HOST, settings.MAIL_PORT) as server:
        server.login(settings.MAIL_USERNAME, settings.MAIL_PASSWORD)
        server.send_message(message)


