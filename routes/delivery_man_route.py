from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from controllers.delivery_man_controller import seed_delivery_men

router = APIRouter()

@router.get("/delivery_man")
def seed_delivery_men():
    seed_delivery_men()
    return {"message": "This route is running"}