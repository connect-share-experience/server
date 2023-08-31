"""This module implements API endpoints handling event operations.

Functions
---------
create_event(event)
    Create an event, with its address.
read_event(event_id)
    Read an event with detailed location.
"""
from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.configs.api_dependencies import get_current_user, get_session
from app.models.events import EventCreate, EventRead
from app.models.addresses import AddressCreate
from app.models.links import UserEventLink
from app.models.reading_models import EventReadFull
from app.models.enums import UserEventStatus
from app.models.users import User
from app.services.event_services import EventService
from app.services.link_user_event_services import UserEventLinkService

router = APIRouter(prefix="/event")


@router.post(path="/create",
             response_model=EventRead,
             response_description="The created event.",
             summary="Create a new event.")
def create_event(*,
                 current_user: User = Depends(get_current_user),
                 session: Session = Depends(get_session),
                 event: EventCreate,
                 address: AddressCreate):
    """Create a new event.

    - **token**: usual authentication token
    - **event**: the event to create
    """
    new_event = EventService(session).create_event(event, address)
    link = UserEventLink(user_id=current_user.id,
                         event_id=new_event.id,
                         status=UserEventStatus.CREATOR)
    UserEventLinkService(session).create_user_event_link(link)
    return new_event


@router.get(path="/{event_id}",
            response_model=EventReadFull)
def read_event(*,
               _: User = Depends(get_current_user),  # needed ?
               session: Session = Depends(get_session),
               event_id: int):
    """Read a single event

    - **token**: usual authentication token.
    - **event_id**: the id of the event to read.
    """
    return EventService(session).read_event(event_id)
