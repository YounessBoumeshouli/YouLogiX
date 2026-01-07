from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from controllers.parcel_controller import ParcelController
from schemas.parcel_schema import (
    ParcelCreateSchema,
    ParcelResponseSchema,
)

router = APIRouter(prefix="/parcels", tags=["Parcels"])

@router.post("", response_model=ParcelResponseSchema, status_code=status.HTTP_201_CREATED)
def create_parcel(payload: ParcelCreateSchema, db: Session = Depends(get_db)):
    controller = ParcelController(db)
    return controller.create_parcel(payload)



@router.get("", response_model=list[ParcelResponseSchema])
def get_parcel(db: Session = Depends(get_db)):
    controller = ParcelController(db)
    return controller.get_all_parcels()



@router.get("/{parcel_id}", response_model=ParcelResponseSchema)
def get_parcel(parcel_id: int, db: Session = Depends(get_db)):
    controller = ParcelController(db)
    return controller.get_parcel(parcel_id)
