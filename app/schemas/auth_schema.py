from pydantic import BaseModel


class SendOtpRequest(BaseModel):
  phone: str


class VerifyOtpRequest(BaseModel):
  phone: str
  otp: str