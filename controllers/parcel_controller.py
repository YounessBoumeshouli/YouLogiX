from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from random import randint

from models.parcel_model import ParcelModel
from schemas.parcel_schema import ParcelCreateSchema


class ParcelController:

    def __init__(self, db: Session):
        self.model = ParcelModel(db)

    # Create a parcel

    def create_parcel(self, payload: ParcelCreateSchema):
        code = randint(1000, 999999999)
        return self.model.createParcel(**payload.model_dump(), code=code)



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