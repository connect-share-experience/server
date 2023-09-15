"""This module implements API endpoints handling event operations.

Functions
---------
create_event(event)
    Create an event, with its address.
read_event(event_id)
    Read an event with detailed location.
"""
from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.configs.api_dependencies import get_current_user, get_session
from app.models.addresses import AddressCreate
from app.models.enums import UserEventStatus, EventCategory
from app.models.events import EventCreate, EventRead
from app.models.latitudes_longitudes import LatLonRead
from app.models.links import UserEventLink
from app.models.reading_models import EventReadWithLatLon
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
            response_model=EventReadWithLatLon,
            response_description="The event with an approximate location.",
            summary="Read an event with approximate location.")
def read_event(*,
               _: User = Depends(get_current_user),
               session: Session = Depends(get_session),
               event_id: int):
    """Read a single event with approximate coordinates.

    - **token**: usual authentication token.
    - **event_id**: the id of the event to read.
    """
    return EventService(session).read_event_approx(event_id)


@router.get(path="/in_area/{radius}",
            response_model=List[EventReadWithLatLon],
            response_description="All events with radius around location.",
            summary="Get events to come in area.")
def read_events_in_radius(*,
                          _: User = Depends(get_current_user),
                          session: Session = Depends(get_session),
                          latlon: LatLonRead,
                          radius: int,
                          category: Optional[EventCategory]):
    """Read all upcoming events in radius around coordinates.

    - **token**: usual authentication token
    - **latlon**: coordinates around which to look for events
    - **radius**: the radius in which to look for events
    """
    return EventService(session).read_events_to_come_in_area(latlon,
                                                             radius,
                                                             category)


@router.get(path="/join/{event_id}",
            response_model=UserEventLink,
            response_description="The created link between user and event.",
            summary="Request to join an event")
def ask_to_join(*,
                current_user: User = Depends(get_current_user),
                session: Session = Depends(get_session),
                event_id: int):
    """Lets the current user request to join the event

    - **token**: current authentication token.
    - **event_id**: the id of the event to join.
    """
    link = UserEventLink(user_id=current_user.id,
                         event_id=event_id,
                         status=UserEventStatus.PENDING)
    return UserEventLinkService(session).create_user_event_link(link)
