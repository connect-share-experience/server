from twilio.rest import Client
from app.configs.settings import ExtResourcesSettings

client = Client(ExtResourcesSettings().account_sid,
                ExtResourcesSettings().auth_token)


def send_sms(phone_number: str) -> str:
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
    verification = client.verify \
        .services(ExtResourcesSettings().service_sid) \
        .verifications \
        .create(to=phone_number, channel='sms')

    print(verification.status)
    return verification.status


def check_sms(phone_number: str, code: str) -> str:
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

    return verification_check.status
