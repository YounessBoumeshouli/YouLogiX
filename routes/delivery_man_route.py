from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from entities import User
from auth.dependencies import require_roles
from controllers.delivery_man_controller import DeliveryManController
from schemas.delivery_man  import (
    DeliveryManBase,
    DeliveryManCreate,
    DeliveryManResponse,
)


router = APIRouter(prefix="/delivery_men", tags=["Delivery Men"])



@router.get("")
def get_delivery_men(
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("logistics_manager"))
):
    controller = DeliveryManController(db)
    return controller.get_all_delivery_men()



@router.post("/parcels", response_model=DeliveryManResponse)
def showParcels(
    payload: DeliveryManCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("logistics_manager"))
):
    controller = DeliveryManController(db)
    return controller.fetch_percels(payload)