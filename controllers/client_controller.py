from sqlalchemy.orm import Session
from models.client_model import get_all_users

def fetch_users(db: Session):
    users = get_all_users(db)
    return users