from datetime import datetime
from email.message import EmailMessage
from jinja2 import Environment, FileSystemLoader, select_autoescape

from app.core.config import settings
from app.mail.client import send_message
from app.mail.schemas import EmailSchema
from app.models.user import User

import pathlib

TEMPLATE_DIR = pathlib.Path(__file__).parent / "templates"

env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=select_autoescape(["html", "xml"]),
)


def send_email(data: EmailSchema):
    msg = EmailMessage()
    msg["From"] = settings.MAIL_FROM_ADDRESS
    msg["To"] = data.to
    msg["Subject"] = data.subject

    if data.text:
        msg.set_content(data.text)

    msg.add_alternative(data.html, subtype="html")

    send_message(msg)


def send_verification_email(user: User, token: str):
    template = env.get_template("verify_email.html")

    html = template.render(
        token=token,
        verify_url=f"{settings.FRONTEND_URL}/verify-user?email-token={token}",
        year=datetime.now().year,
        app_name=settings.APP_NAME
    )

    text = f"""
        Verify Your Email.

        Token:
        {token}
    """

    send_email(
        EmailSchema(
            to=user.email,
            subject="Verify Your Email",
            html=html,
            text=text,
        )
    )


def send_reset_password_email(user: User, token: str):
    template = env.get_template("reset_password.html")
    verify_url=f"{settings.FRONTEND_URL}/reset-password?email-token={token}"

    html = template.render(
        token=token,
        verify_url=verify_url,
        year=datetime.now().year,
        app_name=settings.APP_NAME
    )

    text = f"""
        Reset Password Notification.

        Verify:
        {verify_url}
    """

    send_email(
        EmailSchema(
            to=user.email,
            subject="Reset Password Notification",
            html=html,
            text=text,
        )
    )
