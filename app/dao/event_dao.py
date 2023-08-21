"""This module implements classes to handle database access for events
Classes
-------
EventDao(session)
    Data access for events.
"""
from typing import List

from fastapi import HTTPException
from sqlmodel import Session, select

from app.models.events import Event, EventUpdate


class EventDao:
    """Data Access for events.

    This class implements all methods for database operations for events.
    All methods return a Event object.

    Methods
    -------
    create_event(self, event)
        Add a new event in database.
    read_event(self, event_id)
        Read a event from database using its id.
    read_events(self, offset, limit)
        Read events from database between offset and offset+limit.
    update_event(self, event_id, new_event)
        Update a event in database with new event data.
    delete_event(self, event_id)
        Delete a event from database using its id.
    """
    def __init__(self, session: Session):
        self.session = session

    def create_event(self, event: Event) -> Event:
        """Create a new Event in DB.

        Parameters
        ----------
        event : Event
            The event to add to database.

        Returns
        -------
        Event
            The created event.
        """
        self.session.add(event)
        self.session.commit()
        self.session.refresh(event)
        return event

    def read_event(self, event_id: int) -> Event:
        """Read a single event using its id.

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
            Raised when there is no event with that id.
        """
        event = self.session.get(Event, event_id)
        if event is None:
            raise HTTPException(status_code=404,
                                detail=f"Event with id {event_id} not found.")
        return event

    def read_events(self, offset: int, limit: int) -> List[Event]:
        """Read all events from offset to offset+limit in the table.

        Parameters
        ----------
        offset : int
            Index at which to start reading.
        limit : int
            Number of entries to read.

        Returns
        -------
        List[Event]
            The events read from table.
        """
        statement = select(Event).offset(offset).limit(limit)
        events = self.session.exec(statement).all()
        return events

    def update_event(self, event_id: int, new_event: EventUpdate) -> Event:
        """Update a event with chosen id with new event data.

        Parameters
        ----------
        event_id : int
            id of the event to update.
        new_event : Event
            The new event whose data to use for the update.

        Returns
        -------
        Event
            The updated event.

        Raises
        ------
        HTTPException
            Raised when there is no event with that id.
        """
        old_event = self.session.get(Event, event_id)
        if not old_event:
            raise HTTPException(status_code=404,
                                detail=f"Event with id {event_id} not found.")
        new_data = new_event.dict(exclude_unset=True)
        for key, value in new_data.items():
            setattr(old_event, key, value)

        self.session.add(old_event)
        self.session.commit()
        self.session.refresh(old_event)
        return old_event

    def delete_event(self, event_id: int) -> Event:
        """Delete a event using its id.

        Parameters
        ----------
        event_id : int
            The id of the event to delete.

        Returns
        -------
        Event
            The deleted event.

        Raises
        ------
        HTTPException
            Raised when there is no event with that id.
        """
        event = self.session.get(Event, event_id)
        if not event:
            raise HTTPException(status_code=404,
                                detail=f"Event with id {event_id} not found.")
        self.session.delete(event)
        self.session.commit()
        return event
