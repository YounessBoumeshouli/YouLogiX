from pydantic import BaseModel
from pydantic import ConfigDict

class ClientSchema(BaseModel):
    first_name: str
    last_name: str
    email: str
    address: str
    phone: str

class ClientCreateSchema(ClientSchema):
    role: str
    password: str


class ClientResponseSchema(ClientSchema):
    id: int
    model_config = ConfigDict(from_attributes=True)
