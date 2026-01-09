from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from controllers.auth_controller import AuthController
from entities import User
from schemas.user_schema import (
    ClientCreateSchema,
    DeliveryManCreateSchema,
    UserLoginSchema,
    UserLoginResponseSchema,
    UserTokenSchema
)
from auth.dependencies import get_current_user, require_roles

router = APIRouter(prefix="/auth", tags=["Auth"])



@router.post("/register", status_code=status.HTTP_201_CREATED)
def create_user(
    payload: ClientCreateSchema | DeliveryManCreateSchema,
    db: Session = Depends(get_db)
):
    controller = AuthController()
    return controller.register(payload, db)



@router.post("/login", response_model=UserLoginResponseSchema)
def log_user_in(
    payload: UserLoginSchema,
    db: Session = Depends(get_db)
):
    controller = AuthController()
    return controller.login(payload, db)



@router.post('/user')
def get_current_user(payload: UserTokenSchema, db: Session = Depends(get_db)):
    return get_current_user(payload.token, db)



# @router.get("/admin/dashboard")
# def admin_dashboard(
#     user : User = Depends(require_roles("client"))
# ):
#     return {"ok": True, "user": user}