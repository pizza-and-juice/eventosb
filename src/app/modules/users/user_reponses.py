from uuid import UUID
from pydantic import BaseModel
from datetime import datetime

from .user_role_enum import RoleEnum

class UserResponse(BaseModel):
    id: UUID
    name: str
    email: str
    pfp: str
    role: RoleEnum
    created_at: datetime

    class Config:
        from_attributes = True 

class UsernameAvailableResponse(BaseModel):
    available: bool