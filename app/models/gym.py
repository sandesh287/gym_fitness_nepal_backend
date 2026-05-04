from sqlalchemy import Column, Integer, String, Float
from app.core.database import Base


class Gym(Base):
  __tablename__ = "gyms"

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String, index=True)
  location = Column(String, index=True)
  price = Column(Integer)
  price_duration = Column(String, default="month")
  rating = Column(Float, default=0.0)