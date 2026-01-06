from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from app.db.database import Base
from entities.enums.vehicule_enum import EnumVehicule

class DeliveryMan(Base):
    __tablename__ = "delivery_men"

    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    address = Column(String, nullable=False)
    vehicule = Column(Enum(EnumVehicule, name="vehicule_enum"), nullable=False)

