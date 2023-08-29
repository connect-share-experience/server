"""This module implements classes to handle database access for friendships.

Classes
-------
FrienshipDao(session)
    Data access for friendships.
"""
from typing import List

from fastapi import HTTPException
from sqlmodel import Session, select

from app.models.enums import FriendshipStatus
from app.models.links import Friendship


class FriendshipDao:
    """Data access for frienships.

    This class implements all methods for database operations for frienships.
    All methods return a Friendship object.

    Methods
    -------
    create_friendship(friendship)
        Create a new friendship.
    read_friendship(sender_id, receiver_id)
        Read a single friendship.
    get_friendship(user1_id, user2_id)
        Read a single friendship both ways.
    read_friendships(offset, limit)
        Read friendships between offset and offset+limit.
    delete_friendship(sender_id, receiver_id)
        Delete a friendship.
    update_friendship_status(sender_id, receiver_id)
        Update a friendship's status.
    """
    def __init__(self, session: Session):
        self.session = session

    def create_friendship(self, friendship: Friendship) -> Friendship:
        """Create a frienship in database.

        Parameters
        ----------
        friendship : Friendship
            The new friendship to create.

        Returns
        -------
        Friendship
            The friendship created.
        """
        self.session.add(friendship)
        self.session.commit()
        return friendship

    def read_friendship(self,
                        sender_id: int,
                        receiver_id: int) -> Friendship:
        """Read a single friendship.

        Parameters
        ----------
        sender_id : int
            The id of the user that sent the invite.
        receiver_id : int
            The id of the user that received the invite.

        Returns
        -------
        Friendship
            The friendship that was read.

        Raises
        ------
        HTTPException
            Raised when no such friendship was found.
        """
        statement = (select(Friendship)
                     .where(Friendship.invite_receiver_id == receiver_id)
                     .where(Friendship.invite_sender_id == sender_id))
        friendship = self.session.exec(statement).one_or_none()
        if friendship is None:
            raise HTTPException(status_code=404,
                                detail="Friendship not found.")
        return friendship

    def get_friendship(self,
                       user1_id: int,
                       user2_id: int) -> Friendship:
        """Read a frienship both ways.

        In this method, we search for the frienship without specifying wich
        user is the sender or receiver of the invite.

        Parameters
        ----------
        user1_id : int
            One of the users of the friendhip.
        user2_id : int
            The other user of the friendship.

        Returns
        -------
        Friendship
            The friendship that was read.

        Raises
        ------
        HTTPException
            Raised when no frienship between those users was found.
        """
        statement = f"""SELECT *
                     FROM friendship
                     WHERE (invite_receiver_id = {user1_id}
                            AND invite_sender_id == {user2_id})
                     OR (invite_receiver_id = {user2_id}
                            AND invite_sender_id == {user1_id});"""
        temp = self.session.execute(statement)  # type: ignore
        friendship = temp.one_or_none()
        if isinstance(friendship, Friendship):
            return friendship
        raise HTTPException(status_code=401, detail="Friendship not found.")

    def read_friendships(self, offset: int, limit: int) -> List[Friendship]:
        """Read several friendships.

        Parameters
        ----------
        offset : int
            Index to start reading at.
        limit : int
            Number of friendships to read.

        Returns
        -------
        List[Friendship]
            The read friendships.
        """
        statement = select(Friendship).offset(offset).limit(limit)
        friendships = self.session.exec(statement).all()
        return friendships

    def delete_friendship(self,
                          sender_id: int,
                          receiver_id: int) -> Friendship:
        """Delete a friendship.

        Parameters
        ----------
        sender_id : int
            The id of the user that sent the friendship invite.
        receiver_id : int
            The id of the user that received the frienship invite.

        Returns
        -------
        Friendship
            The deleted friendship.

        Raises
        ------
        HTTPException
            Raised when no such friendship is found.
        """
        statement = (select(Friendship)
                     .where(Friendship.invite_receiver_id == receiver_id)
                     .where(Friendship.invite_sender_id == sender_id))
        friendship = self.session.exec(statement).one_or_none()
        if friendship is None:
            raise HTTPException(status_code=401,
                                detail="Friendship not found.")
        self.session.delete(friendship)
        self.session.commit()
        return friendship

    def update_friendship_status(self,
                                 sender_id: int,
                                 receiver_id: int,
                                 new_status: FriendshipStatus) -> Friendship:
        """Update a friendship status.

        Parameters
        ----------
        sender_id : int
            The id of the user that sent the friendship invite.
        receiver_id : int
            The id of the user that reveived the friendship invite.
        new_status : FriendshipStatus
            The status of the relationship.

        Returns
        -------
        Friendship
            The updated friendship.

        Raises
        ------
        HTTPException
            Raised when no such friendship is found.
        """
        statement = (select(Friendship)
                     .where(Friendship.invite_receiver_id == receiver_id)
                     .where(Friendship.invite_sender_id == sender_id))
        friendship = self.session.exec(statement).one_or_none()
        if friendship is None:
            raise HTTPException(status_code=401,
                                detail="Friendship not found.")
        friendship.status = new_status
        self.session.add(friendship)
        self.session.commit()
        return friendship
