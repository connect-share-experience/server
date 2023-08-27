'''This module defines models used to handle event location.

Classes
-------
Location(SQLModel):
    This class handle event locations in database.
'''
from typing import Optional, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.events import Event


class _AddressBase(SQLModel):
    '''This is the base model for other address models.

    For attributes, see each specific class.
    '''
    num: Optional[int]
    street: Optional[str]
    city: Optional[str]
    zipcode: Optional[int]
    other: Optional[str]
    # We'll use the custom validator if we actually use lat, lon


class _AddressBaseStrict(SQLModel):
    '''This model is used to validate the address data before

    For attributes, see each specific class.
    '''
    num: int
    street: str
    city: str
    zipcode: int
    other: Optional[str]
    # We'll use the custom validator if we actually use lat, lon


class _LatLonBase(SQLModel):
    '''This is the base model for other lat/lon models.

    For attributes, see each specific class.
    '''
    lat: Optional[float] = Field(gt=-90, lt=90)
    lon: Optional[float] = Field(gt=-180, lt=180)


class _LatLonBaseStrict(SQLModel):
    '''This model is used to validate the coordinates before

    For attributes, see each specific class.
    '''
    lat: float = Field(gt=-90, lt=90)
    lon: float = Field(gt=-180, lt=180)


class LocationCreate(_AddressBaseStrict):
    '''Model for creating locations.

    Attributes
    ----------
    num : int
        The num component of the address.
    street : str
        The name of the street the event takes place.
    city : str
        The city of the event.
    zipcode : int
        The zipcode of the event.
    other: Optional[str]
        Additional information, such as floor or access instructions.
    '''


class LocationUpdate(_AddressBase, _LatLonBase):
    '''Model for updating the location of the event.

    Attributes
    ----------
    lat: Optional[float] = Field(gt=-90, lt=90)
        Latitude of the location.
    lon: Optional[float] = Field(gt=-180, lt=180)
        Longitude of the location.
    num : Optional[int]
        The num component of the address.
    street : Optional[str]
        The name of the street the event takes place.
    city : Optional[str]
        The city of the event.
    zipcode : Optional[int]
        The zipcode of the event.
    other: Optional[str]
        Additional information, such as floor or access instructions.
    '''


class LocationReadApprox(_LatLonBaseStrict):
    '''This class manages event locations.

    Attributes
    ----------
    lat: float = Field(gt=-90, lt=90)
        Latitude of the location.
    lon: float = Field(gt=-180, lt=180)
        Longitude of the location.
    '''


class LocationRead(_LatLonBaseStrict, _AddressBaseStrict):
    '''This class manages event locations.

    Attributes
    ----------
    lat: float = Field(gt=-90, lt=90)
        Latitude of the location.
    lon: float = Field(gt=-180, lt=180)
        Longitude of the location.
    num : int
        The num component of the address.
    street : str
        The name of the street the event takes place.
    city : str
        The city of the event.
    zipcode : int
        The zipcode of the event.
    other: Optional[str]
        Additional information, such as floor or access instructions.
    '''


class Location(_AddressBaseStrict, _LatLonBaseStrict, table=True):
    '''This class manages event locations.

    Attributes
    ----------
    lat: float = Field(gt=-90, lt=90)
        Latitude of the location.
    lon: float = Field(gt=-180, lt=180)
        Longitude of the location.
    num : int
        The num component of the address.
    street : str
        The name of the street the event takes place.
    city : str
        The city of the event.
    zipcode : int
        The zipcode of the event.
    other: Optional[str]
        Additional information, such as floor or access instructions.
    event_id: Optional[int]
        Id of the event.
    event: Event
        The event that takes place at that location.
    '''
    event_id: Optional[int] = Field(default=None,
                                    foreign_key="event.id",
                                    primary_key=True)
    event: Optional['Event'] = Relationship(back_populates="location")
