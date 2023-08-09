"""This module implements all models used for authentication tokens."""
from pydantic import BaseModel, validator

from app.utils.validators import check_valid_phone


class Token(BaseModel):
    """Model reprensenting the tokens used to authenticate admins and users."""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Model carrying the data found when decoding tokens."""
    phone: str

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
