from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class PostCreate(BaseModel):
    title: str
    content: Optional[str] = None

class PostRead(PostCreate):
    id: UUID
    user_id: UUID
