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

import googlemaps
import os
from dotenv import load_dotenv

import random
import math

load_dotenv(dotenv_path='./app/env')

GoogleMapsKey = os.getenv('GoogleMapsKey')

gmaps = googlemaps.Client(key=GoogleMapsKey)

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
        coordinates = gmaps.geocode(f'{location.num} {location.street}, {location.city}, {location.zipcode}')[0]['geometry']['location']
        location.lat = coordinates['lat']
        location.lon = coordinates['lng']
        return LocationDao(self.session).create_location(location)

    def read_location(self, event_id : int) -> Location:
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
    
    def read_location_approx(self, event_id : int) -> Location:
        '''Read a location from database.
        
        Parameters
        ----------
        event_id : int
            The id of the event to read.
            
        Returns
        -------
        Location
            The location read with approximate coordinates.
        '''
        location = LocationDao(self.session).read_location(event_id)
        
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
        location = Location.parse_obj(location)
        coordinates = gmaps.geocode(f'{location.num} {location.street}, {location.city}, {location.zipcode}')[0]['geometry']['location']
        location.lat = coordinates['lat']
        location.lon = coordinates['lng']        
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
