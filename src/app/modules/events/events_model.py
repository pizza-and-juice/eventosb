import uuid

from sqlalchemy import Column, String, DateTime, func,  Integer, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.app.db.base import Base

from .event_status_enum import EventStatusEnum

class Event(Base):
    __tablename__ = "events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String, index=True, nullable=False)
    subtitle = Column(String, nullable=False)
    description = Column(String, nullable=False)
    image = Column(String, nullable=False)

    country = Column(String, nullable=False)
    city = Column(String, nullable=False)
    address = Column(String, nullable=False)
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)

    website = Column(String, nullable=True)

    attendees_capacity = Column(Integer, nullable=False)
    status = Column(Enum(EventStatusEnum), nullable=False, default=EventStatusEnum.INCOMING)

    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    attendees = relationship(
        "EventAttendee",
        back_populates="event",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
