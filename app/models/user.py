from sqlalchemy import Column, Integer, String
from app.core.database import Base


class User(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True, index=True)
  phone = Column(String, unique=True, index=True)
  name = Column(String, nullable=True)
  email = Column(String, nullable=True)
  role = Column(String, default="user")