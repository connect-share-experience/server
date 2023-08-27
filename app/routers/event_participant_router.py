"""This module implements API endpoints handling event operations.

They all use the currently authenticated user. The user must (WIP) be a
participant in the event in order to use those endpoints.

Functions
---------
send_picture(event_id, picture)
    Send a picture to the event.
"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlmodel import Session

from app.configs.api_dependencies import get_current_user, get_session
from app.models.messages import Message
from app.models.users import User, UserRead
from app.services.message_services import MessageService
from app.services.link_user_event_services import UserEventLinkService

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

    - **token**: usual authentication token.
    - **event_id**: the id of the event in which to send a picture.
    - **file**: the picture to send.
    """
    # TODO gotta check that the user is either participant or creator of event
    if (UserEventLinkService(session)
            .is_participant(current_user.id, event_id)) is False:
        raise HTTPException(
            status_code=401,
            detail=f"Current user isn't allowed in event {event_id}")
    return MessageService(session).create_picture_message(current_user.id,
                                                          event_id,
                                                          file)


@router.get(path="/inbox",
            response_model=List[Message],
            response_description="All messages and pictures in the event.",
            summary="Read all messages in event inbox.")
def read_inbox(*,
               current_user: User = Depends(get_current_user),
               session: Session = Depends(get_session),
               event_id: int):
    """
    Read all messages in event inbox. This includes all organization messages,
    participant addition and deletion, and all pictures.

    - **token**: usual authentication token.
    - **event_id**: the id of the event in which messages must be read.
    """
    # TODO gotta check that the user is either participant or creator of event
    if (UserEventLinkService(session)
            .is_participant(current_user.id, event_id)) is False:
        raise HTTPException(
            status_code=401,
            detail=f"Current user isn't allowed in event {event_id}")
    return MessageService(session).read_event_messages(event_id)


@router.get(path="/participants",
            response_model=List[UserRead],
            response_description="All users participating in the event.",
            summary="Read all users taking part in the event.")
def read_participants(*,
                      current_user: User = Depends(get_current_user),
                      session: Session = Depends(get_session),
                      event_id: int):
    """
    Read all users that participate in the event, creator included.

    - **token**: usual authentication token.
    - **event_id**: the id of the event the users take part in.
    """
    if (UserEventLinkService(session)
            .is_participant(current_user.id, event_id)) is False:
        raise HTTPException(
            status_code=401,
            detail=f"Current user isn't allowed in event {event_id}")
    return UserEventLinkService(session).read_participants(event_id)
