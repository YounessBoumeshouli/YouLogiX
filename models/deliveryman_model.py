import User
import Parcel
import etities.deliveryman_entity
from entities.enums.Parcel_enum import Parcel_enum

class Deliveryman(User):

    def assignParcel(self , parcel_id)->bool:
        parcel =  Parcel.getParcel(parcel_id)
        return 0 if parcel.status == Parcel_enum.LIVRED else 1
