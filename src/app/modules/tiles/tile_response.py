from uuid import UUID
from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class TileResponse(BaseModel):
    id: UUID
    image_url: str
    position: str
    board_id: UUID
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
