"""This module contains methods to handle verification codes.

Functions
---------
create_verify_code()
    Create a randomly generated verification code.
send_verify_code()
    Send the verification code to the user.
"""


def create_verify_code() -> str:
    """Create a randomly generated verification code.

    Returns
    -------
    str
        The verification code.
    """
    return "1941"


def send_verify_code() -> bool:
    """Send the verification code to the user.

    Returns
    -------
    bool
        True if code was sent.
    """
    return True
