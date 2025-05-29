from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class BoardResponse(BaseModel):
    id: UUID
    name: str
    topic: str
    creator_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
    