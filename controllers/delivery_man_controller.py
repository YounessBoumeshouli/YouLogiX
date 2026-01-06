from sqlalchemy.orm import Session
from models.client_model import get_all_users
from models.delivery_man_model import get_all_percels
class DeliveryManController:
    def __init__(self,delivery_man_model):
        self.delivery_man_model  = delivery_man_model
    def seed_delivery_men(self):
        self.delivery_man_model.seed_delivery_men()
    def fetch_percels(db: Session):
        percels = get_all_percels(db)
        return percels
