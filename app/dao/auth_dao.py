"""This module implements classes to handle database access for auths.

Classes
-------
AuthDao(session)
    Handle database operations for authistrators.
"""
from typing import List, Optional

from fastapi import HTTPException
from sqlmodel import Session, select

from app.models.auths import Auth


class AuthDao:
    """Data Access Object for authentications.

    This class implements all methods for database operations for auths.
    All methods return an Auth object.

    Methods
    -------
    create_auth(self, auth)
        Add a new auth in database.
    read_auths(self, offset, limit)
        Read auths from database between offset and offset+limit.
    delete_auth(self, phone)
        Delete an auth from database using its phone number.
    read_auth(self, phone)
        Read an auth from database using its phone_number.
    update_code(self, phone)
        Update the verification code of the auth.
    """
    def __init__(self, session: Session):
        self.session = session

    def create_auth(self, auth: Auth) -> Auth:
        """Create a new auth in database.

        Parameters
        ----------
        auth : Auth
            The auth to add to database.

        Returns
        -------
        Auth
            The created auth.
        """
        self.session.add(auth)
        self.session.commit()
        return auth

    def read_auth_by_phone(self, phone: str) -> Auth:
        """Read a single auth using its username.

        Parameters
        ----------
        phone : str
            The phone number of the auth to read.

        Returns
        -------
        Auth
            The auth that was read.

        Raises
        ------
        HTTPException
            Raised when there is no auth with that id.
        """
        statement = select(Auth).where(Auth.phone == phone)
        auth = self.session.exec(statement).one_or_none()
        if auth is None:
            raise HTTPException(status_code=404,
                                detail=f"Auth {phone} not found.")
        return auth

    def read_auths(self, offset: int, limit: int) -> List[Auth]:
        """Read all auths from offset to offset+limit in the table.

        Parameters
        ----------
        offset : int
            Index at which to start reading.
        limit : int
            Number of entries to read.

        Returns
        -------
        List[Auth]
            The auths read from table.
        """
        statement = select(Auth).offset(offset).limit(limit)
        auths = self.session.exec(statement).all()
        return auths

    def delete_auth(self, phone: str) -> Auth:
        """Delete a auth using its phone number.

        Parameters
        ----------
        phone: str
            The phone number of the auth to delete.

        Returns
        -------
        Auth
            The deleted auth.

        Raises
        ------
        HTTPException
            Raised when there is no auth with that id.
        """
        statement = select(Auth).where(Auth.phone == phone)
        auth = self.session.exec(statement).one_or_none()
        if auth is None:
            raise HTTPException(status_code=404,
                                detail=f"Auth with id {phone} not found.")
        self.session.delete(auth)
        self.session.commit()
        return auth

    def update_code(self, phone: str, verify_code: Optional[str]) -> Auth:
        """Delete the verification code of the auth.

        Parameters
        ----------
        phone : str
            The phone number of the auth.

        Returns
        -------
        Auth
            The auth whose verification code was deleted.

        Raises
        ------
        HTTPException
            Raised when the auth does not exist.
        """
        statement = select(Auth).where(Auth.phone == phone)
        old_auth = self.session.exec(statement).one_or_none()
        if old_auth is None:
            raise HTTPException(status_code=404,
                                detail=f"Auth {phone} not found.")
        old_auth.verify_code = verify_code
        self.session.add(old_auth)
        self.session.commit()
        return old_auth
