from sqlalchemy.orm import Session
from models.client_model import get_all_users
from models.delivery_man_model import get_all_percels

def fetch_percels(db: Session):
    percels = get_all_percels(db)
    return percels