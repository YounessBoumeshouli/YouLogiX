from sqlalchemy import Column, Text, Integer, String, Float, ForeignKey, Enum, TIMESTAMP, func
from app.db.database import Base
from entities.enums.status_enum import EnumStatus

class HistoricalStatus(Base):
    __tablename__ = "historical_status"

    id = Column(Integer, primary_key=True)

    oldStatut = Column(Enum(EnumStatus, name="status_enum"), nullable=False)
    newStatut = Column(Enum(EnumStatus, name="status_enum"), nullable=False)
    timestamp = Column(TIMESTAMP,server_default=func.now())
    idParcel = Column(Integer, ForeignKey("parcels.id"), nullable=False)