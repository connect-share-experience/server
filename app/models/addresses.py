"""This module defines all models used to hanfle users.

These classes collect all data related to the event addresses.

Classes
-------
AddressCreate(SQLModel)
AddressUpdate(SQLModel)
AddressRead(SQLModel)
Address(SQLModel, table=True)
"""
from typing import Optional, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.events import Event


class _AddressBase(SQLModel):
    """Base model for all address models.

    This contains the attributes that are common to each address class.
    """
    num: Optional[int]
    street: Optional[str]
    city: Optional[str]
    zipcode: Optional[int]
    other: Optional[str]


class _AddressBaseStrict(_AddressBase):
    """Similar to _AdressBase, but stricter."""
    num: int
    street: str
    city: str
    zipcode: int


class AddressCreate(_AddressBaseStrict):
    """Model for creating addresses."""


class AddressUpdate(_AddressBase):
    """Model for updating adresses."""


class AddressRead(_AddressBaseStrict):
    """Model for reading addresses."""


class Address(_AddressBaseStrict, table=True):
    """Models for addresses in database.

    Attributes
    ----------
    num: int
        Street number.
    street: str
        Street name.
    zipcode: int
        Zipcode of the city.
    city: str
        City.
    other: Optional[str]
        Some other comment needed to find the event.
    event_id: Optional[int]
        The id of the event.
    event: Optional[Event]
        The event.
    """
    event_id: Optional[int] = Field(default=None,
                                    foreign_key="event.id",
                                    primary_key=True)
    event: Optional['Event'] = Relationship(
        back_populates="address",
        sa_relationship_kwargs={'uselist': False})
