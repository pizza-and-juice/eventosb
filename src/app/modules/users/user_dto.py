from pydantic import BaseModel

class UpdateUserDto(BaseModel):
    username: str
