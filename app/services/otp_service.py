import random

otp_storage = {}


def generate_otp(phone: str) -> str:
  otp = str(random.randint(100000, 999999))
  otp_storage[phone] = otp
  print(f"OTP for {phone}: {otp}")
  return otp


def verify_otp(phone: str, otp: str) -> bool:
  stored_otp = otp_storage.get(phone)

  if stored_otp == otp:
      del otp_storage[phone]
      return True

  return False