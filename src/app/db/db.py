import os
import ssl
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .base import Base

from src.app.core.config import settings


DATABASE_URL = settings.DATABASE_URL


ssl_context = ssl.create_default_context(cafile=settings.CA_CERT_PATH)

# Create async engine
engine = create_async_engine(
    DATABASE_URL, 
    connect_args={"ssl": ssl_context},
    echo=True
)

# Create async session maker
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)

# Base class for models


# Dependency for getting DB session
async def get_db():
    async with AsyncSessionLocal() as session:
        try: 
            yield session
        finally: 
            await session.close()
