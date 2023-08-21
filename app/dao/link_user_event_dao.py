"""This module implements classes to handle database access for user-event.

Classes
-------
UserEventLinkDao(session)
    Data access for links between users and events.
"""
from typing import List

from fastapi import HTTPException
from sqlmodel import Session, select

from app.models.links import UserEventLink


class UserEventLinkDao:
    """Data access for links between users and events.

    Methods
    -------
    create_user_event_link(link)
        Create a new link.
    read_user_event_link(user_id, event_id)
        Read a single link.
    read_user_events(user_id)
        Read all links of a user.
    read_event_users(event_id)
        Read all links of an event.
    update_user_event_link(user_id, event_id, new_link)
        Update a link.
    delete_user_event_link(user_id, event_id)
        Delete a link.
    """
    def __init__(self, session: Session):
        self.session = session

    def create_user_event_link(self, link: UserEventLink) -> UserEventLink:
        """Create a new link between a user and an event.

        Parameters
        ----------
        link : UserEventLink
            The link to create.

        Returns
        -------
        UserEventLink
            The created link.
        """
        self.session.add(link)
        self.session.commit()
        return link

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

        Raises
        ------
        HTTPException
            Raised when the link does not exist.
        """
        statement = (select(UserEventLink)
                     .where(UserEventLink.user_id == user_id)
                     .where(UserEventLink.event_id == event_id))
        link = self.session.exec(statement).one_or_none()
        if link is None:
            raise HTTPException(status_code=404,
                                detail="User-Event Link not found.")
        return link

    def read_all_user_events(self, user_id: int) -> List[UserEventLink]:
        """Get all links for a user.

        Parameters
        ----------
        user_id : int
            The id of the user to look for.

        Returns
        -------
        List[UserEventLink]
            All links of the user.

        Raises
        ------
        HTTPException
            Raised when no links are found.
        """
        statement = (select(UserEventLink)
                     .where(UserEventLink.user_id == user_id))
        links = self.session.exec(statement).all()
        if links is None:
            raise HTTPException(
                status_code=404,
                detail=f"User with id {user_id} has no events.")
        return links

    def read_all_event_users(self, event_id: int) -> List[UserEventLink]:
        """Get all links for an event.

        Parameters
        ----------
        event_id : int
            The id of the event to look for.

        Returns
        -------
        List[UserEventLink]
            All links for the event.

        Raises
        ------
        HTTPException
            Raised when no link is found.
        """
        statement = (select(UserEventLink)
                     .where(UserEventLink.event_id == event_id))
        links = self.session.exec(statement).all()
        if links is None:
            raise HTTPException(
                status_code=404,
                detail=f"Event with id {event_id} has no users.")
        return links

    def update_user_event_link(self,
                               user_id: int,
                               event_id: int,
                               new_link: UserEventLink) -> UserEventLink:
        """Update an existing user-event link.

        Parameters
        ----------
        user_id : int
            The id of the user in the link.
        event_id : int
            The id of the event in the link.
        new_link : UserEventLink
            The new link data to update.

        Returns
        -------
        UserEventLink
            The updated link.
        """
        old_link = self.read_user_event_link(user_id, event_id)
        new_data = new_link.dict(exclude_unset=True)
        for key, value in new_data.items():
            setattr(old_link, key, value)

        self.session.add(old_link)
        self.session.commit()
        self.session.refresh(old_link)
        return old_link

    def delete_user_event_link(self,
                               user_id: int,
                               event_id: int) -> UserEventLink:
        """Delete a link between a user and an event.

        Parameters
        ----------
        user_id : int
            The id of the user in the link.
        event_id : int
            The id of the event in the link.

        Returns
        -------
        UserEventLink
            The deleted link.
        """
        link = self.read_user_event_link(user_id, event_id)
        self.session.delete(link)
        self.session.commit()
        return link
