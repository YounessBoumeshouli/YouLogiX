from sqlalchemy.orm.session import Session

from entities.delivery_man_entity import DeliveryMan
from entities.enums.status_enum import EnumStatus
from entities.enums.vehicule_enum import EnumVehicule
from schemas.delivery_man import DeliveryManCreate
import models.parcel_model as Parcel
import models.client_model as Client
from schemas.parcel_schema import ParcelResponseSchema


class DeliveryManModel:
    def __init__(self, db: Session):
        self.db = db

    def seed_delivery_men(self):
        if self.db.query(DeliveryMan).count() == 0:
            print("🌱 Initialisation des 10 livreurs...")
            for i in range(1, 11):
                new_man = DeliveryMan(
                    first_name=f"Livreur {i}",
                    last_name=f"Livreur {i}",
                    email=f"delivery{i}@youlogix.com",
                    password="hashed_password_example",
                    address=f"{i} Rue de la Logistique",
                    phone=f"06 449 9333{i}",
                    vehicule=EnumVehicule.CAR if i % 2 == 0 else EnumVehicule.MOTORBIKE
                )
                self.db.add(new_man)
            self.db.commit()
            print("✅ 10 livreurs insérés avec succès.")
        else:
            print("ℹ️ Les livreurs existent déjà, skipping seed.")
    # def GetAll(self):
    #     return self.db.query(DeliveryMan).all()
    def get_all_parcels(self):
        return self.db.query(DeliveryMan).all()

    #
    # def deliveryMan_create(self,delivery_man_in: DeliveryManCreate)->bool:
    #     delivery_man_data = delivery_man_in.model_dump()
    #     db_delivery_man = Client(
    #         **delivery_man_data,
    #         hashed_password=hashed_password
    #     )
    #
    #     db.add(db_delivery_man)
    #     self.db.commit()
    #     self.db.refresh(db_delivery_man)
    #     return db_delivery_man
