from typing import Optional

from pydantic import BaseModel, field_validator

from datetime import datetime

class CreateEventDto(BaseModel):
    title: str
    subtitle: str
    description: str

    country: str
    city: str
    address: str
    start_date: str
    end_date: str

    website: Optional[str] = None

    attendees_capacity: int

    @field_validator('start_date', 'end_date')
    def parse_date(cls, value):
        try:
            return datetime.strptime(value, "%m/%d/%Y")
        except ValueError:
            raise ValueError("La fecha debe tener el formato MM/DD/AAAA")