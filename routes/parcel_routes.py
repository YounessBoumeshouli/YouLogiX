from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from controllers.parcel_controller import ParcelController
from schemas.client_schema import (
    ClientCreateSchema,
    ClientResponseSchema,
)

router = APIRouter(prefix="/parcels", tags=["Parcels"])

@router.post("", status_code=status.HTTP_201_CREATED)
def create_parcel(payload, db: Session = Depends(get_db)):
    controller = ParcelController(db)
    return controller.create_parcel(payload)
