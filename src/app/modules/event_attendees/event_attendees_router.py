from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.app.db.db import get_db
from src.app.modules.auth.guards import require_roles
from src.app.modules.users.user_role_enum import RoleEnum

from src.app.modules.users.users_model import User

from .event_attendees_responses import (ListAttendingEventsResponse, ListCreatedEventsResponse)


from . import event_attendees_service as event_attendees_svc

router = APIRouter(prefix="/user-events", tags=["user-events"])

@router.get("/attending", response_model=ListAttendingEventsResponse)
async def list_attending_events(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_roles(RoleEnum.USER, RoleEnum.ADMIN, RoleEnum.SUPER_ADMIN))
):
    res = await event_attendees_svc.list_attending_events(db, user)
    return res

@router.get("/attending/ids", response_model=List[str])
async def list_attending_event_ids(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_roles(RoleEnum.USER, RoleEnum.ADMIN, RoleEnum.SUPER_ADMIN))
):
    res = await event_attendees_svc.list_attending_ids(db, user)
    return res

@router.get("/created", response_model=ListCreatedEventsResponse)
async def list_created_events(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_roles(RoleEnum.USER, RoleEnum.ADMIN, RoleEnum.SUPER_ADMIN))
):
    res = await event_attendees_svc.list_created_events(db, user)
    return res
