from datetime import datetime
from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class DeviceCreate(BaseModel):
    title: str
    type: str
    description: Optional[str] = None

class DeviceRead(DeviceCreate):
    is_on: bool
    status: str
    last_active: datetime | None
    id: UUID
    user_id: UUID
