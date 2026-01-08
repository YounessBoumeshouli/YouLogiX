from fastapi import APIRouter, Depends, status
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
@router.post("/delivery_man/parcels", response_model=DeliveryManResponse)
def showParcels(payload: DeliveryManCreate, db: Session = Depends(get_db)):
    controller = DeliveryManController(db)
    return controller.fetch_percels(payload)