"""This module implements classes used to handle user authentication.

Classes
-------
Auth(SQLModel, table=True)
    Implements the authentication data in database.
"""
from typing import Optional

from pydantic import validator
from sqlmodel import Field, SQLModel, UniqueConstraint

from app.utils.validators import check_valid_phone


class Auth(SQLModel, table=True):
    """This class implements authentication data inside the database.

    Attributes
    ----------
    phone: str
        The phone used to authenticate. Primary key. Custom validator.
    verify_code: str
        Code used to authenticate the user.
    """
    __table_args__ = (UniqueConstraint("phone"),)
    phone: str = Field(foreign_key='user.phone', primary_key=True)
    verify_code: Optional[str] = Field(default=None)

    @classmethod
    @validator("phone")
    def phone_validator(cls, value: str) -> str:
        """Verify that the input value is a valid phone number.

        Parameters
        ----------
        value : str
            The input value to check.

        Returns
        -------
        str
            The string representing a phone number.
        """
        return check_valid_phone(value)
