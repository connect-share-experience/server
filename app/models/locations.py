"""This module defines models used to handle event location.

Classes
-------
Location(SQLModel):
    This class handle event locations in database.
"""
from typing import Optional, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.events import Event


class _LocationBase(SQLModel):
    """This is the base model for other location models.

    For attributes, see each specific class.
    """
    lat: float
    lon: float
    other: Optional[str]
    # We'll use the custom validator if we actually use lat, lon


class Location(_LocationBase, table=True):
    """This class manages event locations.

    Attributes
    ----------
    lat: float
        Latitude of the location.
    lon: float
        Longitude of the location.
    other: Optional[str]
        Additional information, such as floor or access instructions.
    event_id: Optional[int]
        Id of the event.
    event: Event
        The event that takes place at that location.
    """
    event_id: Optional[int] = Field(default=None,
                                    foreign_key="event.id",
                                    primary_key=True)
    event: Optional['Event'] = Relationship(back_populates="location")
