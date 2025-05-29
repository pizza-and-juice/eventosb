from typing import Optional
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class CreateTileDto(BaseModel):
    board_id: UUID
    position: str

class UpdateTileDto(BaseModel):
    board_id: UUID
    position: str

