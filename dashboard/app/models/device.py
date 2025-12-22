from sqlalchemy import Column, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.models.base import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID

class Device(Base):
    __tablename__ = "devices"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(200), nullable=False)
    type = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="devices")
