from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from src.app.db.base import Base

from src.app.modules.auth.auth_router import router as auth_router
from src.app.modules.users.users_router import router as user_router
from src.app.modules.events.events_router import router as events_router
from src.app.modules.event_actions.event_actions_router import router as event_actions_router
from src.app.modules.event_attendees.event_attendees_router import router as event_attendees_router
# from modules.files.files_router import router as file_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(events_router)
app.include_router(event_actions_router)
app.include_router(event_attendees_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ INSEGURO en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# create tables
# async def init_models():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


