from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from controllers.client_controller import fetch_users

router = APIRouter()

@router.get("/clients")
def read_users(db: Session = Depends(get_db)):
    return fetch_users(db)