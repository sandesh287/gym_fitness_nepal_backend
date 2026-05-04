from pydantic import BaseModel


class FitnessClassCreateRequest(BaseModel):
  gym_id: int
  gym_name: str
  title: str
  trainer: str
  time: str
  duration: str
  capacity: int


class FitnessClassUpdateRequest(BaseModel):
  gym_id: int
  gym_name: str
  title: str
  trainer: str
  time: str
  duration: str
  capacity: int
  available_slots: int