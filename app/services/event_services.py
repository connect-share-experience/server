"""This module implements services relating to the events.

Classes
-------
EventService
    Intermediate services for events.
"""
import os
import shutil

from fastapi import UploadFile
from sqlmodel import Session

from app.configs.settings import StaticSettings
from app.dao.event_dao import EventDao
from app.models.addresses import Address, AddressCreate
from app.models.events import Event, EventUpdate, EventCreate
from app.utils.geoloc_utils import get_latlon_from_address
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

    def read_event(self,
                   event_id: int) -> Event:
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
