import User
import Parcel
from entities.parcel_entity import Parcel

import etities.deliveryman_entity
from entities.enums.Parcel_enum import Parcel_enum


def getParcel(id):
    return db.query(Parcel).where(Parcel.c.id,id)
def assignToDeliveryMan(parcel_id,delivery_man_id):
    return db.update(Parcel.c.delivery_man_id  , delivery_man_id).where(Parcel.c.id,id)

def assignParcel(parcel_id)->bool:
    parcel =  Parcel.getParcel(parcel_id)
    return 0 if parcel.status == Parcel_enum.LIVRED else 1
