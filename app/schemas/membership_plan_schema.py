from pydantic import BaseModel


class MembershipPlanCreateRequest(BaseModel):
  gym_id: int
  gym_name: str
  title: str
  duration: str
  duration_days: int
  price: int
  features: str


class MembershipPlanUpdateRequest(BaseModel):
  gym_id: int
  gym_name: str
  title: str
  duration: str
  duration_days: int
  price: int
  features: str