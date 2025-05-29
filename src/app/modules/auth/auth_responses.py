from pydantic import BaseModel
from uuid import UUID

class UserResponse(BaseModel):
    id: UUID
    name: str # Full name 
    email: str
    role: str  # enum, e.g., "user", "admin"
    pfp: str  # URL or path to profile picture
    created_at: str  # ISO format datetime string

class TokenResponse(BaseModel):
    access_token: str
    expires_at: str  # ISO format datetime string

class RegisterResponse(BaseModel):
    user: UserResponse
    token: TokenResponse
    

class LoginResponse(BaseModel):
    user: UserResponse
    token: TokenResponse

class SessionResponse(BaseModel):
    user: UserResponse
    