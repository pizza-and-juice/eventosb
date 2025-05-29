from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services.db import get_db
from services.auth import get_current_user

from guards.admin_guard import admin_required

from modules.users.users_model import User

from .board_responses import BoardResponse
from .board_dto import CreateBoardDto
from .board_svc import get_all_boards, get_board_by_id, create_board


router = APIRouter(prefix="/boards", tags=["boards"])

@router.get("", response_model=List[BoardResponse])
async def read_root(
    user: User = Depends(admin_required), 
    db: AsyncSession = Depends(get_db)
):
    return await get_all_boards(db)

@router.get("/{board_id}", response_model=BoardResponse)
async def read_board(board_id: str, db: AsyncSession = Depends(get_db)):
    return await get_board_by_id(board_id, db)

@router.post("", response_model=BoardResponse)
async def post_board(dto: CreateBoardDto, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await create_board(dto, user.id, db)

