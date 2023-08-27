"""This module implements classes to handle database access for users.

Classes
-------
UserDao(session)
    Data access for users.
"""
from typing import List

from fastapi import HTTPException
from sqlmodel import Session, select

from app.models.users import User, UserUpdate


class UserDao:
    """Data Access for users.

    This class implements all methods for database operations for users.
    All methods return a User object.

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
    read_user_by_phone(self, phone)
        Read a single user using its phone_number.
    """
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, user: User) -> User:
        """Create a new User in DB.

        Parameters
        ----------
        user : User
            The user to add to database.

        Returns
        -------
        User
            The created user.
        """
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

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

        Raises
        ------
        HTTPException
            Raised when there is no user with that id.
        """
        user = self.session.get(User, user_id)
        if user is None:
            raise HTTPException(status_code=404,
                                detail=f"User with id {user_id} not found.")
        return user

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
        statement = select(User).where(User.phone == phone)
        user = self.session.exec(statement).one_or_none()
        if user is None:
            raise HTTPException(status_code=404,
                                detail=f"User with phone {phone} not found.")
        return user

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
        statement = select(User).offset(offset).limit(limit)
        users = self.session.exec(statement).all()
        return users

    def update_user(self, user_id: int, new_user: UserUpdate) -> User:
        """Update a user with chosen id with new user data.

        Parameters
        ----------
        user_id : int
            id of the user to update.
        new_user : User
            The new user whose data to use for the update.

        Returns
        -------
        User
            The updated user.

        Raises
        ------
        HTTPException
            Raised when there is no user with that id.
        """
        old_user = self.session.get(User, user_id)
        if not old_user:
            raise HTTPException(status_code=404,
                                detail=f"User with id {user_id} not found.")
        new_data = new_user.dict(exclude_unset=True)
        for key, value in new_data.items():
            setattr(old_user, key, value)

        self.session.add(old_user)
        self.session.commit()
        self.session.refresh(old_user)
        return old_user

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

        Raises
        ------
        HTTPException
            Raised when there is no user with that id.
        """
        user = self.session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404,
                                detail=f"User with id {user_id} not found.")
        self.session.delete(user)
        self.session.commit()
        return user

    def update_picture(self, user_id: int, picture_name: str) -> User:
        """Update the profile picture name of the user in database.

        Parameters
        ----------
        user_id : int
            The id of the user to update.
        picture_name : str
            Identifier of the picture.

        Returns
        -------
        User
            The updated user.

        Raises
        ------
        HTTPException
            Raised when no user with such id is found.
        """
        old_user = self.session.get(User, user_id)
        if not old_user:
            raise HTTPException(status_code=404,
                                detail=f"User with id {user_id} not found.")
        if old_user.picture != "default_user_pic.png":
            old_user.picture = picture_name
            self.session.add(old_user)
            self.session.commit()
            self.session.refresh(old_user)
        return old_user
