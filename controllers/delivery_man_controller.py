from sqlalchemy.orm import Session
from models.client_model import get_all_users
from models.deliveryman_model import DeliveryManModel
class DeliveryManController:
    def __init__(self,delivery_man_model):
        self.delivery_man_model  = delivery_man_model
    def seed_delivery_men(self):
        self.delivery_man_model.seed_delivery_men()
    def fetch_percels(db: Session):
        percels = DeliveryManModel.get_all_parcels(db)
        return percels
