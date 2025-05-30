from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.app.db.db import get_db

from src.app.modules.auth.guards import require_roles

from src.app.modules.users.users_model import User
from src.app.modules.events.events_model import Event
from src.app.modules.events.event_attendees_model import EventAttendee

from src.app.modules.users.user_role_enum import RoleEnum
from src.app.modules.events.event_role_enum import EventRoleEnum
from src.app.modules.events.event_status_enum import EventStatusEnum 


router = APIRouter(prefix="/event-actions", tags=["Events Actions"])

@router.post("/{event_id}/register", status_code=status.HTTP_201_CREATED)
async def register_to_event(
    event_id: UUID,
    user: User = Depends(require_roles(RoleEnum.USER, RoleEnum.ADMIN, RoleEnum.SUPER_ADMIN)),
    db: AsyncSession = Depends(get_db),
):
    # Verifica si ya está registrado
    result = await db.execute(
        select(EventAttendee).where(EventAttendee.event_id == event_id, EventAttendee.user_id == user.id)
    )

    # obtiene el evento para verificar capacidad
    event_result = await db.execute(select(Event).where(Event.id == event_id))
    event = event_result.scalar_one_or_none()

    existing = result.scalar_one_or_none()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "You are already registered for this event.",
                "code": "400__ALREADY_REGISTERED"
            }
        )

    attendee = EventAttendee(
        event_id=event_id,
        user_id=user.id,
        event_role=EventRoleEnum.ATTENDEE  # o lo que aplique
    )

    db.add(attendee)
    await db.commit()

    return {"message": "Successfully registered to event."}

@router.post("/{event_id}/register-as-speaker", status_code=status.HTTP_201_CREATED)
async def register_to_event(
    event_id: UUID,
    user: User = Depends(require_roles(RoleEnum.USER, RoleEnum.ADMIN, RoleEnum.SUPER_ADMIN)),
    db: AsyncSession = Depends(get_db),
):
    # Verifica si ya está registrado
    result = await db.execute(
        select(EventAttendee).where(EventAttendee.event_id == event_id, EventAttendee.user_id == user.id)
    )

    existing = result.scalar_one_or_none()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "You are already registered for this event.",
                "code": "400__ALREADY_REGISTERED"
            }
        )

    attendee = EventAttendee(
        event_id=event_id,
        user_id=user.id,
        event_role=EventRoleEnum.SPEAKER  # o lo que aplique
    )

    db.add(attendee)
    await db.commit()

    return {"message": "Successfully registered to event."}

@router.delete("/{event_id}/unregister", status_code=status.HTTP_200_OK)
async def unregister_from_event(
    event_id: UUID,
    user: User = Depends(require_roles(RoleEnum.USER, RoleEnum.ADMIN, RoleEnum.SUPER_ADMIN)),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(EventAttendee).where(EventAttendee.event_id == event_id, EventAttendee.user_id == user.id)
    )
    attendee = result.scalar_one_or_none()
    if not attendee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
            "message": "You are not registered for this event.",
            "code": "404__NOT_REGISTERED"
        })

    await db.delete(attendee)
    await db.commit()
    return {"message": "Successfully unregistered from event."}

@router.post("/{event_id}/complete", status_code=status.HTTP_200_OK)
async def complete_event(
    event_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_roles(RoleEnum.USER, RoleEnum.ADMIN, RoleEnum.SUPER_ADMIN))
):
    # Opcional: verifica que el usuario sea el host
    result = await db.execute(select(Event).where(Event.id == event_id))
    event = result.scalar_one_or_none()

    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
            "message": "Event not found.",
            "code": "404__EVENT__NOT_FOUND"
        })
    
    # Verifica si el usuario es el organizador del evento
    result_host = await db.execute(
        select(EventAttendee)
        .where(
            EventAttendee.event_id == event_id,
            EventAttendee.event_role == EventRoleEnum.ORGANIZER,
            EventAttendee.user_id == user.id
        )
    )

    host = result_host.scalar_one_or_none()

    if not host:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "message": "You do not have permission to complete this event.",
                "code": "403__FORBIDDEN__COMPLETE_EVENT"
            }
        )


    event.status = EventStatusEnum.COMPLETED  # si usas Enum, usa el valor adecuado
    await db.commit()
    return {"message": "Event marked as completed."}