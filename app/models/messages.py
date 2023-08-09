"""This module implements classes to handle messages in events.

Classes
-------
Message(SQLModel)
    Implements messages posted on events.
"""
from datetime import datetime as dtdatetime
from typing import Optional, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.events import Event


class Message(SQLModel, table=True):
    """This class implements messages posted on events.

    Only the event creator can post a message, at a given datetime.

    Attributes
    ----------
    datetime: Optional[datetime]
        The date an time the message was sent. Fills when created.
    text: str
        The content of the message.
    event_id: Optional[int]
        Id of the event the message refers to.
    event: Optional[Event]
        Event the message refers to.
    """
    event_id: Optional[int] = Field(default=None,
                                    foreign_key="event.id",
                                    primary_key=True)
    datetime: Optional[dtdatetime] = Field(default=dtdatetime.now(),
                                           primary_key=True)
    text: str = Field(max_length=3000)

    event: Optional["Event"] = Relationship(back_populates="messages")
