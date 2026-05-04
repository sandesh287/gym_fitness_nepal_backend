from sqlalchemy import Column, Integer, String
from app.core.database import Base


class Membership(Base):
  __tablename__ = "memberships"

  id = Column(Integer, primary_key=True, index=True)
  user_phone = Column(String, index=True)

  gym_id = Column(Integer)
  gym_name = Column(String)

  plan_id = Column(Integer)
  plan_title = Column(String)
  plan_price = Column(String)
  
  duration_days = Column(Integer)

  payment_method = Column(String)
  pidx = Column(String)

  start_date = Column(String)
  end_date = Column(String)

  status = Column(String)