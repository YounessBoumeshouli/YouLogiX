from pydantic import BaseModel, EmailStr
from typing import Literal


class UserReadSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    role: str


class UserCreateSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    phone: str


class ClientCreateSchema(UserCreateSchema):
    role: Literal["client"]
    address: str


class DeliveryManCreateSchema(UserCreateSchema):
    role: Literal["delivery_man"]
    address: str
    vehicule: Literal["CAR", "MOTORBIKE"]


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class UserLoginResponseSchema(BaseModel):
    access_token: str
    token_type: str


class UserTokenSchema(BaseModel):
    token: str
