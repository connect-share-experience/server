"""This module implements services relating to the locations.

Classes
-------
LocationService
    Intermediate services for locations.
"""
from datetime import date

from sqlmodel import Session

from app.dao.location_dao import LocationDao
from app.models.locations import Location, LocationUpdate


class LocationService:
    """Intermediate services for locations.

    This class implements operations between router and dao layers.

    Methods
    -------
    create_location(location)
        Create a new location.
    get_location(user1_id, user2_id)
        Read a single location both ways.
    delete_location(sender_id, receiver_id)
        Delete a location.
    update_location_status(sender_id, receiver_id)
        Update a location's status.
    """
    def __init__(self, session: Session):
        self.session = session

    def create_location(self,
                          event_id: int,
                          lat : float,
                          lon : float) -> Location:
        """Create a location in database.

        Parameters
        ----------
        location : Location
            The new location to create.

        Returns
        -------
        Location
            The location created.
        """
        location = Location(event_id=event_id,
                                lat=lat,
                                lon=lon)
        return LocationDao(self.session).create_location(location)


    def update_location(self,
                                 lat : float,
                                 lon : float) -> Location:
        """Update a location status.

        Parameters
        ----------
        sender_id : int
            The id of the user that sent the location invite.
        receiver_id : int
            The id of the user that reveived the location invite.
        new_status : bool
            The status of the relationship. True if accepted, False otherwise.

        Returns
        -------
        Location
            The updated location.
        """
        return (LocationDao(self.session)
                .update_location(LocationUpdate(lat=lat,lon=lon)))

    def delete_location(self,
                          event_id) -> Location:
        """Delete a location.

        Parameters
        ----------
        sender_id : int
            The id of the user that sent the location invite.
        receiver_id : int
            The id of the user that received the frienship invite.

        Returns
        -------
        Location
            The deleted location.
        """
        return LocationDao(self.session).delete_location(event_id)
