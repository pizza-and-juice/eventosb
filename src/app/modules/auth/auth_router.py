from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from src.app.db.db import get_db

from src.app.modules.users.users_model import User

from .auth_dto import RegisterDto, LoginDto
from .auth_responses import RegisterResponse, LoginResponse
from .auth_svc import create_user, login_user, session
from .guards import get_request_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=RegisterResponse)
async def register(
    dto: Annotated[RegisterDto, Body(embed=False, title="Register DTO")],
    db: AsyncSession = Depends(get_db),
):
    res = await create_user(dto, db)
    return res

@router.post("/login", response_model=LoginResponse)
async def login(
    dto: Annotated[LoginDto, Body(title="Login DTO", example={"email": "example@gmail.com", "password": "password"})],
    db: AsyncSession = Depends(get_db)
):
    res = await login_user(dto, db)
    return res

@router.get("/session")
async def get_user_session(current_user: User = Depends(get_request_user)):
    res = await session(current_user)
    return res

# just for debugging purposes should be removed in production
@router.post("/swagger-login", response_model=LoginResponse)
async def login2(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    dto = LoginDto(email=form_data.username, password=form_data.password)
    res = await login_user(dto, db)
    return JSONResponse(
        content={
            "access_token": res.token.access_token,
            "token_type": "bearer",
        }
    )   
    