"""This module implements services relating to the friendships.

Classes
-------
FriendshipService
    Intermediate services for friendships.
"""
from datetime import date as dt

from sqlmodel import Session

from app.dao.friendship_dao import FriendshipDao
from app.models.enums import FriendshipStatus
from app.models.links import Friendship
from app.services.link_user_event_services import UserEventLinkService
from app.dao.event_dao import EventDao


class FriendshipService:
    """Intermediate services for friendships.

    This class implements operations between router and dao layers.

    Methods
    -------
    create_friendship(friendship)
        Create a new friendship.
    get_friendship(user1_id, user2_id)
        Read a single friendship both ways.
    delete_friendship(sender_id, receiver_id)
        Delete a friendship.
    update_friendship_status(sender_id, receiver_id)
        Update a friendship's status.
    """
    def __init__(self, session: Session):
        self.session = session

    def create_friendship(self,
                          sender_id: int,
                          receiver_id: int) -> Friendship:
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
        shared_events = UserEventLinkService(self.session).find_shared_events(
                                                                sender_id,
                                                                receiver_id)
        if not shared_events:
            # Handle the case where there are no shared events if needed
            pass  # TODO : http error to add here
        most_recent_event = sorted(
            shared_events,
            key=lambda x: EventDao(self.session).read_event(
                x.event_id).start_time, reverse=True)[0]
        # TODO avoid the lambda for typing reasons, define the function smh
        friendship = Friendship(invite_sender_id=sender_id,
                                invite_receiver_id=receiver_id,
                                date=dt.today(),
                                status=FriendshipStatus.PENDING,
                                event_id=most_recent_event.event_id)
        return FriendshipDao(self.session).create_friendship(friendship)

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
        """
        return FriendshipDao(self.session).get_friendship(user1_id, user2_id)

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
        new_status : bool
            The status of the relationship. True if accepted, False otherwise.

        Returns
        -------
        Friendship
            The updated friendship.
        """
        return (FriendshipDao(self.session)
                .update_friendship_status(sender_id, receiver_id, new_status))

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
        """
        return FriendshipDao(self.session).delete_friendship(sender_id,
                                                             receiver_id)
