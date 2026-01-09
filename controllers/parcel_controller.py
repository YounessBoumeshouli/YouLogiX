from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from random import randint

from models.parcel_model import ParcelModel
from entities.enums.status_enum import EnumStatus
from schemas.parcel_schema import ParcelCreateSchema, ParcelUpdateSchema


class ParcelController:

    def __init__(self, db: Session):
        self.model = ParcelModel(db)

    # Create a parcel

    def create_parcel(self, client_id: int, payload: ParcelCreateSchema):
        code = randint(1000, 999999999)
        return self.model.createParcel(client_id=client_id, **payload.model_dump(), code=code)



    # Get a parcel

    def get_parcel(self, parcel_id: int):
        parcel = self.model.getParcelById(parcel_id)
        if not parcel:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Parcel not found"
            )
        return parcel
    

    
    # Get all parcels

    def get_all_parcels(self):
        return self.model.getAll()
    


    # Filter Parcels by city

    def get_parcels_by_city(self, city_name: str):
        return self.model.getParcelsByCity(city_name)
    


    # Filter parcels by status

    def get_parcels_by_status(self, status: str):
        upper_status = status.upper()
        return self.model.getParcelsByStatus(upper_status)
    


    # Update a parcel 

    def update_parcel(self, current_id, parcel_id: int, payload: ParcelUpdateSchema):

        parcel = self.model.getParcelById(parcel_id)

        if parcel.idClient != current_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You are not authorized to perform this action"
            )
        
        if not parcel:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Parcel not found"
            )
        
        if parcel.status != EnumStatus.CREATED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Can't update a parcel after it's been approved"
            )

        return self.model.updateParcel(parcel, **payload.model_dump(exclude_unset=True))