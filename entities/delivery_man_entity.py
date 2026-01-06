from sqlalchemy import Column, Integer, String
from app.DB.database import Base

class Delivery_man(Base):
    __tablename__ = "delivery_man"
    id = Column(Integer, primary_key=True)
    name = Column(String)

