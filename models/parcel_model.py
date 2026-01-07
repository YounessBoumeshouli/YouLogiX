from sqlalchemy.orm.session import Session

from entities.parcel_entity import Parcel

from entities.enums.status_enum import EnumStatus
from schemas import delivery_man


class Parcel :
    def __init__(self, db: Session):
        self.db = db

    def getParcel(self,id):
        return self.db.query(Parcel).where(Parcel.c.id,id)
    def getParcelByDeliveryMan(self, delivery_man_id):
        return self.db.query(Parcel).where(delivery_man.c.id,delivery_man_id)
    def assignToDeliveryMan(self,parcel_id,delivery_man_id):
        return self.db.update(Parcel.c.delivery_man_id  , delivery_man_id).where(Parcel.c.id,id)

    def assignParcel(parcel_id)->bool:
        parcel =  Parcel.getParcel(parcel_id)
        return 0 if parcel.status == EnumStatus.LIVRED else 1



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


    def getParcelById(self, id) -> Parcel:
        return self.db.query(Parcel).where(Parcel.id == id).first()
    

    def getAll(self) -> list[Parcel]:
        return self.db.query(Parcel).all()
    

    
    def updateParcel(self, parcel: Parcel, **kwargs):

        for key, value in kwargs.items():
            if hasattr(parcel, key):
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

