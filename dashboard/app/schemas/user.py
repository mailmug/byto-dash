import uuid
from pydantic import BaseModel

from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):
    name: str


class UserCreate(schemas.BaseUserCreate):
    name: str


class UserUpdate(schemas.BaseUserUpdate):
    name: str

class RegisterWithTokenResponse(BaseModel):
    user: UserRead
    token: str
