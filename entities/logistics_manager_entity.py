from sqlalchemy import Column, Integer, ForeignKey
from entities.user_entity import User

class LogisticsManager(User):
    __tablename__ = "logistics_managers"

    id = Column(Integer, ForeignKey("users.id"), primary_key=True)