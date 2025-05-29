from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Path, Form, File, UploadFile, HTTPException, status
from typing import Annotated, List
from uuid import UUID

from src.app.db.db import get_db 
from src.app.modules.auth.guards import require_roles

from src.app.modules.users.users_model import User

from src.app.modules.users.user_role_enum import RoleEnum

from .events_dto import CreateEventDto

from . import events_service as events_svc
from .events_model import Event

from .events_responses import ListEvenstResponse, EventDetailResponse, CreateEventResponse, DeleteEventResponse




router = APIRouter(prefix="/events", tags=["events"])

# design
# POST 

@router.get("/list", response_model=ListEvenstResponse)
async def read_root(
    # user: User = Depends(require_roles(RoleEnum.ADMIN, RoleEnum.SUPER_ADMIN)),
    db: AsyncSession = Depends(get_db)
):
    res = await events_svc.list_events(db)
    return res


@router.get("/retrieve/{event_id}", response_model=EventDetailResponse)
async def read_user(
    # user_id: Annotated[UUID, Path(title="User ID", description="UUID of the user")],
    event_id: Annotated[UUID, Path(title="Event ID", description="UUID of the event")],
    user: User = Depends(require_roles(RoleEnum.USER, RoleEnum.ADMIN, RoleEnum.SUPER_ADMIN)),
    db: AsyncSession = Depends(get_db)
):
    res = await events_svc.retrieve_by_id(event_id, db)
    return res

@router.post("/create", response_model=CreateEventResponse)
async def create_event(
    title: Annotated[str, Form(title="Event Title", description="Title of the event")],
    subtitle: Annotated[str, Form(title="Event Subtitle", description="Subtitle of the event")],
    description: Annotated[str, Form(title="Event Description", description="Description of the event")],
    image: Annotated[UploadFile, File(description="Image file for the event")],
    
    country: Annotated[str, Form(title="Country", description="Country where the event is held")],
    city: Annotated[str, Form(title="City", description="City where the event is held")],
    address: Annotated[str, Form(title="Address", description="Address of the event location")],
    start_date: Annotated[str, Form(title="Start Date", description="Start date of the event in ISO format")],
    end_date: Annotated[str, Form(title="End Date", description="End date of the event in ISO format")],
    attendees_capacity: Annotated[int, Form(title="Attendees Capacity", description="Maximum number of attendees for the event")],
    
    website: Annotated[Optional[str], Form(title="Website", description="Website of the event")] = None,
    
    user: User = Depends(require_roles(RoleEnum.USER, RoleEnum.ADMIN, RoleEnum.SUPER_ADMIN)),
    db: AsyncSession = Depends(get_db)
):
    try:
        dto = CreateEventDto(
            title=title,
            subtitle=subtitle,
            description=description,

            country=country,
            city=city,
            address=address,
            start_date=start_date,
            end_date=end_date,

            website=website,
            attendees_capacity=attendees_capacity,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    
    res = await events_svc.create_event(
        dto=dto,
        image=image,
        user=user,
        db=db
    )
    return res


@router.delete("/delete/{event_id}", response_model=DeleteEventResponse)
async def delete_event(
    event_id: Annotated[UUID, Path(title="Event ID", description="UUID of the event")],
    user: User = Depends(require_roles(RoleEnum.USER, RoleEnum.ADMIN, RoleEnum.SUPER_ADMIN)),
    db: AsyncSession = Depends(get_db)
):
    res = await events_svc.delete(event_id, user, db)
    return res