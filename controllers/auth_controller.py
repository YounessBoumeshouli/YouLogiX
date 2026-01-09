from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends
from app.db.database import get_db
from auth.security import hash_password, verify_password, create_access_token

from models.client_model import ClientModel
from models.deliveryman_model import DeliveryManModel
from entities import User
from schemas.user_schema import (
    ClientCreateSchema,
    DeliveryManCreateSchema, 
    UserLoginSchema,
)



class AuthController:

    ### Register

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
                password=hash_password(data.password),
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
                password=hash_password(data.password),
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
    


    ### Login
        
    def login(
        self,
        payload: UserLoginSchema,
        db: Session = Depends(get_db),
    ):
        user = db.query(User).where(User.email == payload.email).first()

        if not user or not verify_password(payload.password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token = create_access_token(
            data={"sub": str(user.id), "role": user.role}
        )

        return {
            "access_token": token,
            "token_type": "bearer"
        }
    


    