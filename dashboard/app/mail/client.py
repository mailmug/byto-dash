import aiosmtplib
from app.core.config import settings


async def send_message(message):
    await aiosmtplib.send(
        message,
        hostname=settings.MAIL_HOST,
        port=settings.MAIL_PORT,
        username=settings.MAIL_USERNAME,
        password=settings.MAIL_PASSWORD,
        start_tls=None,
        use_tls=None,
        timeout=10,
    )
