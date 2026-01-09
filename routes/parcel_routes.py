from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from entities import User
from auth.dependencies import require_roles
from controllers.parcel_controller import ParcelController
from controllers.client_controller import ClientController
from schemas.parcel_schema import (
    ParcelCreateSchema,
    ParcelResponseSchema,
    ParcelUpdateSchema
)



router = APIRouter(prefix="/parcels", tags=["Parcels"])



@router.post("", response_model=ParcelResponseSchema, status_code=status.HTTP_201_CREATED)
def create_parcel(
    payload: ParcelCreateSchema,
    db: Session = Depends(get_db),
    user : User = Depends(require_roles("client"))
):
    controller = ParcelController(db)
    return controller.create_parcel(user.id, payload)



@router.get("", response_model=list[ParcelResponseSchema])
def get_parcel(
    db: Session = Depends(get_db),
    user : User = Depends(require_roles("logistics_manager"))
):
    controller = ParcelController(db)
    return controller.get_all_parcels()



@router.put("/{parcel_id}", response_model=ParcelResponseSchema)
def update_parcel(
    parcel_id: int, 
    payload: ParcelUpdateSchema, 
    db: Session = Depends(get_db),
    user : User = Depends(require_roles("client"))
):
    controller = ParcelController(db)
    return controller.update_parcel(user.id, parcel_id, payload)

@router.get("/sent", response_model=list[ParcelResponseSchema])
def get_sent_parcels(
    db: Session = Depends(get_db),
    user : User = Depends(require_roles("client"))
):
    controller = ClientController(db)
    return controller.getSentParcels(user.id)

@router.get("/received", response_model=list[ParcelResponseSchema])
def get_received_parcels(
    db: Session = Depends(get_db),
    user : User = Depends(require_roles("client"))
):
    controller = ClientController(db)
    return controller.getReceivedParcels(user.id)

@router.get("/{parcel_id}", response_model=ParcelResponseSchema)
def get_parcel(
    parcel_id: int,
    db: Session = Depends(get_db),
    user : User = Depends(require_roles("logistics_manager"))
):
    controller = ParcelController(db)
    return controller.get_parcel(parcel_id)



@router.get("/city/{city_name}", response_model=list[ParcelResponseSchema])
def get_parcels_by_city(
    city_name: str, 
    db: Session = Depends(get_db),
    user : User = Depends(require_roles("logistics_manager"))
):
    controller = ParcelController(db)
    return controller.get_parcels_by_city(city_name)



@router.get("/status/{status}", response_model=list[ParcelResponseSchema])
def get_parcels_by_status(
    status: str,
    db: Session = Depends(get_db),
    user : User = Depends(require_roles("logistics_manager"))
):
    controller = ParcelController(db)
    return controller.get_parcels_by_status(status)