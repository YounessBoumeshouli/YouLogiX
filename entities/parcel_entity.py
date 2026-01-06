from sqlalchemy import Column, Text, Integer, String, Float, ForeignKey
from app.db.database import Base
from enums.status_enum import EnumStatus

class Parcel(Base):
    __tablename__ = "parcels"

    id = Column(Integer, primary_key=True)
    description = Column(Text, nullable=False)
    weight = Column(Float, nullable=False)
    status = Column(EnumStatus, nullable=False)
    idDeliveryMan = Column(Integer, ForeignKey("delivery_men.id"), nullable=False)
    idClient = Column(Integer, ForeignKey("clients.id"), nullable=False)
    idRecipient = Column(Integer, ForeignKey("clients.id"), nullable=False)
    DestinationCity = Column(String, nullable=False)
    code = Column(String, nullable=False)