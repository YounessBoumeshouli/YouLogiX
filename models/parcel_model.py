from random import randint
from loguru import logger
from sqlalchemy.orm.session import Session

from entities import HistoricalStatus, Client
from entities.parcel_entity import Parcel

from entities.enums.status_enum import EnumStatus
from schemas import delivery_man
from random import randint, choice

class ParcelModel :
    def __init__(self, db: Session):
        self.db = db



    def createParcel(self, description: str, weight: float, status: str, idClient: int, idRecipient: int, DestinationCity: str, code: str):
        parcel = Parcel(
            description = description,
            weight = weight,
            status = status,
            idDeliveryMan = None,
            idClient = idClient,
            idRecipient = idRecipient,
            DestinationCity = DestinationCity,
            code = code
        )

        self.db.add(parcel)
        self.db.commit()
        self.db.refresh(parcel)

        self.updateParcelStatus(parcel.id, EnumStatus.CREATED)
        logger.info(f"PARCEL: Parcel {parcel.id} 's created successfully")

        return parcel



    def getParcelById(self, id) -> Parcel:
        return self.db.query(Parcel).where(Parcel.id == id).first()
    


    def getAll(self) -> list[Parcel]:
        return self.db.query(Parcel).all()
    


    def getParcelsByClient(self, client_id: int) -> list[Parcel]:
        return self.db.query(Parcel).where(Parcel.idClient == client_id).all()
    


    def getParcelsByRecipient(self, recipient_id: int) -> list[Parcel]:
        return self.db.query(Parcel).where(Parcel.idRecipient == recipient_id).all()
    


    def getParcelsByDeliveryMan(self, delivery_id: int) -> list[Parcel]:
        return self.db.query(Parcel).where(Parcel.idDeliveryMan == delivery_id).all()
    


    def getParcelsByCity(self, city: str) -> list[Parcel]:
        return self.db.query(Parcel).where(Parcel.DestinationCity == city).all()
    


    def getParcelsByStatus(self, status: str) -> list[Parcel]:
        return self.db.query(Parcel).where(Parcel.status == status).all()


    
    def updateParcel(self, parcel: Parcel, **kwargs):
        for key, value in kwargs.items():
            if hasattr(parcel, key):
                logger.info(f"PARCEL: Parcel {parcel.id} ''s column {key}  is updated successfully")

                setattr(parcel, key, value)

        self.db.commit()
        self.db.refresh(parcel)

        return parcel
    


    def updateParcelStatus(self, parcel_id, new_status) -> HistoricalStatus | None:
        parcel = self.getParcelById(parcel_id)

        if not parcel:
            return None
        
        history = HistoricalStatus(
            statut = new_status,
            idParcel = parcel_id
        )

        self.db.add(history)
        self.db.commit()
        self.db.refresh(history)
        logger.info(f"PARCEL: Parcel {parcel_id} 's status is updated successfully from {parcel.status} to {new_status}  ")
        return history



    def assignToDeliveryMan(self, parcel_id, delivery_man_id):
         self.db.query(Parcel).filter(Parcel.id == parcel_id).update(
            {"idDeliveryMan": delivery_man_id}
        )
         self.db.commit()
         logger.info(f"ASSIGN: Parcel {parcel_id} given to {delivery_man_id}")
         return "parcel assinged to a delivery man successfully"
    

    
    def seed_parcels(self, count: int = 10):
        if self.db.query(Parcel).count() == 0:
            client_ids = [c.id for c in self.db.query(Client.id).all()]

            if not client_ids:
                print("❌ Cannot seed parcels: No clients found in database!")
                return

            print(f"🌱 Initializing {count} parcels using Client IDs: {client_ids}")

            city_zones = {
                "Marrakech": ["Menara", "Gueliz", "Medina", "Sidi Youssef"],
                "Casablanca": ["Anfa", "Maarif", "Ain Diab", "Sidi Moumen"],
                "Rabat": ["Agdal", "Hay Riad", "Hassan", "Yacoub El Mansour"]
            }
            cities = list(city_zones.keys())

            for i in range(1, count + 1):
                city = cities[(i - 1) // 4 % len(cities)]
                zone = city_zones[city][(i - 1) % 4]

                # 2. Pick a random ID from the ACTUAL list of clients
                random_client_id = choice(client_ids)
                random_recipient_id = choice(client_ids)

                new_parcel = Parcel(
                    description=f"Parcel {i}",
                    weight=float(randint(3, 50)),
                    status=EnumStatus.CREATED,
                    idClient=random_client_id,
                    idRecipient=random_recipient_id,
                    idDeliveryMan=None,
                    DestinationCity=f"{city} {zone}",
                    code=str(randint(1000, 99999))
                )
                self.db.add(new_parcel)

            self.db.commit()
            print("✅ Colis insérés avec succès.")



    def getParcel(self, parcel_id):
        return self.db.query(Parcel).filter(Parcel.id == parcel_id).first()
    


    def assignParcel(parcel_id)->bool:
        parcel =  parcel_id.getParcel(parcel_id)
        return 0 if parcel.status == EnumStatus.LIVRED else 1
