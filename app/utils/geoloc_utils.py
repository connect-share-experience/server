"""This module contains useful functions used with geolocations.

Functions
---------
get_latlon_from_address(address)
    Get the coordinates from the address.
get_random_latlon(latlon):
    Create a random latlon nearby
"""
import math
import random

from geopy import distance
from googlemaps import Client

from app.configs.settings import ExtResourcesSettings
from app.models.addresses import AddressCreate
from app.models.latitudes_longitudes import LatLon

gmaps = Client(key=ExtResourcesSettings().gmaps_key)
RADIUS_METERS = 100


def get_latlon_from_address(address: AddressCreate) -> LatLon:
    """Get the coordinates of a place using its address.

    This uses the Google Maps API

    Parameters
    ----------
    address : AddressCreate
        The address of the place.

    Returns
    -------
    LatLon
        The latitude-longitude coordinates of the place.
    """
    temp_coords = gmaps.geocode(f"{address.num} {address.street}," +
                                f"{address.city}, {address.zipcode}")
    coordinates = temp_coords[0]['geometry']['location']
    return LatLon(lat=coordinates['lat'],
                  lon=coordinates['lng'])


def get_random_latlon(latlon: LatLon) -> LatLon:
    """Create random latlon coordinates.

    We create random coordinates within the radius around the given latlon.

    Parameters
    ----------
    latlon : LatLon
        The coordinates around which to create random ones.
    radius : int
        The radius within which to create the random coordinates.

    Returns
    -------
    LatLon
        The randomly generated coordinates.
    """
    # Generate random radius and theta to use for polar coordinates
    random_u = random.uniform(0, 1)
    random_v = random.uniform(0, 1)
    radius_degrees = RADIUS_METERS/1113000
    radius = radius_degrees * math.sqrt(random_u)
    theta = 2 * math.pi * random_v

    # Create the actual coordinates within the radius
    small_lat = radius * math.cos(theta)
    small_lon = radius * math.sin(theta)

    # Take into account the shrinking of the east-west distances
    small_lat = small_lat / math.cos(latlon.lon)

    # Add those small vector to current coordinates
    latlon.lat += small_lat
    latlon.lon += small_lon

    return latlon


def is_within_radius(latlon1: LatLon, latlon2: LatLon, radius: int) -> bool:
    """Check wether the coordinates are within radius distance of each other.

    Parameters
    ----------
    latlon1 : LatLon
        The first set of coordinates.
    latlon2 : LatLon
        The second set of coordinates.
    radius : int
        The distance -in meters- to check for.

    Returns
    -------
    bool
        True if the coordinates are closer than radius, False otherwise.
    """
    coords1 = (latlon1.lat, latlon1.lon)
    coords2 = (latlon2.lat, latlon2.lon)
    meters_dist = distance.distance(coords1, coords2).meters
    if meters_dist <= radius:
        return True
    return False
