from pydantic import BaseModel
from pydantic import ConfigDict
class ClientCreateSchema(BaseModel):
    first_name: str
    last_name: str
    email: str
    address: str
    phone: str
    password: str


class ClientResponseSchema(ClientCreateSchema):
    id: int
    model_config = ConfigDict(from_attributes=True)