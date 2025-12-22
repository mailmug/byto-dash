import uuid
from pydantic import BaseModel
from typing import Optional
from pydantic import Field
from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):
    name: str


class UserCreate(schemas.BaseUserCreate):
    name: str


class UserUpdate(schemas.BaseUserUpdate):
    email: Optional[str] = Field(default=None, exclude=True)
    name: str

class RegisterWithTokenResponse(BaseModel):
    user: UserRead
    token: str

class UserProfile(BaseModel):
    name: Optional[str] = None
    password: Optional[str] = None
