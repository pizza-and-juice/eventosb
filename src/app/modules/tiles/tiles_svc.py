import os
from pathlib import Path
from uuid import UUID
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from fastapi import HTTPException, status, UploadFile

from .tile_model import Tile
from .tile_response import TileResponse
from .tile_dto import CreateTileDto, UpdateTileDto

from modules.boards.board_svc import get_board_by_id


async def get_all_tiles(board_id: UUID, db: AsyncSession):

    board = await get_board_by_id(board_id, db)

    result = await db.execute(
        select(Tile).where(Tile.board_id == board.id)
    )
    tiles = result.scalars().all()
    return [TileResponse.model_validate(t) for t in tiles]

async def get_tile_by_id(board_id: UUID, tile_id: UUID, db: AsyncSession):

    result = await db.execute(
        select(Tile).where(Tile.id == tile_id)
    )

    tile = result.scalars().first()

    if not tile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tile not found")
    
    if tile.board_id != board_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Board not found")
    
    return TileResponse.model_validate(tile)

async def get_tile_by_position(board_id: UUID, position: str, db: AsyncSession):

    result = await db.execute(
        select(Tile).where(Tile.position == position)
    )

    tile = result.scalars().first()

    if not tile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tile not found")
    
    if tile.board_id != board_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Board not found")
    
    return TileResponse.model_validate(tile)


# 2MB = 1024 * 1024 bytes
MAX_SIZE = 2 * 1024 * 1024



async def create_tile(dto: CreateTileDto, image: UploadFile, db: AsyncSession):

    # check image size
    if image.size > MAX_SIZE:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File size too large")

    # check if board exists
    board = await get_board_by_id(dto.board_id, db)

    if not board:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Board not found")
    

    # check if tile already exists at position
    tile = await db.execute(
        select(Tile).where(Tile.position == dto.position, Tile.board_id == board.id)
    )

    tile = tile.scalars().first()

    if tile:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tile already exists at this position")
    
    # check if folder for board exists (replace with S3 bucket check)
    curr_dir = Path(__file__).resolve().parent.parent.parent
    _path = os.path.join(curr_dir, "assets", str(dto.board_id))

    if not os.path.exists(_path):
        os.makedirs(_path)

    # save image to folder (replace with S3 bucket upload)
    filename = os.path.join(_path, dto.position +'.png')

    with open(filename, "wb") as f:
        f.write(image.file.read())

    new_tile = Tile(**dto.model_dump(), image_url=f"http://localhost:8000/files/{dto.board_id}/{dto.position}.png")
    db.add(new_tile)
    await db.commit()
    await db.refresh(new_tile)

    return TileResponse(
        id=new_tile.id,
        board_id=new_tile.board_id,
        position=new_tile.position,
        image_url=new_tile.image_url,
        updated_at=new_tile.updated_at
    )
    
    
async def update_tile(dto: UpdateTileDto, image: UploadFile, db: AsyncSession):
    # check image size
    if image.size > MAX_SIZE:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File size too large")

    # check if board exists
    board = await get_board_by_id(dto.board_id, db)

    if not board:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Board not found")
    

    # check if tile  exists at position
    tile = await db.execute(
        select(Tile).where(Tile.position == dto.position, Tile.board_id == board.id)
    )

    tile = tile.scalars().first()

    if not tile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tile not found")
    
    # check if folder for board exists (replace with S3 bucket check)
    curr_dir = Path(__file__).resolve().parent.parent.parent
    _path = os.path.join(curr_dir, "assets", str(dto.board_id))

    if not os.path.exists(_path):
        os.makedirs(_path)

    # save image to folder (replace with S3 bucket upload)
    filename = os.path.join(_path, dto.position +'.png')

    with open(filename, "wb") as f:
        f.write(image.file.read())

    image_url = f"http://localhost:8000/files/{dto.board_id}/{dto.position}.png"

    # update tile attributes
    tile.image_url = image_url
    tile.updated_at = datetime.now()

    await db.commit()
    await db.refresh(tile)

    return TileResponse(
        id=tile.id,
        board_id=tile.board_id,
        position=tile.position,
        image_url=tile.image_url,
        updated_at=tile.updated_at
    )

async def delete_tile(tile_id: UUID, db: AsyncSession):

    tile = await db.get(Tile, tile_id)

    if not tile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tile not found")
    
    await db.delete(tile)
    await db.commit()
    return {"message": "Tile deleted successfully"}