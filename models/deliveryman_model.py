from entities.delivery_man_entity import Delivery_man
from entities.enums.Parcel_enum import Parcel_enum
from app.schemas.delivery_man import DeliveryManCreate
import parcel_model
class DeliveryManModel:
    def __int__(self,db):
        self.db = db

    def seed_delivery_men(db: Session):
        if db.query(Delivery_man).count() == 0:
            print("🌱 Initialisation des 10 livreurs...")
            for i in range(1, 11):
                new_man = Delivery_man(
                    name=f"Livreur {i}",
                    email=f"delivery{i}@youlogix.com",
                    hashed_password="hashed_password_example",
                    address=f"{i} Rue de la Logistique",
                    vehicule=EnumVehicule.MOTO if i % 2 == 0 else EnumVehicule.CAMION
                )
                db.add(new_man)
            db.commit()
            print("✅ 10 livreurs insérés avec succès.")
        else:
            print("ℹ️ Les livreurs existent déjà, skipping seed.")
    def GetAll(self):
        return self.db.query(Delivery_man).all()
    def get_all_parcels(self):
        return self.db.query(Delivery_man).all()
    def get_client_adresse(self,parcel : Parcel):
        return self.db.query(Client.adress).where(id,parcel.c.client_id)
    def GetDisponibleDeliveryMan(self,parcel_id):
        parcel =  parcel_model.getParcel(parcel_id)
        adress = get_client_adresse(parcel)
        return slef.db.query(Delivery_man).where(Delivery_man.adresse , adress).first()

    def assignParcel(self, parcel_id)->bool:
        delivery_man = GetDisponibleDeliveryMan(self.db,parcel_id)
        parcel =  parcel_model.assignToDeliveryMan(parcel_id,delivery_man.c.id)

    def deliveryMan_create(self,delivery_man_in: DeliveryManCreate)->bool:
        delivery_man_data = delivery_man_in.model_dump()
        db_delivery_man = Client(
            **delivery_man_data,
            hashed_password=hashed_password
        )

        db.add(db_delivery_man)
        self.db.commit()
        self.db.refresh(db_delivery_man)
        return db_delivery_man
