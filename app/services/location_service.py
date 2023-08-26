"""This module implements services relating to the locations.

Classes
-------
LocationService
    Intermediate services for locations.
"""
from datetime import date

from sqlmodel import Session
from app.dao.location_dao import LocationDao
from app.models.locations import Location, LocationUpdate, LocationCreate



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

    def create_location(self, location : LocationCreate) -> Location:
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
        location = Location.parse_obj(location)
        return LocationDao(self.session).create_location(location)

    def read_location(self, event_id) -> Location:
        """Read a location from database.
        
        Parameters
        ----------
        event_id : int
            The id of the event to read.
        
        Returns
        -------
        Location
            The location read.
        """
        return LocationDao(self.session).read_location(event_id)
    
    

    def update_location(self, event_id : int ,location :  LocationUpdate) -> Location:
        """Update a location in database.
        
        Parameters
        ----------
        event_id : int
            The id of the event to update.
        location : LocationUpdate
            The new location data.
            
        Returns
        -------
        Location
            The updated location.
        """
        
        return LocationDao(self.session).update_location(event_id,location)

    def delete_location(self, event_id) -> Location:
        """Delete a location from database.
        
        Parameters
        ----------
        event_id : int
            The id of the event to delete.
            
        Returns
        -------
        Location
            The deleted location.
        """
        
        return LocationDao(self.session).delete_location(event_id)
