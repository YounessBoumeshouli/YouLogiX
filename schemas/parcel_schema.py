from pydantic import BaseModel

class ParcelCreateSchema(BaseModel):
    description: str
    weight: float
    status: str
    idDeliveryMan: str
    idClient: int
    idRecipient: int
    DestinationCity: str
    code :str


class ParcelResponseSchema(ParcelCreateSchema):
    id: int

    class Config:
        from_attributes = True