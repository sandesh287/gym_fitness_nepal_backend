from pydantic import BaseModel


class MembershipCreateRequest(BaseModel):
  user_phone: str
  gym_id: int
  gym_name: str
  plan_id: int
  plan_title: str
  plan_price: str
  duration_days: int
  payment_method: str
  pidx: str