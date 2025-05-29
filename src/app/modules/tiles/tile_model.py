from sqlalchemy import Column, String, Text, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from services.db import Base
import uuid

class Tile(Base):
    __tablename__ = "tiles"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    image_url = Column(String, nullable=False)
    position = Column(String, nullable=False) # phi and theta combined as a string f"{phi},{theta}"
    board_id = Column(UUID(as_uuid=True), ForeignKey("boards.id"), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
