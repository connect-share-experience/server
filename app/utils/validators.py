"""This module contains validators used through several models in the app.

Functions
---------
check_valid_phone(value)
    Verify that the input value is a valid phone number.
"""
import phonenumbers as pn
from fastapi import HTTPException


def check_valid_phone(value: str) -> str:
    """Verify that the input value is a valid phone number.

    Parameters
    ----------
    value : str
        The input value to check.

    Returns
    -------
    str
        The string representing a phone number.

    Raises
    ------
    HTTPException
        Raised when the string is not a valid phone number
    """
    # TODO Might wanna use a custom exception instead.
    invalid_exc = HTTPException(
        status_code=422,
        detail=f"{value} is not a valid phone number.")
    try:
        phone = pn.parse(value)
        if pn.is_valid_number(phone):
            return value
        raise invalid_exc
    except pn.NumberParseException as exc:
        raise invalid_exc from exc
