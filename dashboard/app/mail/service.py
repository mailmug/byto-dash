from datetime import datetime
from email.message import EmailMessage
from jinja2 import Environment, FileSystemLoader, select_autoescape

from app.core.config import settings
from app.mail.client import send_message
from app.mail.schemas import EmailSchema

import pathlib

TEMPLATE_DIR = pathlib.Path(__file__).parent / "templates"

env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=select_autoescape(["html", "xml"]),
)


async def send_email(data: EmailSchema):
    msg = EmailMessage()
    msg["From"] = settings.MAIL_FROM_ADDRESS
    msg["To"] = data.to
    msg["Subject"] = data.subject

    if data.text:
        msg.set_content(data.text)

    msg.add_alternative(data.html, subtype="html")

    await send_message(msg)


async def send_verification_email(email: str, token: str):
    template = env.get_template("verify_email.html")

    html = template.render(
        token=token,
        verify_url=f"{settings.FRONTEND_URL}/verify?token={token}",
        year=datetime.now().year,
        app_name=settings.APP_NAME
    )

    text = f"""
        Verify Your Email.

        Token:
        {token}
    """

    await send_email(
        EmailSchema(
            to=email,
            subject="Verify Your Email",
            html=html,
            text=text,
        )
    )
