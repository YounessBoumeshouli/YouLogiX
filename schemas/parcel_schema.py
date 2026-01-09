from pydantic import BaseModel
from typing import Optional
from pydantic import ConfigDict
class ParcelCreateSchema(BaseModel):
    description: str
    weight: float
    status: str
    idClient: int
    idRecipient: int
    DestinationCity: str

class ParcelUpdateSchema(BaseModel):
    description: Optional[str] = None
    weight: Optional[float] = None
    idRecipient: Optional[int] = None
    DestinationCity: Optional[str] = None


class ParcelSchema(BaseModel):
    description: str
    weight: float
    status: str
    idDeliveryMan: int | None
    idClient: int
    idRecipient: int
    DestinationCity: str
    code: str


class ParcelResponseSchema(ParcelSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)