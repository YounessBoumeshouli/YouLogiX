from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from models.client_model import ClientModel
from schemas.client_schema import (
    ClientCreateSchema,
    ClientResponseSchema,
)

router = APIRouter(prefix="/clients", tags=["Clients"])

@router.post("", response_model=ClientResponseSchema, status_code=status.HTTP_201_CREATED)
def create_client(payload: ClientCreateSchema, db: Session = Depends(get_db)):

    model = ClientModel(db)

    existing_client = model.get_by_email(payload.email)

    if existing_client:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Client with this email already exists",
        )

    return model.create(**payload.model_dump())



@router.get("", response_model=list[ClientResponseSchema])
def get_clients(db: Session = Depends(get_db)):

    model = ClientModel(db)
    return model.get_all()



@router.get("/{client_id}", response_model=ClientResponseSchema)
def get_client_by_id(client_id: int, db: Session = Depends(get_db)):

    model = ClientModel(db)
    client = model.get_by_id(client_id)

    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found",
        )

    return client

