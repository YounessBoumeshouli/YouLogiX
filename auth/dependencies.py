from fastapi import HTTPException, Depends
from entities import User
from app.db.database import get_db
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from auth.security import verify_access_token



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")



def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db),
    ):
        try:
            user = verify_access_token(token)

            if user['id'] is None:
                raise HTTPException(status_code=401)

        except Exception:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = db.get(User, user['id'])

        if not user:
            raise HTTPException(status_code=401)

        return user
    
    

def require_roles(*roles: str):
    def checker(user: User = Depends(get_current_user)):
        if user.role not in roles:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return checker
