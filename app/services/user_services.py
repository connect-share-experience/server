"""This module implements services relating to the users.

Classes
-------
UserService
    Intermediate services for users.
"""
import shutil
from typing import List

from fastapi import UploadFile
from sqlmodel import Session

from app.configs.settings import StaticSettings
from app.dao.auth_dao import AuthDao
from app.dao.user_dao import UserDao
from app.models.auths import Auth
from app.models.enums import FriendshipStatus
from app.models.users import User, UserCreate, UserUpdate
from app.utils.picture_utils import create_picture_name


class UserService:
    """Intermediate services for users.

    This class implements operations between router and dao layers.

    Methods
    -------
    create_user(self, user)
        Add a new user in database.
    read_user(self, user_id)
        Read a user from database using its id.
    read_users(self, offset, limit)
        Read users from database between offset and offset+limit.
    update_user(self, user_id, new_user)
        Update a user in database with new user data.
    delete_user(self, user_id)
        Delete a user from database using its id.
    read_user_sent_invites(self, user_id)
        Read a user's sent invites recepients.
    read_user_received_invites(self, user_id)
        Read a user's received invites senders.
    read_friends(self, user_id)
        Read all friends of a user.
    """

    def __init__(self, session: Session):
        self.session = session

    def create_user(self, user: UserCreate) -> User:
        """Create a new user in database.

        Parameters
        ----------
        user : UserCreate
            The user to add to database.

        Returns
        -------
        User
            The created user.
        """
        new_user = User.parse_obj(user)
        db_user = UserDao(self.session).create_user(new_user)
        new_auth = Auth(phone=db_user.phone)
        AuthDao(self.session).create_auth(new_auth)
        return db_user

    def read_user(self, user_id: int) -> User:
        """Read a single user using its id.

        Parameters
        ----------
        user_id : int
            The id of the user to read.

        Returns
        -------
        User
            The user that was read.
        """
        return UserDao(self.session).read_user(user_id)

    def read_user_by_phone(self, phone: str) -> User:
        """Read a user using its phone number.

        Parameters
        ----------
        phone : str
            The phone number of the user to read.

        Returns
        -------
        User
            The user that was read.

        Raises
        ------
        HTTPException
            Raised when the user cannot be found.
        """
        return UserDao(self.session).read_user_by_phone(phone)

    def read_users(self, offset: int, limit: int) -> List[User]:
        """Read all users from offset to offset+limit in the table.

        Parameters
        ----------
        offset : int
            Index at which to start reading.
        limit : int
            Number of entries to read.

        Returns
        -------
        List[User]
            The users read from table.
        """
        return UserDao(self.session).read_users(offset, limit)

    def update_user(self, user_id: int, user: UserUpdate) -> User:
        """Update a user with chosen id with new user data.

        Parameters
        ----------
        user_id : int
            The id of the user to update.
        new_user : User
            The new user whose data to use for the update.

        Returns
        -------
        User
            The updated user.
        """
        return UserDao(self.session).update_user(user_id, user)

    def delete_user(self, user_id: int) -> User:
        """Delete a user using its id.

        Parameters
        ----------
        user_id : int
            The id of the user to delete.

        Returns
        -------
        User
            The deleted user.
        """
        user = UserDao(self.session).read_user(user_id)
        AuthDao(self.session).delete_auth(user.phone)
        return UserDao(self.session).delete_user(user_id)

    def read_user_sent_invites(self, user_id: int) -> List[User]:
        """Read a user's sent invites recepients.

        Parameters
        ----------
        user_id : int
            The id of the user whose invites to read.

        Returns
        -------
        List[User]
            The users that the invites were sent to.
        """
        user = UserDao(self.session).read_user(user_id)
        users = []
        for invite in user.sent_invites:
            if invite.status == FriendshipStatus.PENDING:
                users.append(invite.invite_receiver)
        return users

    def read_user_received_invites(self, user_id: int) -> List[User]:
        """Read a user's received invites senders.

        Parameters
        ----------
        user_id : int
            The id of the user whose invites to read.

        Returns
        -------
        List[User]
            The users that the invites were received from.
        """
        user = UserDao(self.session).read_user(user_id)
        users = []
        for invite in user.received_invites:
            if invite.status == FriendshipStatus.PENDING:
                users.append(invite.invite_sender)
        return users

    def read_friends(self, user_id: int) -> List[User]:
        """Read all friends of a user.

        Parameters
        ----------
        user_id : int
            The id of the user whose friends to read.

        Returns
        -------
        List[User]
            The friends of said user.
        """
        user = UserDao(self.session).read_user(user_id)
        friends = []
        for invite in user.sent_invites:
            if invite.status == FriendshipStatus.ACCEPTED:
                friends.append(invite.invite_receiver)
        for invite in user.received_invites:
            if invite.status == FriendshipStatus.ACCEPTED:
                friends.append(invite.invite_sender)
        return friends

    def update_picture(self, user_id: int, picture: UploadFile) -> User:
        """Update a user picture.

        Parameters
        ----------
        user_id : int
            The id of the user to update
        picture : UploadFile
            The picture file.

        Returns
        -------
        User
            The updated user.

        Raises
        ------
        HTTPException
            Raised when the picture format is not allowed.
        """
        file_path = StaticSettings().user_page_pic_dir

        token_name = create_picture_name(picture)

        user = UserDao(self.session).update_picture(user_id, token_name)

        with open(f"{file_path}/{user.picture}", "wb") as buffer:
            shutil.copyfileobj(picture.file, buffer)
        picture.file.close()

        return user
