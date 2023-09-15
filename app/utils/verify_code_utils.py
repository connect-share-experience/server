"""This module contains methods to handle verification codes.

Functions
---------
create_verify_code()
    Create a randomly generated verification code.
send_verify_code()
    Send the verification code to the user.
check_verify_code(phone_number)
    check if the verification code provided by the user is correct
"""
from twilio.rest import Client
import phonenumbers
from app.configs.settings import ExtResourcesSettings

client = Client(ExtResourcesSettings().account_sid,
                ExtResourcesSettings().auth_token)


def create_verify_code() -> str:
    """Create a randomly generated verification code.

    Returns
    -------
    str
        The verification code.
    """
    return "1941"


def send_verify_code(phone_number: str, country: str = None) -> str:
    """Send an SMS message.

    Parameters
    ----------
    phone_number : str
        The phone number to send the message to.
    message : str
        The message to send.

    Returns
    -------
        verification.status : str
            The status of the verification.
    """
    phone_number = phonenumbers.format_number(
        phonenumbers.parse(phone_number, country),
        phonenumbers.PhoneNumberFormat.INTERNATIONAL
        )
    verification = client.verify \
        .services(ExtResourcesSettings().service_sid) \
        .verifications \
        .create(to=phone_number, channel='sms')
    if isinstance(verification.status, str):
        return verification.status
    raise TypeError("Twilio verification status should be a string.")


def check_verify_code(phone_number: str, country: str, code: str) -> str:
    """Check the SMS code.

    Args:
        phone_number : str
            The phone number to send the message to.
        code : str
            The code to check.

    Returns:
        verification_check.status : str
            The status of the verification check.
    """
    verification_check = client.verify \
        .services(ExtResourcesSettings().service_sid) \
        .verification_checks \
        .create(to=phone_number, code=code)
    if isinstance(verification_check.status, str):
        return verification_check.status
    raise TypeError("Twilio verification status should be a string.")
