from pydantic import BaseModel

class ClientCreateSchema(BaseModel):
    first_name: str
    last_name: str
    email: str
    address: str
    phone: str
    password: str


class ClientResponseSchema(ClientCreateSchema):
    id: int

    class Config:
        from_attributes = True