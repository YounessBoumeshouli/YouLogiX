from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from controllers.auth_controller import AuthController
from schemas.user_schema import (
    ClientCreateSchema,
    DeliveryManCreateSchema
)

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
def create_client(
    payload: ClientCreateSchema | DeliveryManCreateSchema,
    db: Session = Depends(get_db)
):
    controller = AuthController()
    return controller.register(payload, db)


