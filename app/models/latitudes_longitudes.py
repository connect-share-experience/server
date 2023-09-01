"""This module defines all models used to handle lat-lon coordinates

Classes
-------
LatLonRead(SQLModel)
LatLon(SQLModel, table=True)
"""
from typing import Optional, TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.events import Event


class _LatLonBase(SQLModel):
    """Base model for all LatLon models.

    This contains the attributes that are common to each LatLon class.
    """
    lat: float
    lon: float


class LatLonRead(_LatLonBase):
    """Model for reading coordinates."""


class LatLon(_LatLonBase, table=True):
    """Model for coordinates in database.

    Attributes
    ----------
    lat: float
        The latitude
    lon: float
        The longitude
    event_id: int
        The id of the event
    event: Event
        The event
    """
    event_id: Optional[int] = Field(default=None,
                                    foreign_key="event.id",
                                    primary_key=True)
    event: Optional['Event'] = Relationship(
        back_populates="latlon",
        sa_relationship_kwargs={'uselist': False})
