from typing import List


from sqlalchemy import select, func
from sqlalchemy.orm import joinedload

from src.app.db.db import  AsyncSession


from src.app.modules.users.user_role_enum import RoleEnum
from src.app.modules.events.event_attendees_model import EventAttendee, EventRoleEnum

from src.app.modules.events.event_role_enum import EventRoleEnum

from src.app.modules.events.events_model import Event
from src.app.modules.users.users_model import User


from src.app.modules.common.metadata_schema import PaginationMetadata
from .event_attendees_responses import (ListAttendingEventsResponse, ListCreatedEventsResponse, EventBaseResponse)

from .event_attendees_responses import ListAttendingEventsResponse

async def list_attending_events(
    db: AsyncSession,
    user_id: str,
) -> ListAttendingEventsResponse:
    
    result = await db.execute(
        select(Event)
        .join(EventAttendee)
        .options(joinedload(Event.attendees))  # optional, preload attendees if needed
        .where(
            EventAttendee.user_id == user_id,
            EventAttendee.event_role.in_([EventRoleEnum.ATTENDEE, EventRoleEnum.SPEAKER])
        )
        .order_by(Event.created_at)
    )


    events = result.unique().scalars().all()

    if len(events) == 0:
        return ListAttendingEventsResponse(
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

    return ListAttendingEventsResponse(
        events=[
            EventBaseResponse(
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
            )
            for e in events
        ],
        metadata=PaginationMetadata(
            items_per_page=len(events),
            total_items=len(events),
            current_page=1,
            total_pages=1
        )
    )

async def list_attending_ids(
    db: AsyncSession,
    event_ids: List[str],
    user: User
) -> List[str]:
    
    if len(event_ids) == 0:
        return []
    
    result = await db.execute(
        select(EventAttendee.event_id)
        .where(
            EventAttendee.user_id == user.id,
            EventAttendee.event_role.in_([EventRoleEnum.ATTENDEE, EventRoleEnum.SPEAKER]),
            EventAttendee.event_id.in_(event_ids)
        )
    )

    events = result.unique().scalars().all()

    # map to ids
    if not events:
        return []
    
    # Convert to string IDs
    event_ids = [str(event_id) for event_id in events]

    return event_ids


async def list_created_events(
    db: AsyncSession,
    user_id: str
) -> ListCreatedEventsResponse:
    
    result = await db.execute(
        select(Event)
        .join(EventAttendee)
        .options(joinedload(Event.attendees))  # si quieres traer los asistentes
        .where(
            EventAttendee.user_id == user_id,
            EventAttendee.event_role == EventRoleEnum.ORGANIZER
        )
        .order_by(Event.created_at.desc())
    )

    events = result.unique().scalars().all()

    print(f"------------------Found {len(events)} created events for user {user_id}")

    if len(events) == 0:
        return ListCreatedEventsResponse(
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

    return ListCreatedEventsResponse(
        events=[
            EventBaseResponse(
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
            )
            for e in events
        ],
        metadata=PaginationMetadata(
            items_per_page=len(events),
            total_items=len(events),
            current_page=1,
            total_pages=1
        )
    )