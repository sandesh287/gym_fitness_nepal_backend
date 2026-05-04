from sqlalchemy import Column, Integer, String
from app.core.database import Base


class FitnessClass(Base):
  __tablename__ = "fitness_classes"

  id = Column(Integer, primary_key=True, index=True)

  gym_id = Column(Integer, index=True)
  gym_name = Column(String)

  title = Column(String, index=True)
  trainer = Column(String)
  time = Column(String)
  duration = Column(String)

  capacity = Column(Integer)
  available_slots = Column(Integer)