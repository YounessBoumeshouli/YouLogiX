from sqlalchemy import func , and_
from loguru import logger
from schemas.delivery_man import DeliveryManCreate
from sqlalchemy.orm.session import Session
from auth.security import hash_password

from entities.delivery_man_entity import DeliveryMan
from entities.enums.status_enum import EnumStatus
from entities.enums.vehicule_enum import EnumVehicule
from entities.client_entity import Client
from entities.parcel_entity import Parcel
from schemas.delivery_man import DeliveryManCreate
from models.parcel_model import ParcelModel
import models.client_model as ClientModel

from entities import LogisticsManager, User
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

    def GetDisponibleDeliveryMan(self, parcel_id):
        parcel_model = ParcelModel(self.db)
        parcel = parcel_model.getParcel(parcel_id)
        address = self.get_client_adresse(parcel)
        city = address.split(' ')[0].strip()

        total_weight_column = func.coalesce(func.sum(Parcel.weight), 0).label("total_weight")

        delivery_men = (
            self.db.query(DeliveryMan, total_weight_column)
            .outerjoin(
                Parcel,
                and_(
                    DeliveryMan.id == Parcel.idDeliveryMan,
                    Parcel.status == EnumStatus.APPROVED
                )
            )
            .filter(DeliveryMan.address.like(f"{city}%"))
            .group_by(DeliveryMan.id,User.id)
            .order_by(total_weight_column.asc())
            .all()
        )


        if delivery_men:
            for row in delivery_men:
                if row[0].vehicule == EnumVehicule.MOTORBIKE:
                    return row[0]
            return delivery_men[0][0]

        global_delivery_men = (
            self.db.query(DeliveryMan, total_weight_column)
            .outerjoin(Parcel, DeliveryMan.id == Parcel.idDeliveryMan)
            .filter(Parcel.status == EnumStatus.APPROVED)
            .group_by(DeliveryMan)
            .order_by(total_weight_column.asc())
            .all()
        )

        if global_delivery_men:
            logger.info(f"Global delivery men found: {global_delivery_men}")
            return global_delivery_men[0][0]
        else :
            logger.error("no delivery man is available")
            return None

    def assignParcel(self, parcel_id):
        delivery_man = self.GetDisponibleDeliveryMan(parcel_id)
        if delivery_man and hasattr(delivery_man, 'id'):
            parcel_model = ParcelModel(self.db)
            return parcel_model.assignToDeliveryMan(parcel_id, delivery_man.id)
        else:
            print(f"No delivery man available for parcel {parcel_id}")
            return delivery_man


    def seed_logistics_managers(self):
        if self.db.query(LogisticsManager).count() == 0:
            print("🌱 Initialisation d'un admin ...")

            new_admin = LogisticsManager(
                first_name=f"Logistics",
                last_name=f"Manager",
                email=f"admin@youlogix.com",
                password=hash_password("pass1234"),
                phone=f"06 111 1111111",
                role="logistics_manager"
            )

            self.db.add(new_admin)
            self.db.commit()

        else:
            print("ℹ️ L'admin existe déjà, skipping seed.")



    def get_all_users(self):
        return self.db.query(User).all()