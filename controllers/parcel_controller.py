from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models.parcel_model import ParcelModel
from schemas.client_schema import ClientCreateSchema


class ParcelController:

    def __init__(self, db: Session):
        self.model = ParcelModel(db)

    # Create a parcel

    def create_parcel(self, payload):
        return self.model.create(**payload.model_dump())
