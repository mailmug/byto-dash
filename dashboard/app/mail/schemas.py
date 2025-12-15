from pydantic import BaseModel, EmailStr


class EmailSchema(BaseModel):
    to: EmailStr
    subject: str
    html: str
    text: str | None = None
