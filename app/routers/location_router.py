from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.configs.api_dependencies import get_session
from app.models.locations import (LocationRead,
                                  LocationUpdate,
                                  LocationCreate,
                                  LocationReadApprox)
from app.services.location_services import LocationService

router = APIRouter(prefix="/location")


@router.post(path="/",
             response_model=LocationRead,
             response_description="Data of the created location.",
             summary="Create a new location.")
async def create_location(*,
                          session: Session = Depends(get_session),
                          location: LocationCreate):
    '''

    This function creates a new location in the database.

    - **body** : the location to create. Model LocationCreate.
    '''
    return LocationService(session).create_location(location)


@router.get(path="/",
            response_model=List[LocationRead],
            response_description="Data of all locations.",
            summary="Read all locations.")
async def read_locations(*,
                         session: Session = Depends(get_session)):
    '''
    This function reads all locations from the database.
    '''
    return LocationService(session).read_locations()


@router.get(path="/{event_id}",
            response_model=LocationRead,
            response_description="Data of the location.",
            summary="Read a single location.")
async def read_location(*,
                        session: Session = Depends(get_session),
                        event_id: int):
    '''
    This function reads a single location from the database.

    - **event_id** : the id of the location to read.
    '''
    return LocationService(session).read_location(event_id)


@router.get(path="/{event_id}/Approximate",
            response_model=LocationReadApprox,
            response_description="Data of the approximate location.",
            summary="Read a single location.")
async def read_location_approx(*,
                               session: Session = Depends(get_session),
                               event_id: int):
    '''
    This function reads a single location from the database.

    - **event_id** : the id of the location to read.
    '''
    return LocationService(session).read_location_approx(event_id)


@router.patch(path="/{event_id}",
              response_model=LocationRead,
              response_description="Data of the updated location.",
              summary="Update a location.")
async def update_location(*,
                          session: Session = Depends(get_session),
                          event_id: int,
                          location: LocationUpdate):
    '''
    This function updates a location in the database.

    - **event_id** : the id of the location to update.
    - **body** : the location to update. Model LocationUpdate.
    '''
    return LocationService(session).update_location(event_id, location)


@router.delete(path="/{event_id}",
               response_model=LocationRead,
               response_description="Data of the deleted location.",
               summary="Delete a location.")
async def delete_location(*,
                          session: Session = Depends(get_session),
                          event_id: int):
    '''
    This function deletes a location from the database.

    - **event_id** : the id of the location to delete.
    '''
    return LocationService(session).delete_location(event_id)
