from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from typing import Optional
from app.database import get_db
import app.user.crud as crud
from app.password_hashing import Hash
from fastapi.encoders import jsonable_encoder
from app.config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(settings.ACCESS_TOKEN_EXPIRES_MINUTES)
REFRESH_TOKEN_EXPIRE_DAYS = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/jwt/create")
router = APIRouter(prefix='/user', tags=['authorization'])

def create_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post('/jwt/create/')
async def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db=db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_token(
        data={"sub": user.name, "type": "access"},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = create_token(
        data={"sub": user.name, "type": "refresh"},
        expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )
    
    response = {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer",
        "user_data": {
            "id": user.userid,
            "username": user.name,
            "email": user.email,
            "userrole": user.roleid,
        }
    }
    
    return jsonable_encoder(response)

@router.get('/jwt/refresh/')
async def refresh(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        token_type: str = payload.get("type")

        if token_type != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )

        # Проверка на истечение срока действия
        if datetime.now(timezone.utc) > datetime.fromtimestamp(payload["exp"], timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token expired"
            )
            
        new_access_token = create_token(
            data={"sub": username, "type": "access"},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        return {"access_token": new_access_token}
    
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )


def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db=db, username=username)
    if not user:
        user = crud.get_user_by_email(db=db, user_email=username)
        if not user:
            return False
    if not Hash.verify_hashed_password(plain_password=password, hashed_password=user.password):
        return False
    return user
