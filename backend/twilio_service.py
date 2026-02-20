from twilio.rest import Client
import os

# def send_otp_sms(account_sid: str, auth_token: str, from_number: str, to_number: str, otp: str) -> str:
#     """
#     Twilio ko call karke SMS bhejta hai.
#     Returns: message SID (Twilio message id)
#     """
#     client = Client(account_sid, auth_token)

#     msg = client.messages.create(
#         body=f"Your OTP is {otp}. It expires in 5 minutes.",
#         from_=from_number,
#         to=to_number
#     )
#     return msg.sid

# from twilio.rest import Client


TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
WHATSAPP_SANDBOX_FROM = os.getenv("TWILIO_WHATSAPP_FROM")
# WHATSAPP_SANDBOX_FROM = "whatsapp:+14155238886"


def send_otp_whatsapp(to_number: str, otp: str) -> str:
    """
    Sends OTP via Twilio WhatsApp Sandbox.
    to_number must be in E.164 format (+91XXXXXXXXXX).
    """

    if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
        raise ValueError("Twilio credentials missing in environment")

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    to = f"whatsapp:{to_number}"

    message = client.messages.create(
        body=f"Your OTP is {otp}.",
        from_=WHATSAPP_SANDBOX_FROM,
        to=to,
    )

    return message.sid
