from sqlalchemy import Column, Integer, String, ForeignKey
from .enums.vehicule_enum import EnumVehicule
from .user_entity import User
class Delivery_man(User):
    __tablename__ = "delivery_men"

    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    address = Column(String, nullable=False)
    vehicule = Column(EnumVehicule, nullable=False)

