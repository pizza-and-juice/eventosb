import random
from uuid import UUID

from fastapi import HTTPException, status, UploadFile

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError  
from sqlalchemy.orm import joinedload
from sqlalchemy import func
from sqlalchemy.orm import selectinload

from .events_model import Event
from .event_attendees_model import EventAttendee
from src.app.modules.users.users_model import User

from .events_dto import CreateEventDto
from .event_role_enum import EventRoleEnum



from src.app.modules.common.metadata_schema import PaginationMetadata
from .events_responses import (
    ListEvenstResponse,
    EventDetailResponse,
    EventBaseResponse,
    CreateEventResponse,
    DeleteEventResponse,
    AttendeeHost,
    AttendeeDetail
)

async def list_events(db: AsyncSession) -> ListEvenstResponse:
    """
    List all events.
    """

    result = await db.execute(select(Event).order_by(Event.created_at.desc()))

    events = result.scalars().all()

    if not events:
        return ListEvenstResponse(
            events=[], 
            metadata=PaginationMetadata(
                items_per_page=0,
                total_items=0,
                current_page=1,
                total_pages=1
            )
        )        
    
    event_ids = [e.id for e in events]

    # Count attendees/speakers grouped by (event_id, role)
    counts_result = await db.execute(
        select(
            EventAttendee.event_id,
            EventAttendee.event_role,
            func.count().label("count")
        ).where(
            EventAttendee.event_id.in_(event_ids),
            EventAttendee.event_role.in_([EventRoleEnum.ATTENDEE, EventRoleEnum.SPEAKER])
        ).group_by(EventAttendee.event_id, EventAttendee.event_role)
    )

    counts_map = {}
    for event_id, role, count in counts_result.all():
        if event_id not in counts_map:
            counts_map[event_id] = {EventRoleEnum.ATTENDEE: 0, EventRoleEnum.SPEAKER: 0}
        counts_map[event_id][role] = count

    return ListEvenstResponse(
        events=[EventBaseResponse(
            id=e.id,
            title=e.title,
            subtitle=e.subtitle,
            image=e.image,
            country=e.country,
            city=e.city,
            address=e.address,
            start_date=e.start_date,
            end_date=e.end_date,
            website=e.website,
            attendees_capacity=e.attendees_capacity,
            attendees=counts_map.get(e.id, {}).get(EventRoleEnum.ATTENDEE, 0),
            speakers=counts_map.get(e.id, {}).get(EventRoleEnum.SPEAKER, 0),
            created_at=e.created_at,
            status=e.status
        ) for e in events],
        metadata=PaginationMetadata(
            items_per_page=len(events),
            total_items=len(events),
            current_page=1,
            total_pages=1
        )
    )

async def retrieve_by_id(event_id: UUID, db: AsyncSession) -> EventDetailResponse:
    """
    Retrieve an event by its ID.
    """
    result = await db.execute(
        select(Event)
        .options(
            selectinload(Event.attendees)
            .selectinload(EventAttendee.user),
        )
        .where(Event.id == event_id)
    )
    event = result.scalar_one_or_none()

    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "Event not found",
                "code": '404__EVENT__NOT_FOUND',
            }
        )
    
    result2 = await db.execute(
        select(EventAttendee)
        .options(joinedload(EventAttendee.user))
        .where(
            EventAttendee.event_id == event.id,
            EventAttendee.event_role == EventRoleEnum.ORGANIZER
        )
    )
    host = result2.scalar_one_or_none()

    if not host:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "Event host not found",
                "code": '404__EVENT__HOST__NOT_FOUND',
            }
        )
    

    counts_result = await db.execute(
        select(
            EventAttendee.event_role,
            func.count().label("count")
        ).where(
            EventAttendee.event_id == event.id,
            EventAttendee.event_role.in_([EventRoleEnum.ATTENDEE, EventRoleEnum.SPEAKER])
        ).group_by(EventAttendee.event_role)
    )

    counts = dict(counts_result.all())
    attendees_count = counts.get(EventRoleEnum.ATTENDEE, 0)
    speakers_count = counts.get(EventRoleEnum.SPEAKER, 0)

    return EventDetailResponse(
        id=event.id,
        title=event.title,
        subtitle=event.subtitle,
        description=event.description,
        image=event.image,
        country=event.country,
        city=event.city,
        address=event.address,
        start_date=event.start_date,
        end_date=event.end_date,
        website=event.website,
        attendees_capacity=event.attendees_capacity,
        attendees_list=[
            AttendeeDetail(
                id=a.user.id,
                email= a.user.email,
                name=f"{a.user.first_name} {a.user.last_name}",
                pfp=a.user.pfp,
                attendee_role= a.event_role
            ) for a in event.attendees
        ],
        attendees=attendees_count,
        speakers= speakers_count,
        host= AttendeeHost(
            id=host.user.id,
            name=f"{host.user.first_name} {host.user.last_name}",
            email=host.user.email,
            pfp=host.user.pfp,
        ),
        status=event.status,
        created_at=event.created_at
    )

async def create_event(dto: CreateEventDto, image: UploadFile, user: User, db: AsyncSession) -> CreateEventResponse:
    """
    Create a new event.
    """

    random_image_id = random.randint(1, 1000)

    new_event = Event(
        title=dto.title,
        subtitle=dto.subtitle,
        description=dto.description,
        image=f"https://picsum.photos/id/{random_image_id}/200",  # Placeholder for image URL
        country=dto.country,
        city=dto.city,
        address=dto.address,
        start_date=dto.start_date,
        end_date=dto.end_date,
        website=dto.website,
        attendees_capacity=dto.attendees_capacity
    )

    host = EventAttendee(
        user_id=user.id,
        event=new_event,
        event_role=EventRoleEnum.ORGANIZER,
    )


    try:
        db.add(new_event)
        db.add(host)
        await db.flush()  # Flush to ensure the new event is saved before refreshing
        await db.refresh(new_event)

        # commit 
        await db.commit()

        return CreateEventResponse(id=new_event.id)

    except SQLAlchemyError as e:
        await db.rollback()  # <-- muy importante
        print(f"Error creating event: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create event."
        )

async def delete(event_id: UUID, user: User, db: AsyncSession) -> DeleteEventResponse:
    """
    Delete an event and all related attendees.
    """
    # 1. Buscar el evento
    result = await db.execute(select(Event).where(Event.id == event_id))
    event = result.scalar_one_or_none()

    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "Event not found",
                "code": '404__EVENT__NOT_FOUND',
            }
        )

    # 2. (Opcional) Validar permisos: solo el organizador o admins pueden eliminar
    result_host = await db.execute(
        select(EventAttendee)
        .where(
            EventAttendee.event_id == event_id,
            EventAttendee.event_role == EventRoleEnum.ORGANIZER,
            EventAttendee.user_id == user.id
        )
    )
    host_entry = result_host.scalar_one_or_none()

    if not host_entry and user.role.value not in {"ADMIN", "SUPER_ADMIN"}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "message": "You do not have permission to delete this event.",
                "code": '403__EVENT__DELETE__FORBIDDEN',
            }
        )

    try:
        await db.delete(event)
        await db.commit()
        return DeleteEventResponse(message="Event deleted successfully.", id=event_id)
    except SQLAlchemyError as e:
        await db.rollback()
        print(f"Error deleting event: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to delete event."
        )