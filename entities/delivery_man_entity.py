from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.database import Base
from enums.vehicule_enum import EnumVehicule

class Delivery_man(Base):
    __tablename__ = "delivery_men"

    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    address = Column(String, nullable=False)
    vehicule = Column(EnumVehicule, nullable=False)

