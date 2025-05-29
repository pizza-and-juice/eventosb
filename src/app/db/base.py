# app/db/base_class.py
from sqlalchemy.orm import declarative_base

Base = declarative_base()

from src.app.modules.users.users_model import User
from src.app.modules.events.events_model import Event
from src.app.modules.events.event_attendees_model import EventAttendee