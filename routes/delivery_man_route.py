import status
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from controllers.delivery_man_controller import DeliveryManController
from schemas.delivery_man  import (
    DeliveryManBase,
    DeliveryManResponse,
)

router = APIRouter()

@router.get("/delivery_man")
def seed_delivery_men():
    db = get_db()
    Controller = DeliveryManController(db)
    Controller.seed_delivery_men()
    return {"message": "This route is running"}
@router.post("/delivery_man/parcels", response_model=DeliveryManResponse, status_code=status.HTTP_201_CREATED)
def showParcels(payload: DeliveryManController, db: Session = Depends(get_db)):
    controller = DeliveryManController(db)
    return controller.fetch_percels()