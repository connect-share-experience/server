"""This module implements services relating to the user-event links.

Classes
-------
UserEventLinkService
    Intermediate services for links between users and events.
"""
from typing import List
from sqlmodel import Session

from app.dao.link_user_event_dao import UserEventLinkDao
from app.models.enums import UserEventStatus
from app.models.links import UserEventLink
from app.models.users import User


class UserEventLinkService:
    """Intermediate services for links between users and events.

    Methods
    -------
    create_user_event_link(self, link)
        Create a user-event link
    read_user_event_link(self, user_id, event_id)
        Read a single user-event link
    read_participants(self, event_id)
        Read all participants of the event
    is_participant_or_creator(self, user_id, event_id)
        Verify that the user takes part in the event
    """
    def __init__(self, session: Session):
        self.session = session

    def create_user_event_link(self, link: UserEventLink) -> UserEventLink:
        """Create a link between user and event.

        Parameters
        ----------
        link : UserEventLink
            The link to create.

        Returns
        -------
        UserEventLink
            The created link.
        """
        return UserEventLinkDao(self.session).create_user_event_link(link)

    def read_user_event_link(self,
                             user_id: int,
                             event_id: int) -> UserEventLink:
        """Read a single link between a user and an event.

        Parameters
        ----------
        user_id : int
            The id of the user in the link.
        event_id : int
            The id of the event in the link.

        Returns
        -------
        UserEventLink
            The link that was read.
        """
        return UserEventLinkDao(self.session).read_user_event_link(user_id,
                                                                   event_id)

    def read_participants(self, event_id: int) -> List[User]:
        """Read all users that participate in the event.

        Parameters
        ----------
        event_id : int
            The id of the event that the users are in.

        Returns
        -------
        List[UserEventLink]
            The list of users that participate in the event.
        """
        links = UserEventLinkDao(self.session).read_all_event_users(event_id)
        participants: List[User] = []
        for link in links:
            if link.status in [UserEventStatus.CREATOR,
                               UserEventStatus.ATTENDS]:
                participants.append(link.user)
        return participants

    def update_status(self,
                      event_id: int,
                      user_id: int,
                      new_status: UserEventStatus) -> UserEventLink:
        """Update the user-event link status.

        Parameters
        ----------
        event_id : int
            The id of the event in the link.
        user_id : int
            The id of the user in the link.
        new_status : UserEventStatus
            The new status to give the relationship.

        Returns
        -------
        UserEventLink
            The updated link.
        """
        link = UserEventLinkDao(self.session).read_user_event_link(user_id,
                                                                   event_id)
        link.status = new_status
        self.session.add(link)
        self.session.commit()
        return link

    def is_participant(self, user_id: int, event_id: int) -> bool:
        """Verifies weather the user attends or creates the event.

        Parameters
        ----------
        user_id : int
            The id of the user to check.
        event_id : int
            The if of the event to check.

        Returns
        -------
        bool
            True if the user is participant or creator, False otherwise.
        """
        link = UserEventLinkDao(self.session).read_user_event_link(user_id,
                                                                   event_id)
        if link.status in [UserEventStatus.CREATOR, UserEventStatus.ATTENDS]:
            return True
        return False

    def is_creator(self, user_id: int, event_id: int) -> bool:
        """Verify whether the user created the event.

        Parameters
        ----------
        user_id : int
            The id of the user to check.
        event_id : int
            The id of the event to check.

        Returns
        -------
        bool
            True if the user created the event. False otherwise.
        """
        link = UserEventLinkDao(self.session).read_user_event_link(user_id,
                                                                   event_id)
        if link.status == UserEventStatus.CREATOR:
            return True
        return False
    
    def find_shared_events(self,
                           user_id1: int,
                           user_id2: int) -> List[UserEventLink]:
        """Find events that are attended by both users.

        Parameters
        ----------
        user_id1 : int
            The id of the first user.
        user_id2 : int
            The id of the second user.

        Returns
        -------
        List[UserEventLink]
            The list of shared events.
        """
        # Find all events for the first user
        events1 = UserEventLinkDao(self.session).read_all_user_events(user_id1)
        # Find all events for the second user
        events2 = UserEventLinkDao(self.session).read_all_user_events(user_id2)
        shared_events = list()
        # Find the intersection of both event lists
        for event1 in events1:
            for event2 in events2:
                if event1.event_id == event2.event_id:
                    shared_events.append(event1)
        return shared_events
