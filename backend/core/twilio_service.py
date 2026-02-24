from twilio.rest import Client
import os


TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_SMS_FROM = os.getenv("TWILIO_SMS_FROM")
# WHATSAPP_SANDBOX_FROM = "whatsapp:+14155238886"


# def send_otp_whatsapp(to_number: str, otp: str) -> str:
#     """
#     Sends OTP via Twilio WhatsApp Sandbox.
#     to_number must be in E.164 format (+91XXXXXXXXXX).
#     """

#     if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
#         raise ValueError("Twilio credentials missing in environment")

#     client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

#     to = f"whatsapp:{to_number}"

#     message = client.messages.create(
#         body=f"Your OTP is {otp}.",
#         from_=WHATSAPP_SANDBOX_FROM,
#         to=to,
#     )

#     return message.sid
def send_otp_sms(to_number: str, otp: str) -> str:
    
    if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
        raise RuntimeError("Twilio credentials missing (TWILIO_ACCOUNT_SID/TWILIO_AUTH_TOKEN)")

    if not TWILIO_SMS_FROM:
        raise RuntimeError("Twilio SMS From number missing (TWILIO_SMS_FROM)")

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    message = client.messages.create(
        body=f"Your OTP is {otp}. Valid for {5} minutes.",
        from_=TWILIO_SMS_FROM,
        to=to_number,
    )
    return message.sid