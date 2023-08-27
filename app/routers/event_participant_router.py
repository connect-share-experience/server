"""This module implements API endpoints handling event operations.

They all use the currently authenticated user. The user must (WIP) be a
participant in the event in order to use those endpoints.

Functions
---------
send_picture(event_id, picture)
    Send a picture to the event.
"""
from fastapi import APIRouter, Depends, UploadFile
from sqlmodel import Session

from app.configs.api_dependencies import get_current_user, get_session
from app.models.messages import Message
from app.models.users import User
from app.services.message_services import MessageService

router = APIRouter(prefix="/event_participant")


@router.post(path="/send_picture",
             response_model=Message,
             response_description="The created message for picture.",
             summary="Send a picture to the event inbox.")
def send_picture(*,
                 current_user: User = Depends(get_current_user),
                 session: Session = Depends(get_session),
                 event_id: int,
                 file: UploadFile):
    """
    Send a picture in an event.

    - **event_id**: The id in which to send a picture
    - **file**: The picture to send.
    """
    # TODO gotta check that the user is either participant or creator of event
    return MessageService(session).create_picture_message(
        user_id=current_user.id,
        event_id=event_id,
        picture=file
    )
