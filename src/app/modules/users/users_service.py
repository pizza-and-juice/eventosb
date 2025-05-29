from uuid import UUID

from fastapi import HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.app.modules.users.users_model import User

from .user_reponses import UsernameAvailableResponse, UserResponse
from .user_dto import UpdateUserDto


async def list_users(db: AsyncSession):
    all_users = await db.execute(select(User))
    all_users = all_users.scalars().all()

    return [UserResponse(
        id=u.id,
        name=f"{u.first_name} {u.last_name}",
        email=u.email,
        pfp=u.pfp,
        role=u.role,
        created_at=u.created_at,
    ) for u in all_users]

async def retrieve_by_id(db: AsyncSession, user_id: str):
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return UserResponse(
        id=user.id,
        name=f"{user.first_name} {user.last_name}",
        email=user.email,
        pfp=user.pfp,
        role=user.role,
        created_at=user.created_at,
    )

async def check_if_user_exists(db: AsyncSession, username: str):
    result = await db.execute(select(User).where((User.username == username)))
    user = result.scalars().first()

    if user:
        return UsernameAvailableResponse(available=False)

    return UsernameAvailableResponse(available=True)

async def update_user(user_id: UUID, dto: UpdateUserDto, db: AsyncSession): 
    
    res = await check_if_user_exists(db, dto.username)

    if not res.available:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already taken")
    
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    user.username = dto.username

    await db.commit()
    await db.refresh(user)
    return user





