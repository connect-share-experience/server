"""This module implements classes to handle database access for messages.

Classes
-------
MessageDao(session)
    Data access for messages.
"""
from datetime import datetime as dttime
from typing import List

from fastapi import HTTPException
from sqlmodel import Session, select

from app.models.messages import Message


class MessageDao:
    """Data Access for users.

    This class implements all methods for database operations for users.
    All methods return a User object.

    Methods
    -------
    create_message(self, message)
        Create a message in database
    read_message(self, user_id, event_id, datetime)
        Read a single message
    read_user_messages(self, user_id)
        Read all messages sent by a user
    read_event_messages(self, event_id)
        Read all messages sent in an event
    read_user_messages_in_event(self, event_id, user_id)
        Read all messages sent by a user in an event
    delete_message(self, event_id, user_id, datetime)
        Delete a message from database
    """
    def __init__(self, session: Session):
        self.session = session

    def create_message(self, message: Message) -> Message:
        """Create a message in database.

        Parameters
        ----------
        message : Message
            The message to create.

        Returns
        -------
        Message
            The created message.
        """
        self.session.add(message)
        self.session.commit()
        return message

    def read_message(self,
                     event_id: int,
                     user_id: int,
                     datetime: dttime) -> Message:
        """Read a single message.

        Parameters
        ----------
        event_id : int
            The id of the event the message was sent in.
        user_id : int
            The id of the user who sent the message.
        datetime : dttime
            The time the message was sent.

        Returns
        -------
        Message
            The read message.

        Raises
        ------
        HTTPException
            Raised when no such message is found.
        """
        statement = (select(Message)
                     .where(Message.event_id == event_id)
                     .where(Message.user_id == user_id)
                     .where(Message.datetime == datetime))
        message = self.session.exec(statement).one_or_none()
        if message is None:
            raise HTTPException(status_code=404,
                                detail="Message not found")
        return message

    def read_user_messages(self, user_id: int) -> List[Message]:
        """Read all messages sent by a user in every events.

        Parameters
        ----------
        user_id : int
            The user who sent the messages.

        Returns
        -------
        List[Message]
            All the messages sent by that user.
        """
        statement = select(Message).where(Message.user_id == user_id)
        messages = self.session.exec(statement).all()
        return messages

    def read_event_messages(self, event_id: int) -> List[Message]:
        """Read all messages in an event.

        Parameters
        ----------
        event_id : int
            The event the messages are in.

        Returns
        -------
        List[Message]
            All messages in event.
        """
        statement = select(Message).where(Message.event_id == event_id)
        messages = self.session.exec(statement).all()
        return messages

    def read_user_messages_in_event(self,
                                    event_id: int,
                                    user_id: int) -> List[Message]:
        """Read all messages sent by a user in an event.

        Parameters
        ----------
        event_id : int
            The id of the event the message is in.
        user_id : int
            The id of the user who sent the message.

        Returns
        -------
        List[Message]
            The messages sent by the user in that event.
        """
        statement = (select(Message)
                     .where(Message.event_id == event_id)
                     .where(Message.user_id == user_id))
        messages = self.session.exec(statement).all()
        return messages

    def delete_message(self,
                       event_id: int,
                       user_id: int,
                       datetime: dttime) -> Message:
        """Delete message in database.

        Parameters
        ----------
        event_id : int
            The id of the event the message is in.
        user_id : int
            The id of the user that sent the message.
        datetime : dttime
            The time the message was sent.

        Returns
        -------
        Message
            The deleted message.
        """
        message = self.read_message(event_id, user_id, datetime)
        self.session.delete(message)
        self.session.commit()
        return message
