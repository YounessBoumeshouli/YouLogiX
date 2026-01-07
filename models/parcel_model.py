from entities.parcel_entity import Parcel

class ParcelModel:

    def __init__(self, db):
        self.db = db

    def createParcel(self, description: str, weight: float, status: str, idDeliveryMan: int, idClient: int, idRecipient: int, city: str, code: str):
        parcel = Parcel(
            description = description,
            weight = weight,
            status = status,
            idDeliveryMan = idDeliveryMan,
            idClient = idClient,
            idRecipient = idRecipient,
            DestinationCity = city,
            code = code
        )

        self.db.add(parcel)
        self.db.commit()
        self.db.refresh(parcel)

        return parcel

    def getParcel(self,id):
        return self.db.query(Parcel).where(Parcel.c.id,id)
    
    def assignToDeliveryMan(self,parcel_id,delivery_man_id):
        return self.db.update(Parcel.c.delivery_man_id  , delivery_man_id).where(Parcel.c.id,id)

