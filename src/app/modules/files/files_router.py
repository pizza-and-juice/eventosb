import os
from typing import Annotated
from urllib.parse import unquote
from uuid import UUID
from pathlib import Path
from fastapi import APIRouter, Path as PathParam, Response

from . import files_service

router = APIRouter(prefix="/files/{board_id}", tags=["files"])

# serve files
@router.get("/{filename}")
def read_file(
    board_id: Annotated[UUID, PathParam( title="the board id", description="The id of the board")],
    filename: Annotated[str, PathParam( title="the name of the image", description="The name of the file to serve")],
):
    """ Serves the file content. """
    # decode url semicolon ,
    name = unquote(filename)

    curr_dir = Path(__file__).resolve().parent.parent.parent
    all_path = os.path.join(curr_dir, "assets", str(board_id), name)
    # _path = os.path.join(curr_dir, "assets", str(dto.board_id))

    content = files_service.get_file_content(all_path)
    return Response(content, media_type="image/png")
    