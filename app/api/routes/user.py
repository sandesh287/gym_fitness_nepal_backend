from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.schemas.user_schema import UserCreateOrUpdateRequest

router = APIRouter()

ADMIN_PHONES = ["9840184059"]


@router.get("/profile")
def get_profile(
  phone: str,
  db: Session = Depends(get_db),
):
  user = db.query(User).filter(User.phone == phone).first()

  if not user:
    role = "admin" if phone in ADMIN_PHONES else "user"
    user = User(phone=phone, role=role)
    db.add(user)
    db.commit()
    db.refresh(user)

  return {
    "message": "Profile fetched successfully",
    "data": {
      "id": user.id,
      "phone": user.phone,
      "name": user.name,
      "email": user.email,
      "role": user.role,
    },
  }


@router.put("/profile")
def update_profile(
  request: UserCreateOrUpdateRequest,
  db: Session = Depends(get_db),
):
  user = db.query(User).filter(User.phone == request.phone).first()

  if not user:
    user = User(phone=request.phone)

  user.name = request.name
  user.email = request.email

  db.add(user)
  db.commit()
  db.refresh(user)

  return {
    "message": "Profile updated successfully",
    "data": {
      "id": user.id,
      "phone": user.phone,
      "name": user.name,
      "email": user.email,
      "role": user.role,
    },
  }