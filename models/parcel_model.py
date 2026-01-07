from sqlalchemy.orm import Session
from entities.parcel_entity import Parcel
from entities.enums.status_enum import EnumStatus
from random import randint
from entities.historical_status_entity import HistoricalStatus

class ParcelModel:

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

        return parcel


    def getParcelById(self, id):
        return self.db.query(Parcel).where(Parcel.id == id).first()
    

    def getAll(self):
        return self.db.query(Parcel).all()
    

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

        return history

    
    
    def assignToDeliveryMan(self,parcel_id,delivery_man_id):
        return self.db.update(Parcel.c.delivery_man_id  , delivery_man_id).where(Parcel.c.id,id)



    
    def seed_parcels(self, count : int = 10):

        if self.db.query(Parcel).count() == 0:
            print("🌱 Initialisation des 10 colis...")
            for i in range(1, count + 1):

                # Parcel

                new_parcel = Parcel(
                    description=f"Parcel {i}",
                    weight=randint(3, 50),
                    status=EnumStatus.CREATED,
                    idClient=randint(11, 20),
                    idRecipient=randint(11, 20),
                    idDeliveryMan=None,
                    DestinationCity="Rabat",
                    code=randint(1000, 99999)
                )
                self.db.add(new_parcel)
            self.db.commit()

            

            for i in range(1, count + 1):

                # Status History

                new_status = HistoricalStatus(
                    statut = EnumStatus.CREATED,
                    idParcel = i
                )
                self.db.add(new_status)

            self.db.commit()
            print("✅ 10 colis insérés avec succès.")
        else:
            print("ℹ️ Les colis existent déjà, skipping seed.")