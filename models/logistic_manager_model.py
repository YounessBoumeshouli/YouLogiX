from sqlalchemy.sql.functions import func

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
        city = address.split(' ')[0].strip()
        total_weight_column = func.sum(Parcel.weight).label("total_weight")
        delivery_men = (
            self.db.query(
                DeliveryMan,
                total_weight_column
            )
            .join(Parcel, DeliveryMan.id == Parcel.idDeliveryMan)
            .filter(Parcel.status == EnumStatus.APPROVED )
            .group_by(DeliveryMan)
            .order_by(total_weight_column.asc())
            .all()
        )
        if delivery_men :
            choosingDeliveryMan = delivery_men[0][0]

            for row in delivery_men:
                delivery_man = row[0]
                total_weight = row[1]

                if delivery_man.vehicule == EnumVehicule.MOTORBIKE:
                    return delivery_man

            return choosingDeliveryMan
        else :
            return 'there is available delivery man for this area'

    def assignParcel(self, parcel_id):
        delivery_man = self.GetDisponibleDeliveryMan(parcel_id)
        if delivery_man and hasattr(delivery_man, 'id'):
            parcel_model = ParcelModel(self.db)
            # Perform the assignment
            return parcel_model.assignToDeliveryMan(parcel_id, delivery_man.id)
        else:
            # 2. Logic for when no delivery man is found
            print(f"No delivery man available for parcel {parcel_id}")
            return delivery_man
