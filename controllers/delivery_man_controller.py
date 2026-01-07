from sqlalchemy.orm import Session
from schemas.parcel_schema import ParcelResponseSchema
from models.deliveryman_model import DeliveryManModel
from models.parcel_model import Parcel
from entities.enums.status_enum import EnumStatus

class DeliveryManController:
    def __init__(self, db:Session):
        self.db = db
        self.delivery_man_model  = DeliveryManModel(db)
    def seed_delivery_men(self):
        self.delivery_man_model.seed_delivery_men()
    def fetch_percels(self  ):
        percels = self.delivery_man_model.get_all_parcels()
        return [1,2,4]
    def isAssigned(self ,delivery_man_id ,  parcel_id)->bool:
        parcel =  Parcel.getParcelByDeliveryMan(delivery_man_id)
        return False if parcel.status == EnumStatus.LIVRED else True
