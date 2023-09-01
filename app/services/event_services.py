"""This module implements services relating to the events.

Classes
-------
EventService
    Intermediate services for events.
"""
from datetime import datetime as dttime
from typing import List
import os
import shutil

from fastapi import HTTPException, UploadFile
from sqlmodel import Session

from app.configs.settings import StaticSettings
from app.dao.event_dao import EventDao
from app.models.addresses import Address, AddressCreate
from app.models.events import Event, EventCreate, EventUpdate
from app.models.latitudes_longitudes import LatLon, LatLonRead
from app.utils.geoloc_utils import (get_latlon_from_address,
                                    get_random_latlon,
                                    is_within_radius)
from app.utils.picture_utils import create_picture_name


class EventService:
    """Intermediate services for events.

    This class implements operations between router and dao layers.

    Methods
    -------
    create_event(event)
        Create a new event.s
    delete_event(sender_id, receiver_id)
        Delete a event.
    update_event_status(sender_id, receiver_id)
        Update a event's status.
    """
    def __init__(self, session: Session):
        self.session = session

    def create_event(self,
                     event: EventCreate,
                     address: AddressCreate) -> Event:
        """Create a frienship in database.

        Parameters
        ----------
        event : Event
            The new event to create.

        Returns
        -------
        Event
            The event created.
        """
        new_event = Event.parse_obj(event)
        new_event.address = Address.parse_obj(address)
        new_event.latlon = get_latlon_from_address(address)
        db_event = EventDao(self.session).create_event(new_event)
        try:
            os.mkdir(path=f"{StaticSettings().events_dir}/event_{db_event.id}")
        except FileExistsError:
            pass
        return db_event

    def read_event(self, event_id: int) -> Event:
        """Read a single event.

        Parameters
        ----------
        event_id : int
            The id of the event to read.

        Returns
        -------
        Event
            The event that was read.
        """
        return EventDao(self.session).read_event(event_id)

    def read_event_approx(self, event_id: int) -> Event:
        """Read an event with approximate coordinates.

        Parameters
        ----------
        event_id : int
            The id of the event to read.

        Returns
        -------
        Event
            The event that was read.

        Raises
        ------
        HTTPException
            Raised when the event has no coordinates.
        """
        event = EventDao(self.session).read_event(event_id)
        if event.latlon is None:
            raise HTTPException(status_code=421,
                                detail="Event does not have coordinates")
        new_latlon = get_random_latlon(event.latlon)
        event.latlon = new_latlon
        return event

    def update_event(self,
                     event_id: int,
                     new_event: EventUpdate) -> Event:
        """Update an event status.

        Parameters
        ----------
        event_id : int
            The id of the event.
        new_event : EventUpdate
            The new event.

        Returns
        -------
        Event
            The updated event.
        """
        return EventDao(self.session).update_event(event_id, new_event)

    def delete_event(self,
                     event_id: int) -> Event:
        """Delete a event.

        Parameters
        ----------
        event_id : int
            The id of the event.


        Returns
        -------
        Event
            The deleted event.
        """
        return EventDao(self.session).delete_event(event_id)

    def update_picture(self, event_id: int, picture: UploadFile) -> Event:
        """Update an event page picture.

        Parameters
        ----------
        event_id : int
            The id of the event whose picture to update.
        picture : UploadFile
            The picture to use.

        Returns
        -------
        Event
            The updated event.
        """
        file_path = StaticSettings().event_page_pic_dir

        token_name = create_picture_name(picture)

        event = EventDao(self.session).update_picture(event_id, token_name)

        with open(f"{file_path}/{event.picture}", "wb") as buffer:
            shutil.copyfileobj(picture.file, buffer)
        picture.file.close()

        return event

    def read_events_to_come_in_area(self,
                                    latlon: LatLonRead,
                                    radius: int) -> List[Event]:
        """Read all events to come within radius arount coordinates.

        Parameters
        ----------
        latlon : LatLonRead
            The coordinates around which to search.
        radius : int
            The radius in which to search.

        Returns
        -------
        List[Event]
            The read events.
        """
        events = EventDao(self.session).read_all_events()
        wanted_events: List[Event] = []
        for event in events:
            full_latlon = LatLon.parse_obj(latlon)
            if event.latlon is None:
                raise HTTPException(status_code=421,
                                    detail="Event has no coordinates.")
            verify = is_within_radius(full_latlon, event.latlon, radius)
            if event.start_time > dttime.now() and verify is True:
                wanted_events.append(event)
        return wanted_events
