from pydantic import BaseModel


class GymCreateRequest(BaseModel):
    name: str
    location: str
    price: int
    price_duration: str
    rating: float = 0.0


class GymUpdateRequest(BaseModel):
    name: str
    location: str
    price: int
    price_duration: str
    rating: float = 0.0