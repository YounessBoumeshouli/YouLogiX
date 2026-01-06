from sqlalchemy import Column, Text, Integer, String, Float, ForeignKey, TIMESTAMP, func
from app.db.database import Base
from enums.status_enum import EnumStatus

class HistoricalStatus(Base):
    __tablename__ = "historical_status"

    id = Column(Integer, primary_key=True)
    oldStatut = Column(EnumStatus, nullable=False)
    newStatut = Column(EnumStatus, nullable=False)
    timestamp = Column(TIMESTAMP,server_default=func.now())
    idParcel = Column(Integer, ForeignKey("parcels.id"), nullable=False)