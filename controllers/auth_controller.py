from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends
from app.db.database import get_db
from fastapi.security import OAuth2PasswordBearer
import bcrypt
from datetime import datetime, timedelta
from jose import jwt
from config import settings

from models.client_model import ClientModel
from models.deliveryman_model import DeliveryManModel
from entities import User, Client, DeliveryMan, LogisticsManager
from models.parcel_model import ParcelModel
from schemas.user_schema import (
    ClientCreateSchema,
    DeliveryManCreateSchema, 
    UserLoginSchema,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


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
                password=self.hash_password(data.password),
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
                password=self.hash_password(data.password),
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

        if not user or not self.verify_password(payload.password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token = self.create_access_token(
            data={"sub": str(user.id), "role": user.role}
        )

        return {
            "access_token": token,
            "token_type": "bearer"
        }
    


    def get_current_user(
        self,
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db),
    ):
        try:
            user = self.verify_access_token(token)

            if user['id'] is None:
                raise HTTPException(status_code=401)

        except Exception:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = db.get(User, user['id'])

        if not user:
            raise HTTPException(status_code=401)

        return user
    

    
    def hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed.decode("utf-8")



    def verify_password(self, password: str, hashed: str) -> bool:
        return bcrypt.checkpw(
            password.encode("utf-8"),
            hashed.encode("utf-8")
        )



    def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)



    def verify_access_token(self, token: str):
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        user_role: str = payload.get("role")

        return {'id': user_id, "role": user_role}
    


    def require_role(self, role: str):
        def checker(user: User = Depends(self.get_current_user)):
            if user.role != role:
                raise HTTPException(status_code=403, detail="Forbidden")
            return user
        return checker
