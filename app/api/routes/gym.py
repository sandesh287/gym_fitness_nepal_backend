from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.gym import Gym
from app.schemas.gym_schema import GymCreateRequest, GymUpdateRequest
from app.models.fitness_class import FitnessClass

router = APIRouter()


def gym_to_dict(gym: Gym):
  return {
    "id": gym.id,
    "name": gym.name,
    "location": gym.location,
    "price": gym.price,
    "price_duration": gym.price_duration,
    "rating": gym.rating,
    "display_price": f"Rs. {gym.price}/{gym.price_duration}",
  }


@router.get("/")
def get_gyms(
  search: str | None = None,
  location: str | None = None,
  class_title: str | None = None,
  min_price: int | None = None,
  max_price: int | None = None,
  db: Session = Depends(get_db),
):
  query = db.query(Gym)

  if search:
    search_value = f"%{search}%"
    query = query.filter(
      (Gym.name.ilike(search_value)) |
      (Gym.location.ilike(search_value))
    )

  if location and location != "All":
    query = query.filter(Gym.location == location)

  if min_price is not None:
    query = query.filter(Gym.price >= min_price)

  if max_price is not None:
    query = query.filter(Gym.price <= max_price)

  gyms = query.all()
  gym_data = [gym_to_dict(gym) for gym in gyms]

  if class_title and class_title != "All":
    gym_ids = {
      c.gym_id
      for c in db.query(FitnessClass)
      .filter(FitnessClass.title == class_title)
      .all()
    }

    gym_data = [
      gym for gym in gym_data
      if gym["id"] in gym_ids
    ]

  return {
    "message": "Gyms fetched successfully",
    "data": gym_data,
  }


@router.post("/")
def create_gym(
  request: GymCreateRequest,
  db: Session = Depends(get_db),
):
  gym = Gym(
    name=request.name,
    location=request.location,
    price=request.price,
    price_duration=request.price_duration,
    rating=request.rating,
  )

  db.add(gym)
  db.commit()
  db.refresh(gym)

  return {
    "message": "Gym created successfully",
    "data": gym_to_dict(gym),
  }


@router.put("/{gym_id}")
def update_gym(
  gym_id: int,
  request: GymUpdateRequest,
  db: Session = Depends(get_db),
):
  gym = db.query(Gym).filter(Gym.id == gym_id).first()

  if not gym:
    raise HTTPException(status_code=404, detail="Gym not found")

  gym.name = request.name
  gym.location = request.location
  gym.price = request.price
  gym.price_duration = request.price_duration
  gym.rating = request.rating

  db.commit()
  db.refresh(gym)

  return {
    "message": "Gym updated successfully",
    "data": gym_to_dict(gym),
  }


@router.delete("/{gym_id}")
def delete_gym(
  gym_id: int,
  db: Session = Depends(get_db),
):
  gym = db.query(Gym).filter(Gym.id == gym_id).first()

  if not gym:
    raise HTTPException(status_code=404, detail="Gym not found")

  db.delete(gym)
  db.commit()

  return {
    "message": "Gym deleted successfully",
    "success": True,
  }


