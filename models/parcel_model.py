from sqlalchemy.orm.session import Session

from entities.parcel_entity import Parcel

from entities.enums.status_enum import EnumStatus

class Parcel :
    def __init__(self, db: Session):
        self.db = db
    def getParcel(self,id):
        return self.db.query(Parcel).where(Parcel.c.id,id)
    def assignToDeliveryMan(self,parcel_id,delivery_man_id):
        return self.db.update(Parcel.c.delivery_man_id  , delivery_man_id).where(Parcel.c.id,id)

    def assignParcel(parcel_id)->bool:
        parcel =  Parcel.getParcel(parcel_id)
        return 0 if parcel.status == EnumStatus.LIVRED else 1
