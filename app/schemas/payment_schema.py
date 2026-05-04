from pydantic import BaseModel


class KhaltiInitiateRequest(BaseModel):
  amount: int
  purchase_order_id: str
  purchase_order_name: str
  customer_name: str
  customer_email: str
  customer_phone: str