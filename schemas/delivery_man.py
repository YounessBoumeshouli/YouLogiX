# app/schemas/delivery_man.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from pydantic import ConfigDict
class DeliveryManBase(BaseModel):
    address: str = Field(..., min_length=2, max_length=50)
    vehicule: str

class DeliveryManCreate(DeliveryManBase):
    adress: str = Field(..., min_length=8)

class DeliveryManResponse(DeliveryManBase):
    id: int

    model_config = ConfigDict(from_attributes=True)