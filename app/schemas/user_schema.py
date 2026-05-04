from pydantic import BaseModel


class UserCreateOrUpdateRequest(BaseModel):
  phone: str
  name: str | None = None
  email: str | None = None