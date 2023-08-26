"""This module implements classes to handle database access for locations
Classes
-------
LocationDao(session)
    Data access for locations.
"""
from typing import List

from fastapi import HTTPException
from sqlmodel import Session, select

from app.models.locations import Location, LocationUpdate, LocationCreate, LocationReadApprox
import random
import math
import googlemaps
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='./app/env')

GoogleMapsKey = os.getenv('GoogleMapsKey')

gmaps = googlemaps.Client(key=GoogleMapsKey)

class LocationDao:
    """Data Access for locations.

    This class implements all methods for database operations for locations.
    All methods return a Location object.

    Methods
    -------
    create_location(self, location)
        Add a new location in database.
    read_location(self, event_id)
        Read a location from database using its id.
    read_locations(self, offset, limit)
        Read locations from database between offset and offset+limit.
    update_location(self, event_id, new_location)
        Update a location in database with new location data.
    delete_location(self, event_id)
        Delete a location from database using its id.
    """
    def __init__(self, session: Session):
        self.session = session

    def create_location(self, location: Location) -> Location:
        """Create a new Location in DB.

        Parameters
        ----------
        location : Location
            The location to add to database.

        Returns
        -------
        Location
            The created location.
        """
        coordinates = gmaps.geocode(f'{location.num} {location.street}, {location.city}, {location.zipcode}')[0]['geometry']['location']
        location.lat = coordinates['lat']
        location.lon = coordinates['lng']
        self.session.add(location)
        self.session.commit()
        self.session.refresh(location)
        return location

    def read_location(self, event_id: int) -> Location:
        """Read a single location using its id.

        Parameters
        ----------
        event_id : int
            The id of the event associated to the location to read.

        Returns
        -------
        Location
            The location of the event that was read.

        Raises
        ------
        HTTPException
            Raised when there is no location with that id.
        """
        location = self.session.get(Location, event_id)
        if location is None:
            raise HTTPException(status_code=404,
                                detail=f"Location associated to the event id {event_id} not found.")
        return location
    
    def read_location_approx(self, event_id: int) -> Location:
        """Read a single location using its id.

        Parameters
        ----------
        event_id : int
            The id of the event associated to the location to read.

        Returns
        -------
        Location
            The location of the event that was read.

        Raises
        ------
        HTTPException
            Raised when there is no location with that id.
        """
        location = self.session.get(Location, event_id)
        if location is None:
            raise HTTPException(status_code=404,
                                detail=f"Location associated to the event id {event_id} not found.")
        
        ## create the ramdomized location
        u = random.uniform(0, 1)
        v = random.uniform(0, 1)
        radius = 100
        r = radius / 111300
        w = r * math.sqrt(u)
        t = 2 * math.pi * u
        lat = w * math.cos(t)
        lon = w * math.sin(t)
        
        lat = lat/ math.cos(location.lon)
        
        location.lat = lat + location.lat
        location.lon = lon + location.lon
    
        return location
    
    # TODO : put that in service and not in dao
        
    def read_locations(self, offset: int, limit: int) -> List[Location]:
        """Read all locations from offset to offset+limit in the table.

        Parameters
        ----------
        offset : int
            Index at which to start reading.
        limit : int
            Number of entries to read.

        Returns
        -------
        List[Location]
            The locations read from table.
        """
        statement = select(Location).offset(offset).limit(limit)
        locations = self.session.exec(statement).all()
        return locations

    def update_location(self, event_id: int, new_location: LocationUpdate) -> Location:
        """Update a location with chosen id with new location data.

        Parameters
        ----------
        event_id : int
            id of the location to update.
        new_location : LocationUpdate
            The new location whose data to use for the update.

        Returns
        -------
        Location
            The updated location.

        Raises
        ------
        HTTPException
            Raised when there is no location with that id.
        """
        old_location = self.session.get(Location, event_id)
        if not old_location:
            raise HTTPException(status_code=404,
                                detail=f"Location associated to the event id {event_id} not found.")
        new_data = new_location.dict(exclude_unset=True)
        for key, value in new_data.items():
            setattr(old_location, key, value)
        coordinates = gmaps.geocode(f'{old_location.num} {old_location.street}, {old_location.city}, {old_location.zipcode}')[0]['geometry']['location']
        old_location.lat = coordinates['lat']
        old_location.lon = coordinates['lng']
        self.session.add(old_location)
        self.session.commit()
        self.session.refresh(old_location)
        return old_location

    def delete_location(self, event_id: int) -> Location:
        """Delete a location using its id.

        Parameters
        ----------
        event_id : int
            The id of the location to delete.

        Returns
        -------
        Location
            The deleted location.

        Raises
        ------
        HTTPException
            Raised when there is no location with that id.
        """
        location = self.session.get(Location, event_id)
        if not location:
            raise HTTPException(status_code=404,
                                detail=f"Location associated to the event id {event_id} not found.")
        self.session.delete(location)
        self.session.commit()
        return location