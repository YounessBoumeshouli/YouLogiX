from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from entities import User
from auth.dependencies import require_roles
from controllers.logistic_manager_controller import LogisticMangerController
from controllers.delivery_man_controller import DeliveryManController
from schemas.delivery_man  import (
    DeliveryManBase,
    DeliveryManCreate,
    DeliveryManResponse,
)
from schemas.user_schema import UserReadSchema

router = APIRouter(tags=["Logistics Managers"])

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

@router.get("/parcels/{parcel_id}/assign_to_delivery_man")
def showParcelsByDeliveryMan(
    parcel_id,
    db: Session = Depends(get_db),
    user : User = Depends(require_roles("logistics_manager"))
):
    controller = LogisticMangerController(db)
    return controller.assignParcel(parcel_id)



@router.get("/users", response_model=list[UserReadSchema])
def getUsers(
    db: Session = Depends(get_db),
    user : User = Depends(require_roles("logistics_manager"))
):
    controller = LogisticMangerController(db)
    return controller.getAllUsers()