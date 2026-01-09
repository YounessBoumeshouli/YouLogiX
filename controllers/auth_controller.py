from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from app.db.database import get_db
from auth.helpers import hash_password

from models.client_model import ClientModel
from models.deliveryman_model import DeliveryManModel
from entities import User, Client, DeliveryMan, LogisticsManager
from models.parcel_model import ParcelModel
from schemas.user_schema import ClientCreateSchema, DeliveryManCreateSchema

class AuthController:

    def register(
        self,
        data: ClientCreateSchema | DeliveryManCreateSchema, 
        db: Session = Depends(get_db)
    ):
        
        result = db.query(User).where(User.email == data.email).first()

        if result:
            raise HTTPException(400, "Email already registered")

        if data.role == "client":

            client_model = ClientModel(db)
            user = client_model.create(
                first_name=data.first_name,
                last_name=data.last_name,
                email=data.email,
                password=hash_password("password"),
                phone=data.phone,
                role=data.role,
                address=data.address,
            )

        elif data.role == "delivery_man":

            delivery_man_model = DeliveryManModel(db)
            user = delivery_man_model.create(
                first_name=data.first_name,
                last_name=data.last_name,
                email=data.email,
                password=hash_password("password"),
                phone=data.phone,
                role=data.role,
                address=data.address,
                vehicule=data.vehicule
            )

        else:
            raise HTTPException(400, "Invalid role")


        return {
            "message": "User registered successfully",
            "user_id": user.id,
            "user_name": f"{user.first_name} {user.last_name}",
            "role": user.role
        }