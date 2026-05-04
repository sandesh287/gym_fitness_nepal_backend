from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.membership_plan import MembershipPlan
from app.schemas.membership_plan_schema import (
  MembershipPlanCreateRequest,
  MembershipPlanUpdateRequest,
)

router = APIRouter()


def plan_to_dict(plan: MembershipPlan):
  return {
    "id": plan.id,
    "gym_id": plan.gym_id,
    "gym_name": plan.gym_name,
    "title": plan.title,
    "duration": plan.duration,
    "duration_days": plan.duration_days,
    "price": plan.price,
    "display_price": f"Rs. {plan.price}",
    "features": [
      feature.strip()
      for feature in plan.features.split(",")
      if feature.strip()
    ],
  }


@router.get("/")
def get_all_plans(db: Session = Depends(get_db)):
  plans = db.query(MembershipPlan).order_by(MembershipPlan.id.desc()).all()

  return {
    "message": "Membership plans fetched successfully",
    "data": [plan_to_dict(plan) for plan in plans],
  }


@router.get("/gym/{gym_id}")
def get_plans_by_gym(
  gym_id: int,
  db: Session = Depends(get_db),
):
  plans = (
    db.query(MembershipPlan)
    .filter(MembershipPlan.gym_id == gym_id)
    .order_by(MembershipPlan.id.desc())
    .all()
  )

  return {
    "message": "Gym membership plans fetched successfully",
    "data": [plan_to_dict(plan) for plan in plans],
  }


@router.post("/")
def create_plan(
  request: MembershipPlanCreateRequest,
  db: Session = Depends(get_db),
):
  plan = MembershipPlan(
    gym_id=request.gym_id,
    gym_name=request.gym_name,
    title=request.title,
    duration=request.duration,
    duration_days=request.duration_days,
    price=request.price,
    features=request.features,
  )

  db.add(plan)
  db.commit()
  db.refresh(plan)

  return {
    "message": "Membership plan created successfully",
    "data": plan_to_dict(plan),
  }


@router.put("/{plan_id}")
def update_plan(
  plan_id: int,
  request: MembershipPlanUpdateRequest,
  db: Session = Depends(get_db),
):
  plan = db.query(MembershipPlan).filter(MembershipPlan.id == plan_id).first()

  if not plan:
    raise HTTPException(status_code=404, detail="Membership plan not found")

  plan.gym_id = request.gym_id
  plan.gym_name = request.gym_name
  plan.title = request.title
  plan.duration = request.duration
  plan.duration_days = request.duration_days
  plan.price = request.price
  plan.features = request.features

  db.commit()
  db.refresh(plan)

  return {
    "message": "Membership plan updated successfully",
    "data": plan_to_dict(plan),
  }


@router.delete("/{plan_id}")
def delete_plan(
  plan_id: int,
  db: Session = Depends(get_db),
):
  plan = db.query(MembershipPlan).filter(MembershipPlan.id == plan_id).first()

  if not plan:
    raise HTTPException(status_code=404, detail="Membership plan not found")

  db.delete(plan)
  db.commit()

  return {
    "message": "Membership plan deleted successfully",
    "success": True,
  }