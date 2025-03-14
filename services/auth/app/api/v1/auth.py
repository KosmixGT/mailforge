from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError
from mailforge_shared.core.config.settings import settings
from mailforge_shared.core.config.database import get_db
from app.application.services.user_service import UserService
from services.auth.app.infrastructure.repositories.user_repository import PostgresUserRepository
from mailforge_shared.core.utils.token_utils import TokenHelper

router = APIRouter(prefix="/auth", tags=["authorization"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/jwt/create")


async def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    repository = PostgresUserRepository(db)
    return UserService(repository)


async def decode_access_token(db: AsyncSession, token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = TokenHelper.decode_token(token)
        username: str = payload.get("sub")
        token_type: str = payload.get("type")

        if username is None or token_type != "access":
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user_service = UserService(PostgresUserRepository(db))
    user = await user_service.get_by_username(username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_user(
    db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    return await decode_access_token(db, token)


@router.post("/jwt/create")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: UserService = Depends(get_user_service),
):
    user = await service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = await TokenHelper.create_token(
        data={"sub": user.name, "type": "access"},
        expires_delta=timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRES_MINUTES)),
    )

    refresh_token = await TokenHelper.create_token(
        data={"sub": user.name, "type": "refresh"}, expires_delta=timedelta(days=30)
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer",
        "user": user,
    }


@router.post("/jwt/refresh")
async def refresh_token(
    token: str = Depends(oauth2_scheme),
    service: UserService = Depends(get_user_service),
):
    try:
        payload = TokenHelper.decode_token(token)
        username: str = payload.get("sub")
        token_type: str = payload.get("type")

        if token_type != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
            )

        user = await service.get_by_username(username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
            )

        access_token = await TokenHelper.create_token(
            data={"sub": username, "type": "access"},
            expires_delta=timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRES_MINUTES)),
        )
        return {"access_token": access_token}

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )
