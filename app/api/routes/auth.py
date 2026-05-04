from fastapi import APIRouter, HTTPException
from app.schemas.auth_schema import SendOtpRequest, VerifyOtpRequest
from app.services.otp_service import generate_otp, verify_otp

router = APIRouter()


@router.post("/send-otp")
def send_otp(request: SendOtpRequest):
  otp = generate_otp(request.phone)

  return {
    "message": "OTP sent successfully",
    "phone": request.phone,
    "debug_otp": otp
  }


@router.post("/verify-otp")
def verify_user_otp(request: VerifyOtpRequest):
  is_valid = verify_otp(request.phone, request.otp)

  if not is_valid:
    raise HTTPException(
      status_code=400,
      detail="Invalid OTP"
    )

  return {
    "message": "OTP verified successfully",
    "phone": request.phone,
    "access_token": "temporary_token_for_now"
  }