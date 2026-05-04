from fastapi import FastAPI
from app.api.routes import auth, gym, payment, membership, booking, user, membership_plan
from app.core.database import engine, Base
from app.models import membership as membership_model
from app.models import booking as booking_model
from app.models import user as user_model
from app.models import gym as gym_model
from app.models import fitness_class as fitness_class_model
from app.models import membership_plan as membership_plan_model

app = FastAPI(
  title="Gym Fitness Nepal API",
  version="1.0.0"
)

Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])

app.include_router(gym.router, prefix="/api/v1/gyms", tags=["Gyms"])

app.include_router(payment.router, prefix="/api/v1/payments", tags=["Payments"])

app.include_router(membership.router, prefix="/api/v1/memberships", tags=["Memberships"])

app.include_router(booking.router, prefix="/api/v1/bookings", tags=["Bookings"])

app.include_router(user.router, prefix="/api/v1/users", tags=["Users"])

app.include_router(
  membership_plan.router,
  prefix="/api/v1/membership-plans",
  tags=["Membership Plans"],
)


@app.get("/")
def root():
  return {
    "message": "Gym Fitness Nepal API is running"
  }


@app.get("/health")
def health_check():
  return {
    "status": "healthy"
  }