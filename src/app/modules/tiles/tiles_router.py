from fastapi import APIRouter, Depends, HTTPException, status, Form, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List, Annotated

from services.db import get_db

from guards.admin_guard import admin_required

from modules.users.users_model import User

from .tile_response import TileResponse
from .tiles_svc import get_all_tiles, get_tile_by_position, create_tile, update_tile, delete_tile
from .tile_dto import CreateTileDto, UpdateTileDto


router = APIRouter(prefix="/boards/{board_id}/tiles", tags=["Tiles"])

@router.get("", response_model=List[TileResponse])
async def read_root(board_id: UUID, db: AsyncSession = Depends(get_db)):
    return await get_all_tiles(board_id, db)
    

@router.get("/{tile_id}", response_model=TileResponse)
async def read_id(board_id: UUID, position: str, db: AsyncSession = Depends(get_db)):
    return await get_tile_by_position(board_id, position, db)

@router.post("")
async def post(
    board_id: UUID,
    position: str = Form(...),
    image: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    return await create_tile(
        CreateTileDto(
            board_id=board_id,
            position=position,
        ),
        image,
        db
    )

@router.put("/{tile_id}", response_model=TileResponse)
async def update(
    board_id: UUID,
    position: str = Form(...),
    image: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    return await update_tile(
        UpdateTileDto(
            board_id=board_id,
            position=position,
        ),
        image,
        db
    )

@router.delete("/{tile_id}")
async def delete_tile(tile_id: UUID, db: AsyncSession = Depends(get_db), user: User = Depends(admin_required)):
    return await delete_tile(tile_id=tile_id, db=db)
