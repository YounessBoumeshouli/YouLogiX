from sqlalchemy.orm import Session
from schemas.parcel_schema import ParcelResponseSchema
from models.logistic_manager_model import LogisticManagerModel
class LogisticMangerController:
    def __init__(self, db:Session):
        self.db = db
        self.logistic_manager_model  = LogisticManagerModel(db)
    def seed_logistic_manager(self):
        self.logistic_manager_model.seed_logistic_manager()
    def fetch_percels(self ):
        percels = self.logistic_manager_model.get_all_parcels()
        return percels
    def assignParcel(self , parcel_id ):
        self.logistic_manager_model.assignParcel(parcel_id)
