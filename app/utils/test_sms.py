from twilio.rest import Client
phone = '+33661477529'
account_sid = 'AC6d3dee87d0dd1a4b79c16e055ed71e7b'
verify_sid = 'VA906e4335fa2838b5f60f6401c2bc5b29'
auth_token = '7d7a08760571d5b7878c5b6ee325b1b8'

client = Client(account_sid, auth_token)


def create_verify_code() -> str:
    """Create a randomly generated verification code.

    Returns
    -------
    str
        The verification code.
    """
    return "1941"


def send_verify_code(phone_number: str) -> str:
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
        .v2 \
        .services('VA906e4335fa2838b5f60f6401c2bc5b29') \
        .verifications \
        .create(to=phone_number, channel='sms')
    if isinstance(verification.status, str):
        return verification.status
    raise TypeError("Twilio verification status should be a string.")


def check_verify_code(phone_number: str, code: str) -> str:
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
        .v2 \
        .services(verify_sid) \
        .verification_checks \
        .create(to=phone_number, code=code)
    if isinstance(verification_check.status, str):
        return verification_check.status
    raise TypeError("Twilio verification status should be a string.")

if __name__ == "__main__":
    otp_verification = send_verify_code(phone)

    print(otp_verification)

    otp_code = input('Enter OTP: ')

    otp_check = check_verify_code(phone, otp_code)

    print(otp_check)
