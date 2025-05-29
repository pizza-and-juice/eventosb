import uuid

from services.db import Base
from sqlalchemy import Column, String, DateTime, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Enum

from enums.enums import RoleEnum

class Board(Base):
    __tablename__ = "boards"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, index=True, nullable=False, unique=True)
    topic = Column(String, nullable=False)
    creator_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
