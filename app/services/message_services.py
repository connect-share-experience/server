"""This module implements services relating to the messages.

Classes
-------
MessageService
    Intermediate services for messages.
"""
from datetime import datetime as dttime
from typing import List
import shutil

from fastapi import UploadFile
from sqlmodel import Session

from app.configs.settings import StaticSettings
from app.dao.message_dao import MessageDao
from app.models.enums import MessageCategory
from app.models.messages import Message
from app.utils.picture_utils import create_picture_name


class MessageService:
    """Intermediate services for messages.

    Methods
    -------
    create_message(self, message)
        Create a general message
    read_event_messages(self, event_id)
        Read all messages in event inbox
    create_picture_message(self, user_id, event_id, picture)
        Create a message containing a picture, and save said picture.
    delete_message(self, user_id, event_id, datetime)
        Delete a single message.
    """
    def __init__(self, session: Session) -> None:
        self.session = session

    def create_message(self, message: Message) -> Message:
        """Create a general message.

        Parameters
        ----------
        message : Message
            The message to create.

        Returns
        -------
        Message
            The created message
        """
        return MessageDao(self.session).create_message(message)

    def read_event_messages(self, event_id: int) -> List[Message]:
        """Read all messages sent in the event.

        Parameters
        ----------
        event_id : int
            The event whose messages to read.

        Returns
        -------
        List[Message]
            The messages in the event.
        """
        return MessageDao(self.session).read_event_messages(event_id)

    def create_picture_message(self,
                               user_id: int,
                               event_id: int,
                               picture: UploadFile) -> Message:
        """Create a message containing a picture and save that picture.

        Parameters
        ----------
        user_id : int
            The id of the user sending the picture.
        event_id : int
            The id of the event the picture was taken at.
        picture : UploadFile
            The picture to save

        Returns
        -------
        Message
            The created message.
        """
        file_path = f"{StaticSettings().events_dir}/event_{event_id}"

        token_name = create_picture_name(picture)

        with open(f"{file_path}/{token_name}", "wb") as buffer:
            shutil.copyfileobj(picture.file, buffer)
        picture.file.close()

        message = Message(event_id=event_id,
                          user_id=user_id,
                          category=MessageCategory.PICTURE,
                          text=token_name)
        return MessageDao(self.session).create_message(message)

    def delete_message(self,
                       event_id: int,
                       user_id: int,
                       datetime: dttime) -> Message:
        """Delete a single message.

        Parameters
        ----------
        event_id : int
            The id of the event the message is posted in.
        user_id : int
            The id of the user that sent the message
        datetime : dttime
            The time the message was posted.

        Returns
        -------
        Message
            The deleted message.
        """
        return MessageDao(self.session).delete_message(event_id,
                                                       user_id,
                                                       datetime)
