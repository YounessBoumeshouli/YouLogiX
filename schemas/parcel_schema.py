from pydantic import BaseModel

class ParcelCreateSchema(BaseModel):
    description: str
    weight: float
    status: str
    idClient: int
    idRecipient: int
    DestinationCity: str


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

    class Config:
        from_attributes = True