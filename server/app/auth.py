from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from fastapi import Depends
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from app.config import settings
import app.user.crud as crud
from app.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/jwt/create/", scheme_name="JWT")

def decode_access_token(db, token):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        username: str = payload.get("sub")
        token_type: str = payload.get("type")
        
        if username is None or token_type != "access":
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception
    
    user = crud.get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user

def get_current_user(db: Session = Depends(get_db),
                    token: str = Depends(oauth2_scheme)):
    return decode_access_token(db, token)
