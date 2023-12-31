"""This module defines all models used to handlle events.

Classes
-------
EventCreate(SQLModel)
    Model for creating events.
EventUpdate(SQLModel)
    Model for creating events.
EventRead(SQLModel)
    Model for reading events.
Event(SQLModel, table=True)
    Model for events in database.
"""
from datetime import datetime as dttime
from typing import List, Optional, TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from app.models.enums import EventCategory

if TYPE_CHECKING:
    from app.models.addresses import Address
    from app.models.latitudes_longitudes import LatLon
    from app.models.links import UserEventLink
    from app.models.messages import Message
    from app.models.ranking_parameters import RankingParameters


class _EventBase(SQLModel):
    """Base model for all event models.

    This contains the attributes that are common to each event model.
    For attributes and methods, see each specifics class.
    """
    name: Optional[str] = Field(max_length=100)
    desc: Optional[str] = Field(max_length=2000)
    category: Optional[EventCategory]
    start_time: Optional[dttime]
    end_time: Optional[dttime]
    capacity: Optional[int] = Field(gt=1)


class _EventBaseStrict(_EventBase):
    """Similar to _EventBase, but with stricter restrictions."""
    name: str = Field(max_length=100)
    desc: str = Field(max_length=2000)  # optional
    category: EventCategory
    start_time: dttime
    end_time: dttime
    capacity: int = Field(ge=2)


class EventUpdate(_EventBase):
    """Model for updateing events.

    Attributes
    ----------
    category: Optional[EventCategory]
        The type of event. The list of possibilities is fixed.
    capacity: Optional[int]
        The attendees capacity. Must be at least 2.
    start_time: Optional[datetime]
        The date and time the event starts.
    end_time: Optional[datetime]
        The date and time the event ends.
    desc: Optional[str]
        A description of the event. Maximum 2000 characters.
    """


class EventCreate(_EventBaseStrict):
    """Model for creating events.

    Attributes
    ----------
    category: EventCategory
        The type of event. The list of possibilities is fixed.
    capacity: int
        The attendees capacity. Must be at least 2.
    start_time: datetime
        The date and time the event starts.
    end_time: datetime
        The date and time the event ends.
    desc: str
        A description of the event. Maximum 2000 characters.
    """


class EventRead(_EventBaseStrict):
    """Model for reading events.

    Attributes
    ----------
    category: EventCategory
        The type of event. The list of possibilities is fixed.
    capacity: int
        The attendees capacity. Must be at least 2.
    start_time: datetime
        The date and time the event starts.
    end_time: datetime
        The date and time the event ends.
    desc: str
        A description of the event. Maximum 2000 characters.
    id: int
        Unique event identifier.
    """
    id: int
    picture: str


class Event(_EventBaseStrict, table=True):
    """Model for events in database.

    Attributes
    ----------
    category: EventCategory
        The type of event. The list of possibilities is fixed.
    capacity: int
        The attendees capacity. Must be at least 2.
    start_time: datetime
        The date and time the event starts.
    end_time: datetime
        The date and time the event ends.
    desc: str
        A description of the event. Maximum 2000 characters.
    id: int
        Unique event identifier.
    location: Optional[Location]
        The location of the event.
    user_links: List["UserEventLink"]
        The links between the event and the users, whether they created,
        requested of attended it.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    picture: str = Field(default="default_event_pic.png")

    latlon: Optional['LatLon'] = Relationship(
        back_populates="event",
        sa_relationship_kwargs={'uselist': False})

    address: Optional['Address'] = Relationship(
        back_populates="event",
        sa_relationship_kwargs={'uselist': False})

    user_links: List["UserEventLink"] = Relationship(back_populates="event")

    messages: List["Message"] = Relationship(back_populates="event")
    ranking_parameters: List["RankingParameters"] = Relationship(
                                                        back_populates="event")
