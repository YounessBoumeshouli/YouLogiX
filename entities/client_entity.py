from sqlalchemy import Column, Integer, String, ForeignKey
from entities.user_entity import User

class Client(User):
    __tablename__ = "clients"

    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    address = Column(String, nullable=False)