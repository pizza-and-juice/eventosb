import uuid

from sqlalchemy import Column, String, DateTime, func, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Enum
from sqlalchemy.orm import relationship

from src.app.db.base import Base

from .event_role_enum import EventRoleEnum

from .event_status_enum import EventStatusEnum

class EventAttendee(Base):
    __tablename__ = "event_attendees"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )
    event_id = Column(
        UUID(as_uuid=True),
        ForeignKey('events.id', ondelete='CASCADE'),
        nullable=False
    )
    event_role = Column(Enum(EventRoleEnum), nullable=False, default=EventRoleEnum.ATTENDEE)

    event = relationship("Event", back_populates="attendees")
    user = relationship("User")

    