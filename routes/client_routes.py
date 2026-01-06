from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from controllers.client_controller import ClientController
from schemas.client_schema import (
    ClientCreateSchema,
    ClientResponseSchema,
)

router = APIRouter(prefix="/clients", tags=["Clients"])

@router.post("", response_model=ClientResponseSchema, status_code=status.HTTP_201_CREATED)
def create_client(payload: ClientCreateSchema, db: Session = Depends(get_db)):
    controller = ClientController(db)
    return controller.create_client(payload)



@router.get("", response_model=list[ClientResponseSchema])
def get_clients(db: Session = Depends(get_db)):
    controller = ClientController(db)
    return controller.get_all_clients()



@router.get("/{client_id}", response_model=ClientResponseSchema)
def get_client(client_id: int, db: Session = Depends(get_db)):
    controller = ClientController(db)
    return controller.get_client(client_id)
