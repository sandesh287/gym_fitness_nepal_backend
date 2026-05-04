from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.booking import Booking
from app.models.fitness_class import FitnessClass
from app.schemas.booking_schema import (
    FitnessClassCreateRequest,
    FitnessClassUpdateRequest,
)

router = APIRouter()


def fitness_class_to_dict(fitness_class: FitnessClass):
    return {
        "id": fitness_class.id,
        "gym_id": fitness_class.gym_id,
        "gym_name": fitness_class.gym_name,
        "title": fitness_class.title,
        "trainer": fitness_class.trainer,
        "time": fitness_class.time,
        "duration": fitness_class.duration,
        "capacity": fitness_class.capacity,
        "available_slots": fitness_class.available_slots,
    }


@router.get("/classes")
def get_classes(
    gym_id: int | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(FitnessClass)

    if gym_id:
        query = query.filter(FitnessClass.gym_id == gym_id)

    classes = query.order_by(FitnessClass.id.desc()).all()

    return {
        "message": "Classes fetched successfully",
        "data": [fitness_class_to_dict(c) for c in classes],
    }


@router.post("/classes")
def create_class(
    request: FitnessClassCreateRequest,
    db: Session = Depends(get_db),
):
    fitness_class = FitnessClass(
        gym_id=request.gym_id,
        gym_name=request.gym_name,
        title=request.title,
        trainer=request.trainer,
        time=request.time,
        duration=request.duration,
        capacity=request.capacity,
        available_slots=request.capacity,
    )

    db.add(fitness_class)
    db.commit()
    db.refresh(fitness_class)

    return {
        "message": "Class created successfully",
        "data": fitness_class_to_dict(fitness_class),
    }


@router.put("/classes/{class_id}")
def update_class(
    class_id: int,
    request: FitnessClassUpdateRequest,
    db: Session = Depends(get_db),
):
    fitness_class = (
        db.query(FitnessClass)
        .filter(FitnessClass.id == class_id)
        .first()
    )

    if not fitness_class:
        raise HTTPException(status_code=404, detail="Class not found")

    fitness_class.gym_id = request.gym_id
    fitness_class.gym_name = request.gym_name
    fitness_class.title = request.title
    fitness_class.trainer = request.trainer
    fitness_class.time = request.time
    fitness_class.duration = request.duration
    fitness_class.capacity = request.capacity
    fitness_class.available_slots = request.available_slots

    db.commit()
    db.refresh(fitness_class)

    return {
        "message": "Class updated successfully",
        "data": fitness_class_to_dict(fitness_class),
    }


@router.delete("/classes/{class_id}")
def delete_class(
    class_id: int,
    db: Session = Depends(get_db),
):
    fitness_class = (
        db.query(FitnessClass)
        .filter(FitnessClass.id == class_id)
        .first()
    )

    if not fitness_class:
        raise HTTPException(status_code=404, detail="Class not found")

    db.delete(fitness_class)
    db.commit()

    return {
        "message": "Class deleted successfully",
        "success": True,
    }


@router.post("/book")
def book_class(
    class_id: int,
    user_phone: str,
    db: Session = Depends(get_db),
):
    existing_booking = (
        db.query(Booking)
        .filter(
            Booking.class_id == class_id,
            Booking.user_phone == user_phone,
            Booking.status == "booked",
        )
        .first()
    )

    if existing_booking:
        return {
            "message": "You have already booked this class",
            "success": False,
        }

    fitness_class = (
        db.query(FitnessClass)
        .filter(FitnessClass.id == class_id)
        .first()
    )

    if not fitness_class:
        return {
            "message": "Class not found",
            "success": False,
        }

    if fitness_class.available_slots <= 0:
        return {
            "message": "No slots available",
            "success": False,
        }

    fitness_class.available_slots -= 1

    booking = Booking(
        class_id=class_id,
        user_phone=user_phone,
        class_title=fitness_class.title,
        trainer=fitness_class.trainer,
        time=fitness_class.time,
        duration=fitness_class.duration,
        gym_id=fitness_class.gym_id,
        status="booked",
    )

    db.add(booking)
    db.commit()
    db.refresh(booking)

    return {
        "message": "Class booked successfully",
        "success": True,
        "data": {
            "id": booking.id,
            "class_id": booking.class_id,
            "user_phone": booking.user_phone,
            "class_title": booking.class_title,
            "trainer": booking.trainer,
            "time": booking.time,
            "duration": booking.duration,
            "gym_id": booking.gym_id,
            "status": booking.status,
        },
    }


@router.get("/history")
def get_booking_history(
    user_phone: str,
    db: Session = Depends(get_db),
):
    bookings = (
        db.query(Booking)
        .filter(Booking.user_phone == user_phone)
        .order_by(Booking.id.desc())
        .all()
    )

    return {
        "message": "Booking history fetched successfully",
        "data": [
            {
                "id": booking.id,
                "class_id": booking.class_id,
                "user_phone": booking.user_phone,
                "class_title": booking.class_title,
                "trainer": booking.trainer,
                "time": booking.time,
                "duration": booking.duration,
                "gym_id": booking.gym_id,
                "status": booking.status,
            }
            for booking in bookings
        ],
    }


@router.patch("/{booking_id}/cancel")
def cancel_booking(
    booking_id: int,
    user_phone: str,
    db: Session = Depends(get_db),
):
    booking = (
        db.query(Booking)
        .filter(
            Booking.id == booking_id,
            Booking.user_phone == user_phone,
            Booking.status == "booked",
        )
        .first()
    )

    if not booking:
        return {
            "message": "Booking not found or already cancelled",
            "success": False,
        }

    booking.status = "cancelled"

    fitness_class = (
        db.query(FitnessClass)
        .filter(FitnessClass.id == booking.class_id)
        .first()
    )

    if fitness_class:
        fitness_class.available_slots += 1

    db.commit()
    db.refresh(booking)

    return {
        "message": "Booking cancelled successfully",
        "success": True,
        "data": {
            "id": booking.id,
            "status": booking.status,
        },
    }