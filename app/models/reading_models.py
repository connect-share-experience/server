"""This module contains all models used only in path operations.

They allow to choose precisely what information the client gets, or what he
must provide.

Classes
-------
EventReadWithLatLon
    Used to read an event with its coordinates.
EventReadFull
    Used to read an event with its whole location.
EventCreateWithAddress
    Used to create an event with its address.
"""
from typing import Optional

from app.models.events import EventRead, EventCreate
from app.models.addresses import AddressRead, AddressCreate
from app.models.latitudes_longitudes import LatLonRead


class EventReadWithLatLon(EventRead):
    """Model used to read event with their coordinates.
    Attributes
    ----------
    latlon: Optional[LatLonRead]
        The coordinates of the event.
    """
    latlon: Optional[LatLonRead] = None


class EventReadFull(EventReadWithLatLon):
    """Model used to read event with their whole location.

    Attributes
    ----------
    address: Optional[AddressRead]
        The address of the event.
    """
    address: Optional[AddressRead] = None


class EventCreateWithAddress(EventCreate):
    """Model used to create event with their address.

    Attributes
    ----------
    address: AddressCreate
        The address of the event.
    """
    address: AddressCreate
