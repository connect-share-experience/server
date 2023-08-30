"""This module implements all the models used for many-to-many relations.

Classes
-------
Friendship(SQLModel, table=True)
    Link for the relationships between users.
"""
from datetime import date as dt
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

from app.models.enums import UserEventStatus, FriendshipStatus

from app.models.users import User
from app.models.events import Event


class Friendship(SQLModel, table=True):
    """Implements the link for the many-to-many relationship between Users.

    This implements a friend list.

    Attributes
    ----------
    user_id1: Optional[int]
        id of the first User of the friendship.
    user_id2: Optional[int]
        id of the second User of the friendship.
    """
    invite_sender_id: Optional[int] = Field(default=None,
                                            foreign_key="user.id",
                                            primary_key=True)
    invite_receiver_id: Optional[int] = Field(default=None,
                                              foreign_key="user.id",
                                              primary_key=True)
<<<<<<< HEAD
    event_id: Optional[int] = Field(default=None,
                                    foreign_key="event.id")
    date: date
    accepted: bool
=======
    date: dt
    status: FriendshipStatus
>>>>>>> d177594ff4a9424a9b97199f4b8121c43f3319fd
    invite_sender: "User" = Relationship(
        back_populates="sent_invites",
        sa_relationship_kwargs={
            "foreign_keys": "Friendship.invite_sender_id"})
    invite_receiver: "User" = Relationship(
        back_populates="received_invites",
        sa_relationship_kwargs={
            "foreign_keys": "Friendship.invite_receiver_id"})
    event: "Event" = Relationship(
        back_populates="shared_event",
        sa_relationship_kwargs={
            "foreign_keys": "Friendship.event_id"})


class UserEventLink(SQLModel, table=True):
    """Link between Users and Events.

    This implements the many to many relationship between those tables: a
    User attends multiple Events and an Event has multiple attendees.

    Attributes
    ----------
    profile_id: Optional[int]
        id of the User that attended.
    event_id: Optional[int]
        id of the event attended.
    status: UserEventStatus
        The status of the link, i.e it the user created, attends, etc.
    text: Optional[str]
        Used when a message is sent by a user that wants to join an event.
    """
    user_id: Optional[int] = Field(default=None,
                                   foreign_key="user.id",
                                   primary_key=True)
    event_id: Optional[int] = Field(default=None,
                                    foreign_key="event.id",
                                    primary_key=True)
    status: UserEventStatus
    text: Optional[str]

    user: "User" = Relationship(back_populates="event_links")
    event: "Event" = Relationship(back_populates="user_links")
