from .user_entity import User
from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from entities.enums.vehicule_enum import EnumVehicule

class DeliveryMan(User):
    __tablename__ = "delivery_men"

    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    address = Column(String, nullable=False)
    vehicule = Column(Enum(EnumVehicule, name="vehicule_enum"), nullable=False)

