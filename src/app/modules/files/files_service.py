import os

from fastapi import HTTPException, status

def get_file_content(storage_dir: str):

    # Check if file exists
    if not os.path.isfile(storage_dir):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
        )

    # Read and return the image
    with open(storage_dir, "rb") as file:
        return file.read()
    