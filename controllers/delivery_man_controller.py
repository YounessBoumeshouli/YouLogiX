from sqlalchemy.orm import Session
from schemas.parcel_schema import ParcelResponseSchema
from models.deliveryman_model import DeliveryManModel
class DeliveryManController:
    def __init__(self, db:Session):
        self.db = db
        self.delivery_man_model  = DeliveryManModel(db)
    def seed_delivery_men(self):
        self.delivery_man_model.seed_delivery_men()
    def fetch_percels(self ):
        percels = self.delivery_man_model.get_all_parcels()
        return percels
