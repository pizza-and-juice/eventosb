from uuid import UUID
from fastapi import HTTPException, status 

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from .board_model import Board
from .board_responses import BoardResponse
from .board_dto import CreateBoardDto

async def get_all_boards(db: AsyncSession):

    query = select(Board)
    result = await db.execute(query)
    boards = result.scalars().all()
    return [BoardResponse.model_validate(b) for b in boards]

async def get_board_by_id(board_id: str, db: AsyncSession ):
    query = select(Board).filter(Board.id == board_id)
    result = await db.execute(query)
    board = result.scalars().first()

    if not board:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Board not found")

    return BoardResponse.model_validate(board)

async def create_board(dto: CreateBoardDto,  creator_id: UUID, db: AsyncSession):

    query = select(Board).where((Board.name == dto.name))
    result = await db.execute(query)
    existing_board = result.scalars().first()

    if existing_board:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Board with this name already exists")

    try:
        new_board = Board(
            name=dto.name,
            topic=dto.topic,
            creator_id=creator_id
        )
        db.add(new_board)
        await db.commit()
        await db.refresh(new_board)

        return BoardResponse.model_validate(new_board)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))