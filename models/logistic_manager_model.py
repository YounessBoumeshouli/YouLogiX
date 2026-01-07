from schemas.delivery_man import DeliveryManCreate
from sqlalchemy.orm.session import Session

from entities.delivery_man_entity import DeliveryMan
from entities.enums.status_enum import EnumStatus
from entities.enums.vehicule_enum import EnumVehicule
from entities.client_entity import Client
from entities.parcel_entity import Parcel
from schemas.delivery_man import DeliveryManCreate
from models.parcel_model import ParcelModel
import models.client_model as ClientModel

from entities import LogisticsManager
from entities.enums.vehicule_enum import EnumVehicule


class LogisticManagerModel():
    def __init__(self, db: Session):
        self.db = db

    # def deliveryMan_create(self , db, delivery_man_in: DeliveryManCreate)->bool:
    #     delivery_man_data = delivery_man_in.model_dump()
    #
    #     db_delivery_man = Client(
    #         **delivery_man_data,
    #         hashed_password=hashed_password
    #     )
    #
    #     db.add(db_delivery_man)
    #     db.commit()
    #     db.refresh(db_delivery_man)
    #     return db_delivery_man
    # Correct
    def get_client_adresse(self, parcel: Parcel):
        result =  self.db.query(Client.address).filter(Client.id == parcel.idClient).first()
        return result[0]
    def GetDisponibleDeliveryMan(self,parcel_id):
        parcel_model  = ParcelModel(self.db)
        parcel =  parcel_model.getParcel(parcel_id)
        address = self.get_client_adresse(parcel)
        return self.db.query(DeliveryMan).where(DeliveryMan.address == address).first()
    def checkWeight(self):
        pass
    def checkCity(self):
        pass

    def assignParcel(self, parcel_id):
        delivery_man = self.GetDisponibleDeliveryMan(parcel_id)
        parcel_model  = ParcelModel(self.db)
        return parcel_model.assignToDeliveryMan(parcel_id,delivery_man.id)
