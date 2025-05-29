from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from src.app.db.base import Base

from src.app.modules.auth.auth_router import router as auth_router
from src.app.modules.users.users_router import router as user_router
from src.app.modules.events.events_router import router as events_router
# from modules.boards.board_router import router as board_router
# from modules.tiles.tiles_router import router as tile_router
# from modules.files.files_router import r.
# uter as file_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(events_router)
# app.include_router(board_router)
# app.include_router(tile_router)
# app.include_router(file_router)

# create tables
# async def init_models():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


