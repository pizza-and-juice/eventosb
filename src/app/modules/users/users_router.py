
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Path, Body
from typing import Annotated, List
from uuid import UUID

from src.app.db.db import get_db 
from src.app.modules.auth.guards import require_roles

from src.app.modules.users.user_role_enum import RoleEnum

from . import users_service as user_svc
from .users_model import User
from .user_reponses import  UserResponse
from .user_dto import UpdateUserDto


router = APIRouter(prefix="/users", tags=["user"])

# design
# POST 

@router.get("/list", response_model=List[UserResponse])
async def read_root(
    user: User = Depends(require_roles(RoleEnum.ADMIN, RoleEnum.SUPER_ADMIN)),
    db: AsyncSession = Depends(get_db)
):
    users = await user_svc.list_users(db)
    return users

# # read self
# @router.get("/retrieve/me", response_model=UserResponse)
# async def read_self(
#     user: User = Depends(get_current_user),
#     db: AsyncSession = Depends(get_db)
# ):
#     user = await get_user_by_id(db, user.id)
#     return user

# user_id is uuid 
@router.get("/retrieve/{user_id}", response_model=UserResponse)
async def read_user(
    user_id: Annotated[UUID, Path(title="User ID", description="UUID of the user")],
    db: AsyncSession = Depends(get_db)
):
    user = await user_svc.retrieve_by_id(db, user_id)
    return user


# check if username is available
# @router.get("/check-username/{username}", response_model=UsernameAvailableResponse)
# async def check_username(
#     username: str,
#     db: AsyncSession = Depends(get_db)
# ):
#     return await check_if_user_exists(db, username)


# @router.put("/{user_id}")
# async def update(
#     user_id: Annotated[UUID, Path(title="User ID", description="UUID of the user")],
#     dto: Annotated[UpdateUserDto, Body(title="Update User DTO")],
#     db: AsyncSession = Depends(get_db),
#     user: User = Depends( get_current_user )
# ):
#     ensure_same_user(user_id, user)
#     return await update_user(user_id, dto, db)
    



