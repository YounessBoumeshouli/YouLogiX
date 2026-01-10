from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from schemas.parcel_schema import ParcelResponseSchema
from models.deliveryman_model import DeliveryManModel
from models.parcel_model import ParcelModel
from models.parcel_model import Parcel
from entities.enums.status_enum import EnumStatus

class DeliveryManController:
    def __init__(self, db:Session):
        self.db = db
        self.delivery_man_model  = DeliveryManModel(db)
        self.parcel_model  = ParcelModel(db)



    def get_all_delivery_men(self):
        return self.delivery_man_model.get_all()
    


    def seed_delivery_men(self):
        self.delivery_man_model.seed_delivery_men()



    def fetch_percels(self  ):
        percels = self.delivery_man_model.get_all_parcels()
        return [1,2,4]
    


    def fetch_my_parcels(self, delivery_man_id):
        my_parcels=self.parcel_model.getParcelsByDeliveryMan(delivery_man_id)
        return my_parcels
    


    def deliverParcel(self, delivery_man_id, parcel_id):
        parcel = self.parcel_model.getParcelById(parcel_id)

        if not parcel:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Parcel not found",
            )
        
        if parcel.idDeliveryMan != delivery_man_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to perform this action",
            )

        self.parcel_model.updateParcelStatus(parcel_id, 'DELIVERED')



    def isAssigned(self ,delivery_man_id ,  parcel_id)->bool:
        parcel =  Parcel.getParcelByDeliveryMan(delivery_man_id)
        return False if parcel.status == EnumStatus.LIVRED else True
