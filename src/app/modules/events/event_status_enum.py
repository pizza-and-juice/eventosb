from enum import Enum, auto

class EventStatusEnum(Enum):
    INCOMING = "INCOMING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"