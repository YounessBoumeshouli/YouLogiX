from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from controllers.client_controller import fetch_users

router = APIRouter()

@router.get("/clients")
def read_users():
    return {"message": "This route is running"}