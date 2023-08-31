"""This module contains useful functions used with geolocations.

Functions
---------
get_latlon_from_address(address)
    Get the coordinates from the address."""
import googlemaps

from app.configs.settings import ExtResourcesSettings
from app.models.addresses import AddressCreate
from app.models.latitudes_longitudes import LatLon

gmaps = googlemaps.Client(key=ExtResourcesSettings().gmaps_key)


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
