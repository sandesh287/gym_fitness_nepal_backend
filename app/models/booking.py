from sqlalchemy import Column, Integer, String
from app.core.database import Base


class Booking(Base):
  __tablename__ = "bookings"

  id = Column(Integer, primary_key=True, index=True)

  user_phone = Column(String, index=True)

  class_id = Column(Integer, index=True)
  class_title = Column(String)
  trainer = Column(String)
  time = Column(String)
  duration = Column(String)

  gym_id = Column(Integer)
  status = Column(String)