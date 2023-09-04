"""This module contains utility functions for generating an encounter matrix.

Functions
---------
generate_encounter_matrix(session, event_id)
    Generate an encounter matrix for a given event.
"""

from typing import List, Tuple

from fastapi import HTTPException
from sqlmodel import Session


from app.models.enums import FriendshipStatus
from app.services.friendship_services import FriendshipService
from app.services.link_user_event_services import UserEventLinkService


def generate_encounter_matrix(
     session: Session,
     event_id: int) -> Tuple[List[List[str]], List[int]]:
    """
    Generate an encounter matrix for a given event.

    The function takes a SQLModel Session and an event ID as input and returns
    a square matrix that represents the interactions between users during the
    event.
    The matrix is of size len_participant*len_participant, where
    len_participant is the number of users that joined the
    event.

    Parameters
    ----------
    session : Session
        The SQLModel Session to interact with the database.
    event_id : int
        The ID of the event for which to generate the encounter matrix.

    Returns
    -------
    Tuple[List[List[str]], List[int]]
        The encounter matrix and a list mapping matrix indices to user IDs.
    """

    # Initialize services
    user_event_service = UserEventLinkService(session)
    friendship_service = FriendshipService(session)

    # Get the list of participants for the event
    participants = user_event_service.read_participants(event_id)
    len_participant = len(participants)

    # Initialize an len_participant x len_participant matrix filled with
    # "NO_INTERACTION"
    matrix = [
        [
            "NO_INTERACTION" for _ in range(len_participant)
            ] for _ in range(len_participant)
        ]

    # Initialize a list to map matrix indices to user IDs
    id_to_user = [participant.id for participant in participants]

    # Fill the off-diagonal cells based on friendships
    for i in range(len_participant):
        for j in range(i+1, len_participant):
            user1 = participants[i]
            user2 = participants[j]

            try:
                friendship = friendship_service.read_friendship(
                    user1.id,
                    user2.id)
                status = friendship.status

                if status == FriendshipStatus.PENDING:
                    matrix[i][j] = "FR_SEND"
                    matrix[j][i] = "FR_IGNORED"
                elif status == FriendshipStatus.ACCEPTED:
                    matrix[i][j] = "FR_ACCEPTED"
                    matrix[j][i] = "FR_ACCEPTED"
                elif status == FriendshipStatus.DENIED:
                    matrix[i][j] = "FR_SEND"
                    matrix[j][i] = "FR_REFUSED"
                elif status == FriendshipStatus.REPORT:
                    matrix[i][j] = "USER_REPORT"
                    matrix[j][i] = "USER_REPORTED"

            except HTTPException:
                # If no friendship record exists, the matrix value remains
                # "NO_INTERACTION"
                pass

    return matrix, id_to_user
