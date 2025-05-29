from typing import Callable, Union, Optional

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.app.db.db import get_db
from src.app.core.security import decode_access_token


from src.app.modules.users.users_model import User
from src.app.modules.users.user_role_enum import RoleEnum


class OptionalOAuth2Bearer(OAuth2PasswordBearer):
    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.headers.get("Authorization")
        if not authorization:
            return None
        return await super().__call__(request)

oauth2_optional_scheme = OptionalOAuth2Bearer(tokenUrl="/auth/swagger-login")    

async def get_request_user(
    token: Optional[str] = Depends(oauth2_optional_scheme),
    db: AsyncSession = Depends(get_db)
) -> User | None:
    """
    Retrieves the current user based on the provided access token.
    If the token is invalid or the user does not exist, returns None.
    """

    if token is None:
        return None

    payload = decode_access_token(token)

    # if token is invalid
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user_id = payload["sub"]

    try:
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="user not found while validating token"
            )

        return user

    except Exception as e:
        # 🔥 rollback si algo sale mal con la base de datos
        if db.in_transaction():
            await db.rollback()
        raise e



def require_roles(*allowed_roles: Union[str, RoleEnum]) -> Callable:
    # Convertimos todos los valores a string si vienen como Enum
    required_roles = set(
        role.value if isinstance(role, RoleEnum) else role
        for role in allowed_roles
    )


    def role_checker(user: User = Depends(get_request_user)) -> User:

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "message": "User not authenticated",
                    "code": "401__UNAUTHORIZED"
                }
            )
        

        if user.role.value not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "message": "User does not have the required role",
                    "code": "403__ACCESS_DENIED"
                }
            )
        return user
    return role_checker

