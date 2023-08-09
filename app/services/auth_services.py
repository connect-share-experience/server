"""This module implements classes used for services using auths.

Here are created several operations used in handling auths betwenn the API
endpoints and the database.

Classes
-------
AuthService
    Intermediate services for auths.
"""
from typing import List, Optional

from sqlmodel import Session

from app.dao.auth_dao import AuthDao
from app.models.auths import Auth


class AuthService:
    """Intermediate services for auths.

    This class implements operations between router and dao layers.

    Methods
    -------
    create_auth(self, auth)
        Add a new auth in database.
    read_auths(self, offset, limit)
        Read auths from database between offset and offset+limit.
    delete_auth(self, phone)
        Delete an auth from database using its phone number.
    read_auth(self, phone)
        Read an auth from database using its phone number.
    """
    def __init__(self, session: Session):
        self.session = session

    def read_auths(self, offset: int, limit: int) -> List[Auth]:
        """Read all auths from offset to offset+limit.

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
        return AuthDao(self.session).read_auths(offset, limit)

    def delete_auth(self, phone: str) -> Auth:
        """Delete a auth using its phone number.

        Parameters
        ----------
        phone : str
            The phone number of the auth to delete.

        Returns
        -------
        Auth
            The deleted auth.
        """
        return AuthDao(self.session).delete_auth(phone)

    def read_auth_by_phone(self, phone: str) -> Auth:
        """Read a single auth using its phone number.

        Parameters
        ----------
        phone : str
            The phone number of the auth to read.

        Returns
        -------
        Auth
            The auth that was read.
        """
        return AuthDao(self.session).read_auth_by_phone(phone)

    def update_code(self,
                    phone: str,
                    verify_code: Optional[str] = None) -> Auth:
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
        return AuthDao(self.session).update_code(phone, verify_code)
