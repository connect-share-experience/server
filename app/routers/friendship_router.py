"""This module implements API endpoints handling friendship operations.

They all use the currently authenticated user.

Functions
---------
send_invite(user_id)
    Send a friendship invite.
accept_invite(user_id)
    Accept a received friendship invite.
unsend_invite(user_id)
    Rescind a friendship invite sent to another user.
reject_invite(user_id)
    Reject a friendship invite received from another user.
delete_friend(user_id)
    Delete a friendship from the current user's list.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.configs.api_dependencies import get_current_user, get_session
from app.models.enums import FriendshipStatus
from app.models.users import User, UserRead
from app.services.friendship_services import FriendshipService

router = APIRouter(prefix="/friendship")


@router.post(path="/send/{user_id}",
             response_model=UserRead,
             response_description="The user the created invite was sent to.",
             summary="Create a friendship invite.")
def send_invite(*,
                current_user: User = Depends(get_current_user),
                session: Session = Depends(get_session),
                user_id: int):
    """
    Send an invite from the current user to another one.

    - **token** : usual authentication header token.
    - **user_id** : the id of the user to send the invite to.
    """
    friendship = FriendshipService(session).create_friendship(current_user.id,
                                                              user_id)
    return friendship.invite_receiver


@router.patch(path="/accept/{user_id}",
              response_model=UserRead,
              response_description="The user whose invite was accepted.",
              summary="Accept a received friendship invite.")
def accept_invite(*,
                  current_user: User = Depends(get_current_user),
                  session: Session = Depends(get_session),
                  user_id: int):
    """
    Lets the current user accept a friendship invite received from another one.

    - **token** : usual authentication header token.
    - **user_id** : the id of the user whose invite to accept.
    """
    friendship = (FriendshipService(session).update_friendship_status(
        user_id,
        current_user.id,
        new_status=FriendshipStatus.ACCEPTED))
    return friendship.invite_sender


@router.delete(path="/uninvite/{user_id}",
               response_model=UserRead,
               response_description="The user the invite was sent to.",
               summary="Rescind an invitation.")
def unsend_invite(*,
                  current_user: User = Depends(get_current_user),
                  session: Session = Depends(get_session),
                  user_id: int):
    """
    Rescind an invitation sent from current user to another one.

    - **token** : usual authentication header token.
    - **user_id** : the id of the user the invite was sent to.
    """
    friendship = (FriendshipService(session)
                  .delete_friendship(current_user.id, user_id))
    return friendship.invite_receiver


@router.delete(path="/reject_invite/{user_id}",
               response_model=UserRead,
               response_description="The user whose invite was rejected.",
               summary="Deny a friendship invite.")
def reject_invite(*,
                  current_user: User = Depends(get_current_user),
                  session: Session = Depends(get_session),
                  user_id: int):
    """
    Let the current user reject a friendship invite sent by another one.

    - **token** : usual authentication header token.
    - **user_id** : the id of the user the invite was received from.
    """
    friendship = (FriendshipService(session)
                  .delete_friendship(user_id, current_user.id))
    return friendship.invite_sender


@router.delete(path="/friends/{user_id}",
               response_model=UserRead,
               response_description="The user that was in the friendship.",
               summary="Delete a frienship.")
def delete_friend(*,
                  current_user: User = Depends(get_current_user),
                  session: Session = Depends(get_current_user),
                  user_id: int):
    """
    Let the current user delete a friendship with another one.

    - **token** : usual authentication header token.
    - **user_id** : the id of the user that's part of the friendship to delete.
    """
    friendship = (FriendshipService(session)
                  .get_friendship(current_user.id, user_id))
    if (isinstance(friendship.invite_sender_id, int) and
       isinstance(friendship.invite_receiver_id, int)):
        return (FriendshipService(session)
                .delete_friendship(sender_id=friendship.invite_sender_id,
                                   receiver_id=friendship.invite_receiver_id))
    raise HTTPException(401, "Error fetching friendship")
