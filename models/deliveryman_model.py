from sqlalchemy.orm.session import Session
from loguru import logger
from entities import LogisticsManager
from entities.delivery_man_entity import DeliveryMan
from entities import User
from entities.enums.status_enum import EnumStatus
from entities.enums.vehicule_enum import EnumVehicule
from schemas.delivery_man import DeliveryManCreate
import models.parcel_model as Parcel
import models.client_model as Client
from schemas.parcel_schema import ParcelResponseSchema
from auth.security import hash_password



class DeliveryManModel:
    def __init__(self, db: Session):
        self.db = db


    def get_all(self):
        return self.db.query(DeliveryMan).all()
    

    def create(self, first_name: str, last_name: str, email: str, address: str, phone: str, password: str, role: str, vehicule: str):
        delivery_man = DeliveryMan(
            first_name=first_name,
            last_name=last_name,
            email=email,
            address=address,
            phone=phone,
            role=role,
            password=password,
            vehicule=vehicule
        )
        self.db.add(delivery_man)
        self.db.commit()
        self.db.refresh(delivery_man)
        return delivery_man


    def seed_delivery_men(self):
        if self.db.query(DeliveryMan).count() == 0:
            print("🌱 Initialisation des livreurs avec zones...")

            city_zones = {
                "Marrakech": ["Menara", "Gueliz", "Medina", "Sidi Youssef"],
                "Casablanca": ["Anfa", "Maarif", "Ain Diab", "Sidi Moumen"],
                "Rabat": ["Agdal", "Hay Riad", "Hassan", "Yacoub El Mansour"]
            }
            cities = list(city_zones.keys())

            for i in range(1, 13):
                city_idx = (i - 1) // 4 % len(cities)
                zone_idx = (i - 1) % 4

                city = cities[city_idx]
                zone = city_zones[city][zone_idx]


                new_man = DeliveryMan(
                    first_name=f"Livreur {i}",
                    last_name=f"Livreur {i}",
                    email=f"delivery{i}@youlogix.com",
                    phone=f"06 549 9333{i}",
                    password=hash_password(f"password {i}"),
                    role="delivery_man",
                    address=f"{city} {zone}",  # "Marrakech Menara" format
                    vehicule=EnumVehicule.CAR if i % 2 == 0 else EnumVehicule.MOTORBIKE
                )
                self.db.add(new_man)

            try:
                self.db.commit()
                logger.success("✅ 12 livreurs insérés avec succès.")
            except Exception as e:
                self.db.rollback()
                logger.error(f"❌ Erreur lors du seed: {e}")
        else:
            logger.info("️ Les livreurs existent déjà, skipping seed.")

    def get_all_parcels(self):
        return self.db.query(DeliveryMan).all()

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
    def checkWeight(self):
        pass
    def checkCity(self):
        pass