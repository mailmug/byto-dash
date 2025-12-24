from sqlalchemy import Column, String, ForeignKey, Text, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.models.base import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

class Device(Base):
    __tablename__ = "devices"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    title = Column(String(200), nullable=False)
    type = Column(String(200), nullable=False)
    status = Column(String(50), nullable=False, default="offline")
    is_on = Column(Boolean, nullable=False, default=False)
    last_active = Column(DateTime, nullable=True)
    description = Column(Text, nullable=True)

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    user = relationship("User", back_populates="devices")
