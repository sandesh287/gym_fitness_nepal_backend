from datetime import datetime, timedelta, date
from fastapi import APIRouter
from app.schemas.membership_schema import MembershipCreateRequest
from sqlalchemy.orm import Session
from fastapi import Depends
from app.core.database import get_db
from app.models.membership import Membership

router = APIRouter()


def update_membership_expiry(membership, db):
  today = date.today()
  end_date = date.fromisoformat(membership.end_date)

  if membership.status == "active" and today > end_date:
    membership.status = "expired"
    db.commit()
    db.refresh(membership)

  return membership


@router.post("/")
def create_membership(
  request: MembershipCreateRequest,
  db: Session = Depends(get_db),
):
  membership = Membership(
    user_phone=request.user_phone,
    gym_id=request.gym_id,
    gym_name=request.gym_name,
    plan_id=request.plan_id,
    plan_title=request.plan_title,
    plan_price=request.plan_price,
    duration_days=request.duration_days,
    payment_method=request.payment_method,
    pidx=request.pidx,
    start_date=datetime.now().date().isoformat(),
    end_date=(datetime.now() + timedelta(days=request.duration_days)).date().isoformat(),
    status="active",
  )

  db.add(membership)
  db.commit()
  db.refresh(membership)

  return {
    "message": "Membership created successfully",
    "data": {
      "id": membership.id,
      "plan_title": membership.plan_title,
    },
  }


@router.get("/active")
def get_active_membership(
  user_phone: str,
  db: Session = Depends(get_db),
):
  memberships = (
    db.query(Membership)
    .filter(Membership.user_phone == user_phone)
    .order_by(Membership.id.desc())
    .all()
  )

  for membership in memberships:
    membership = update_membership_expiry(membership, db)

    if membership.status == "active":
      return {
        "message": "Active membership found",
        "data": membership.__dict__,
      }

  return {
    "message": "No active membership",
    "data": None,
  }


@router.get("/history")
def get_membership_history(
  user_phone: str,
  db: Session = Depends(get_db),
):
  memberships = (
    db.query(Membership)
    .filter(Membership.user_phone == user_phone)
    .order_by(Membership.id.desc())
    .all()
  )

  updated_memberships = [
    update_membership_expiry(membership, db)
    for membership in memberships
  ]

  return {
    "message": "Membership history fetched successfully",
    "data": [m.__dict__ for m in updated_memberships],
  }