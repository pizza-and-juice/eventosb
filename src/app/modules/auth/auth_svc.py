from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status

from src.app.core.security import hash_password, create_access_token, verify_password

from src.app.modules.users.users_model import User


from .auth_dto import RegisterDto, LoginDto
from .auth_responses import RegisterResponse, LoginResponse, TokenResponse, UserResponse, SessionResponse
from ..users.users_model import User


async def create_user(dto: RegisterDto, db: AsyncSession):

    # check if user already exis
    query = select(User).where((User.email == dto.email))
    result = await db.execute(query)
    user = result.scalars().one_or_none()

    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "message": "User with this email already exists",
                "code": "409__AUTH__USER_EXISTS"
            }
        )
    
    # add verification to prevent abuse
    # await send_verification_email(conf, dto.email, '123456')
 
    #hash password
    hashed_password = hash_password(dto.password)

    new_user = User(
        email=dto.email,
        password=hashed_password,
        first_name=dto.first_name,
        last_name=dto.last_name,
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    # create session
    token = create_access_token({"sub": str(new_user.id)})

    return RegisterResponse(
        user=UserResponse(
            id=new_user.id,
            email=new_user.email,
            name=f"{new_user.first_name} {new_user.last_name}",
            role=new_user.role,
            pfp=new_user.pfp,
            created_at=new_user.created_at.isoformat()
        ),
        token=TokenResponse(
            access_token=token,
            expires_at=""  # Example expiration date, should be dynamic
        )
    )

async def login_user(dto: LoginDto, db: AsyncSession):
    query = select(User).where(User.email == dto.email)
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if not user or not verify_password(dto.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={
            "message": "Invalid email or password",
            "code": "401__AUTH__INVALID_CREDENTIALS"
        })

    token = create_access_token({"sub": str(user.id)})

    return LoginResponse(
        user=UserResponse(
            id=user.id,
            email=user.email,
            name=f"{user.first_name} {user.last_name}",
            role=user.role,
            pfp=user.pfp,
            created_at=user.created_at.isoformat()
        ),
        token=TokenResponse(
            access_token=token,
            expires_at=""  # Example expiration date, should be dynamic
        )
    )

async def session(user: User | None):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail={
                "message": "unauthorized",
                "code": "401__UNAUTHORIZED"
            }
        )
    
    return SessionResponse(
        user=UserResponse(
            id=user.id,
            name=f"{user.first_name} {user.last_name}",
            email=user.email,
            role=user.role,
            pfp=user.pfp,
            created_at=user.created_at.isoformat(),
        )
    )