import hmac
import hashlib
import secrets
import os

OTP_TTL_SECONDS = os.getenv("OTP_TTL_SECONDS") # 5 minutes 


def generate_otp_4() -> str:
    
    return f"{secrets.randbelow(10000):04d}"


def hash_otp(otp: str, secret: str) -> str:
    
    if not secret:
        raise ValueError("OTP secret missing")

    msg = otp.encode("utf-8")
    key = secret.encode("utf-8")
    return hmac.new(key, msg, hashlib.sha256).hexdigest()


def verify_otp(otp: str, stored_hash: str, secret: str) -> bool:

    computed = hash_otp(otp, secret)
    return hmac.compare_digest(computed, stored_hash)




# OTP_TTL_SECONDS = 300  # 5 min

# def generate_otp_4() -> str:
#     # 0000 to 9999, always 4 digits
#     return f"{random.randint(0, 9999):04d}"

# def hash_otp(otp: str, secret: str) -> str:
#     # OTP ko direct store nahi karte; HMAC hash store karte hain
#     return hmac.new(secret.encode(), otp.encode(), hashlib.sha256).hexdigest()

# def verify_otp(otp: str, otp_hash: str, secret: str) -> bool:
#     # timing attack safe compare
#     return hmac.compare_digest(hash_otp(otp, secret), otp_hash)

# def now_ts() -> int:
#     return int(time.time())