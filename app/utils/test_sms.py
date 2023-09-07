from twilio.rest import Client

phone_number = '+33661477529'
account_sid = 'AC6d3dee87d0dd1a4b79c16e055ed71e7b'
verify_sid = 'VA906e4335fa2838b5f60f6401c2bc5b29'
auth_token = '9b039e90ee0ec5627144e6ae58760a00'

client = Client(account_sid, auth_token)

otp_verification = client.verify.v2.services(verify_sid).verifications.create(
    to=phone_number, channel='sms'
    )

print(otp_verification.status)

otp_code = input('Enter OTP: ')

otp_check = client.verify.services(verify_sid).verification_checks.create(
    to=phone_number, code=otp_code
    )

print(otp_check.status)
