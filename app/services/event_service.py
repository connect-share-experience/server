"""This module implements services relating to the events.

Classes
-------
EventService
    Intermediate services for events.
"""
from datetime import datetime

from sqlmodel import Session

from app.dao.event_dao import EventDao
from app.models.events import Event, EventUpdate
from app.models.enums import EventCategory

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
                     name : str,
                     desc : str,
                     category : EventCategory,
                     datetime : datetime,
                     capacity : int) -> Event:
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
        event = Event(name = name, 
                        desc = desc,
                        category = category,
                        datetime = datetime,
                        capacity = capacity)
        return EventDao(self.session).create_event(event)


    def update_event(self,
                                 event_id: int,
                                 new_event: EventUpdate) -> Event:
        """Update a event status.

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
        return (EventDao(self.session)
                .update_event(event_id, new_event))

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
