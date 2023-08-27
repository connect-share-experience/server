"""This module contains functions used for pictures through the app.

Functions
---------
create_picture_name(picture)
    Create a random identifier name for picture files to be saved under.
"""
from uuid import uuid4

from fastapi import HTTPException, UploadFile

ALLOWED_EXTENSIONS = ["png", "jpg", 'jpeg', 'JPG']


def create_picture_name(picture: UploadFile) -> str:
    """Create a random identifier name for picture files to be saved under.

    Parameters
    ----------
    picture : UploadFile
        The picture whose name to create.

    Returns
    -------
    str
        The created name.

    Raises
    ------
    HTTPException(422)
        Raised when the picture does not contain a string filename.
    HTTPException(415)
        Raised when the picture does not have an allowed extension.
    """
    if picture.filename is None:
        raise HTTPException(status_code=422,
                            detail="Cannot process image without extension.")
    extension = picture.filename.split(".")[1]
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=415,
                            detail=f"File type .{extension} not allowed.")

    token_name = uuid4().hex + "." + extension
    return token_name
