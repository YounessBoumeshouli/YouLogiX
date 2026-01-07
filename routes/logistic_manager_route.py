import status
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from controllers.delivery_man_controller import DeliveryManController
from schemas.delivery_man  import (
    DeliveryManBase,
DeliveryManCreate,
    DeliveryManResponse,
)

router = APIRouter()

@router.get("/delivery_man")
def seed_delivery_men():
    db = get_db()
    Controller = DeliveryManController(db)
    Controller.seed_delivery_men()
    return {"message": "This route is running"}
@router.get("/delivery_man/parcels")
def showParcels( db: Session = Depends(get_db)):
    controller = DeliveryManController(db)
    return controller.fetch_percels()
@router.get("/delivery_man/parcels/{parcel_id}/assign_to_delivery_man", response_model=DeliveryManResponse)
def showParcelsByDeliveryMan(payload: DeliveryManCreate, db: Session = Depends(get_db)):
    controller = DeliveryManController(db)
    return controller.fetch_percels(payload)