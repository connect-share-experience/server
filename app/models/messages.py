"""This module implements classes to handle messages in events.

Classes
-------
Message(SQLModel)
    Implements messages posted on events.
"""
from datetime import datetime as dttime
from typing import Optional, TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from app.models.enums import MessageCategory
if TYPE_CHECKING:
    from app.models.events import Event
    from app.models.users import User


class Message(SQLModel, table=True):
    """This class implements messages posted on events.

    Only the event creator can post a message, at a given datetime.

    Attributes
    ----------
    datetime: Optional[datetime]
        The date an time the message was sent. Fills when created.
    text: str
        The content of the message. Image identifier in such case.
    event_id: Optional[int]
        Id of the event the message refers to.
    event: Optional[Event]
        Event the message refers to.
    """
    event_id: Optional[int] = Field(default=None,
                                    foreign_key="event.id",
                                    primary_key=True)
    user_id: Optional[int] = Field(default=None,
                                   foreign_key="user.id",
                                   primary_key=True)
    datetime: Optional[dttime] = Field(default=dttime.now(),
                                       primary_key=True)
    category: MessageCategory
    text: str = Field(max_length=3000)

    event: Optional["Event"] = Relationship(back_populates="messages")
    user: Optional["User"] = Relationship(back_populates="messages")
