from pydantic import BaseModel

class ClientCreateSchema(BaseModel):
    first_name: str
    last_name: str
    address: str
    phone: str


class ClientResponseSchema(BaseModel):
    first_name: str
    last_name: str
    email: str
    address: str
    phone: str
    password: str