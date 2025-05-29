# src/app/db/init_db.py

import asyncio
from src.app.db.db import AsyncSessionLocal 

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.app.core.security import hash_password  # si usas hashing

from src.app.modules.users.users_model import User
from src.app.modules.users.user_role_enum import RoleEnum

async def init_db(session: AsyncSession):
    # Verificar si ya existe un admin
    result = await session.execute(select(User).where(User.email == "admin@example.com"))
    if result.scalar_one_or_none():
        return

    user = User(
        email="admin@example.com",
        password=hash_password("secret"),
        first_name="Admin",
        last_name="User",
        role=RoleEnum.ADMIN,
        pfp="",
    )

    session.add(user)
    await session.commit()

async def main():
    async with AsyncSessionLocal() as session:
        await init_db(session)

if __name__ == "__main__":
    asyncio.run(main())