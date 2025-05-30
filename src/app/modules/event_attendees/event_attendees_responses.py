from typing import List
from pydantic import BaseModel

from src.app.modules.events.events_responses import EventBaseResponse

from src.app.modules.common.metadata_schema import PaginationMetadata

    
class ListAttendingEventsResponse(BaseModel):
    events: List[EventBaseResponse]
    metadata: PaginationMetadata


class ListCreatedEventsResponse(BaseModel):
    events: List[EventBaseResponse]
    metadata: PaginationMetadata