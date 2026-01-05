from sqlalchemy.orm import Session
from entities.client_entity import User

def get_all_users(db: Session):
    return db.query(User).all()