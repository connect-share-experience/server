"""This module implements API endpoints handling event operations.

All functions need for the current user to be the creator of the event.

Functions
---------
update_event(event_id, new_event)
    Update an event information
update_picture(event_id, file)
    Update an event's page picture
delete_event(event_id)
    Delete an event
send_message(event_id, text)
    Send a message to an event's inbox
delete_message(event_id, user_id, datetime)
    Delete a message from an event's inbox
accept_participant(event_id, user_id)
    Accept that a user joins an event
deny_participant(event_id, user_id)
    Refuse that a user joins an event
delete_participant(event_id, user_id)
    Delete a participant from an event
"""
from datetime import datetime as dttime
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlmodel import Session

from app.configs.api_dependencies import get_current_user, get_session
from app.models.enums import MessageCategory, UserEventStatus
from app.models.events import EventRead, EventUpdate
from app.models.messages import Message
from app.models.users import User, UserRead
from app.services.event_services import EventService
from app.services.message_services import MessageService
from app.services.link_user_event_services import UserEventLinkService

router = APIRouter(prefix="/event_creator")


@router.patch(path="/update_event/{event_id}",
              response_model=EventRead,
              response_description="The updated event.",
              summary="Update the data of an event.")
def update_event(*,
                 current_user: User = Depends(get_current_user),
                 session: Session = Depends(get_session),
                 event_id: int,
                 new_event: EventUpdate):
    """
    Update an event's information.

    - **token**: usual authentication token.
    - **event_id**: the id of the event to update.
    - **new_event**: the new event information.
    """
    if UserEventLinkService(session).is_creator(current_user.id, event_id):
        return EventService(session).update_event(event_id, new_event)
    raise HTTPException(status_code=401,
                        detail="Only creator of the event is authorized.")


@router.patch(path="/event_picture/{event_id}",
              response_model=EventRead,
              response_description="The updated event with picture.",
              summary="Update an event's page picture")
def update_picture(*,
                   current_user: User = Depends(get_current_user),
                   session: Session = Depends(get_session),
                   event_id: int,
                   file: UploadFile):
    """
    Update an event page picture.

    - **token**: usual authentication token.
    - **event_id**: the id of the event which needs its picture updated.
    - **file**: the picture to add to the event.
    """
    if UserEventLinkService(session).is_creator(current_user.id, event_id):
        return EventService(session).update_picture(event_id, file)
    raise HTTPException(status_code=401,
                        detail="Only creator of the event is authorized.")


@router.delete(path="/delete_event/{event_id}",
               response_model=EventRead,
               response_description="The deleted event.",
               summary="Delete an event altogether.")
def delete_event(*,
                 current_user: User = Depends(get_current_user),
                 session: Session = Depends(get_session),
                 event_id: int):
    """
    Delete an event altogether.

    - **token**: usual authentication token.
    - **event_id**: the id of the event to delete.
    """
    if UserEventLinkService(session).is_creator(current_user.id, event_id):
        return EventService(session).delete_event(event_id)
    raise HTTPException(status_code=401,
                        detail="Only creator of the event is authorized.")


@router.post(path="/send_message/{event_id}",
             response_model=Message,
             response_description="The created organization message.",
             summary="Send a message to the event inbox.")
def send_message(*,
                 current_user: User = Depends(get_current_user),
                 session: Session = Depends(get_session),
                 event_id: int,
                 text: str):
    """
    Send an organisation message in the event inbox.

    - **token**: usual authentication token.
    - **event_id**: the id of the event to send the message in.
    - **text**: the content of the message
    """
    if UserEventLinkService(session).is_creator(current_user.id, event_id):
        message = Message(event_id=event_id,
                          user_id=current_user.id,
                          category=MessageCategory.ORGA,
                          text=text)
        return MessageService(session).create_message(message)
    raise HTTPException(status_code=401,
                        detail="Only creator of the event is authorized.")


@router.delete(path="/delete_message/{event_id}/{user_id}/{datetime}",
               response_model=Message,
               response_description="The deleted message.",
               summary="Delete a message.")
def delete_message(*,
                   current_user: User = Depends(get_current_user),
                   session: Session = Depends(get_session),
                   event_id: int,
                   user_id: int,
                   datetime: dttime):
    """
    Delete a message in the event inbox.

    - **token**: usual authentication token.
    - **event_id**: the id of the event the message is in.
    - **user_id**: the id of the user that sent the message
    - **datetime**: the date and time the message was sent.
    """
    if UserEventLinkService(session).is_creator(current_user.id, event_id):
        return MessageService(session).delete_message(event_id,
                                                      user_id,
                                                      datetime)
    raise HTTPException(status_code=401,
                        detail="Only creator of the event is authorized.")


@router.patch(path="/accept_participant/{event_id}/{user_id}",
              response_model=UserRead,
              response_description="The accepted user.",
              summary="Accept a user in an event.")
def accept_participant(*,
                       current_user: User = Depends(get_current_user),
                       session: Session = Depends(get_session),
                       event_id: int,
                       user_id: int):
    """
    Accept that a user participates in an event. They must've asked to join.

    - **token**: the usual authentication token
    - **event_id**: the id of the event in which to add the user
    - **user_id**: the id of the user to add to the event
    """
    if UserEventLinkService(session).is_creator(current_user.id, event_id):
        link = UserEventLinkService(session).read_user_event_link(user_id,
                                                                  event_id)
        if link.status == UserEventStatus.PENDING:
            return UserEventLinkService(session).update_status(
                event_id,
                user_id,
                UserEventStatus.ATTENDS)
        raise HTTPException(
            status_code=401,
            detail="Cannot accept a user that didn't ask to join.")
    raise HTTPException(status_code=401,
                        detail="Only creator of the event is authorized.")


@router.patch(path="/reject_participant/{event_id}/{user_id}",
              response_model=UserRead,
              response_description="The denied user.",
              summary="Deny a user the right to participate in the event.")
def deny_participant(*,
                     current_user: User = Depends(get_current_user),
                     session: Session = Depends(get_session),
                     event_id: int,
                     user_id: int):
    """
    Deny a user the right to participate in an event.
    The user must have asked to join the event.

    - **token**: usual authentication token.
    - **event_id**: the id of the event to deny access to
    - **user_id**: the user to deny participation to

    """
    if UserEventLinkService(session).is_creator(current_user.id, event_id):
        link = UserEventLinkService(session).read_user_event_link(user_id,
                                                                  event_id)
        if link.status == UserEventStatus.PENDING:
            return UserEventLinkService(session).update_status(
                event_id,
                user_id,
                UserEventStatus.DENIED)
        raise HTTPException(
            status_code=401,
            detail="Cannot deny a user that didn't ask to join.")
    raise HTTPException(status_code=401,
                        detail="Only creator of the event is authorized.")


@router.delete(path="/delete_participant/{event_id}/{user_id}",
               response_model=UserRead,
               response_description="The deleted participant.",
               summary="Delete a participant from the event.")
def delete_participant(*,
                       current_user: User = Depends(get_current_user),
                       session: Session = Depends(get_session),
                       event_id: int,
                       user_id: int):
    """
    Delete a participant from an event. The user must be a participant.

    - **token**: usual authentication token.
    - **event_id**: the id of the event in which to delete the participant.
    - **user_id**: the id of the user to delete from the event.
    """
    if UserEventLinkService(session).is_creator(current_user.id, event_id):
        link = UserEventLinkService(session).read_user_event_link(user_id,
                                                                  event_id)
        if link.status == UserEventStatus.ATTENDS:
            return UserEventLinkService(session).update_status(
                event_id,
                user_id,
                UserEventStatus.DELETED)
        raise HTTPException(
            status_code=401,
            detail="Cannot delete a user that wasn't a participant yet.")
    raise HTTPException(status_code=401,
                        detail="Only creator of the event is authorized.")
