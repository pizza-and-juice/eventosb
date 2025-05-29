from pydantic import BaseModel

class CreateBoardDto(BaseModel):
    name: str
    topic: str
    