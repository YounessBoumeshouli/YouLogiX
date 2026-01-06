from sqlalchemy import Column, Text, Integer, String, Float, ForeignKey, Enum
from app.db.database import Base
from entities.enums.status_enum import EnumStatus

class Parcel(Base):
    __tablename__ = "parcels"

    id = Column(Integer, primary_key=True)
    description = Column(Text, nullable=False)
    weight = Column(Float, nullable=False)
    status = Column(Enum(EnumStatus, name="status_enum"), nullable=False)
    idDeliveryMan = Column(Integer, ForeignKey("delivery_men.id"), nullable=False)
    idClient = Column(Integer, ForeignKey("clients.id"), nullable=False)
    idRecipient = Column(Integer, ForeignKey("clients.id"), nullable=False)
    DestinationCity = Column(String, nullable=False)
    code = Column(String, nullable=False)