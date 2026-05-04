from sqlalchemy import Column, Integer, String
from app.core.database import Base


class MembershipPlan(Base):
  __tablename__ = "membership_plans"

  id = Column(Integer, primary_key=True, index=True)

  gym_id = Column(Integer, index=True)
  gym_name = Column(String)

  title = Column(String)
  duration = Column(String)
  duration_days = Column(Integer)
  price = Column(Integer)
  features = Column(String)