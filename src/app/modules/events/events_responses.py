from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime

from .event_status_enum import EventStatusEnum
from .event_role_enum import EventRoleEnum

from src.app.modules.common.metadata_schema import PaginationMetadata


class EventBaseResponse(BaseModel):
    id: UUID
    title: str
    subtitle: str
    image: str

    country: str
    city: str
    address: str
    start_date: datetime
    end_date: datetime

    website: Optional[str] = None

    attendees_capacity: int

    attendees: int
    speakers: int

    status: EventStatusEnum
    created_at: datetime



class AttendeeDetail(BaseModel):
    id: UUID
    name: str
    email: str
    pfp: Optional[str] = None
    attendee_role: EventRoleEnum

class AttendeeHost(BaseModel):
    id: UUID
    name: str
    email: str
    pfp: Optional[str] = None
   

class EventDetailResponse(EventBaseResponse):
    id: UUID
    title: str
    subtitle: str
    description: str
    image: str

    country: str
    city: str
    address: str
    start_date: datetime
    end_date: datetime

    website: Optional[str] = None

    attendees_capacity: int

    attendees_list: List[AttendeeDetail]
    host: AttendeeHost

    status: EventStatusEnum
    created_at: datetime


class ListEvenstResponse(BaseModel):
    events: List[EventBaseResponse]
    metadata: PaginationMetadata


class CreateEventResponse(BaseModel):
    id: UUID

class DeleteEventResponse(BaseModel):
    id: UUID
    message: str
    