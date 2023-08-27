"""This module implements API endpoints handling user operations.

They are operations using the currently authenticated user.

Functions
---------
read_self()
    Read current user.
delete_self()
    Delete current user.
update_self(user)
    Update current user.
update_bio(new_bio)
    Update current user's bio.
read_sent_invites()
    Get the users that current user sent an invite to.
read_received_invites()
    Get the users that current user received an invite from.
read_friends()
    Get current user's friends.
"""
from typing import List
from fastapi import APIRouter, Depends, UploadFile
from sqlmodel import Session

from app.configs.api_dependencies import get_current_user, get_session
from app.models.users import User, UserRead, UserUpdate
from app.services.user_services import UserService

router = APIRouter(prefix="/me")


@router.get(path="/",
            response_model=UserRead,
            response_description="Data of current user.",
            summary="Read current user information.")
async def read_self(*,
                    current_user: User = Depends(get_current_user)):
    """
    Using only the authentication token, read info of the current user.

    - **token** : usual authentication header token.
    """
    return current_user


@router.delete(path="/",
               response_model=UserRead,
               response_description="Data of deleted current user.",
               summary="Delete current user.")
async def delete_self(*,
                      current_user: User = Depends(get_current_user),
                      session: Session = Depends(get_session)):
    """
    Using only the authentication token, delete current user.

    - **token** : usual authentication header token.
    """
    return UserService(session).delete_user(current_user.id)


@router.patch(path="/",
              response_model=UserRead,
              response_description="Data of the current user updated.",
              summary="Update current user data.")
async def update_self(*,
                      current_user: User = Depends(get_current_user),
                      session: Session = Depends(get_session),
                      user: UserUpdate):
    """
    Update the information of the current user.

    - **token** : usual authentication header token.
    - **body** : the new info to use. Model UserCreate.
    """
    return UserService(session).update_user(current_user.id, user)


@router.patch(path="/bio",
              response_model=UserRead,
              response_description="Data of the current user updated.",
              summary="Update current user bio.")
async def update_bio(*,
                     current_user: User = Depends(get_current_user),
                     session: Session = Depends(get_session),
                     new_bio: str):
    """
    Update the bio of the current user.

    - **token** : usual authentication header token.
    - **new_bio** : The new bio to replace the current user's with.
    """
    new_user = UserUpdate(bio=new_bio)
    return UserService(session).update_user(current_user.id, new_user)


@router.get(path="/sent_invites",
            response_model=List[UserRead],
            response_description="List of users that invites were sent to.",
            summary="Read current user sent invites.")
def read_sent_invites(*,
                      current_user: User = Depends(get_current_user),
                      session: Session = Depends(get_session)):
    """
    Get the list of users that the current user sent a invite to.
    Only unaccepted invites are selected.

    - **token** : usual authentication header token.
    """
    return UserService(session).read_user_sent_invites(current_user.id)


@router.get(path="/received_invites",
            response_model=List[UserRead],
            response_description="List of users that sent invites.",
            summary="Read current user received invites.")
def read_received_invites(*,
                          current_user: User = Depends(get_current_user),
                          session: Session = Depends(get_session)):
    """
    Get the list of users that the current user received an invite from.
    Only unaccepted invites are selected.

    - **token** : usual authentication header token.
    """
    return UserService(session).read_user_received_invites(current_user.id)


@router.get(path="/friends",
            response_model=List[UserRead],
            response_description="List of friends.",
            summary="Get the friends of the current user.")
def read_friends(*,
                 current_user: User = Depends(get_current_user),
                 session: Session = Depends(get_session)):
    """
    Get the list of friends of the current user.

    - **token** : usual authentication header token.
    """
    return UserService(session).read_friends(current_user.id)


@router.patch(path="/picture",
              response_model=UserRead,
              response_description="The updated user with picture.",
              summary="Update a user's profile picture.")
def update_picture(*,
                   current_user: User = Depends(get_current_user),
                   session: Session = Depends(get_session),
                   file: UploadFile):
    """
    Update the profile picture of the current user.

    - **token** usual authentication header token.
    - **file** the picture to upload. Use png or jpg.
    """
    return UserService(session).update_picture(current_user.id, file)
