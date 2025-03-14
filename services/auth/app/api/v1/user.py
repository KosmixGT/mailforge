from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from mailforge_shared.core.config.database import get_db
from services.auth.app.application.dto.user_dto import UserDTO, UserCreateDTO
from app.application.services.user_service import UserService
from services.auth.app.infrastructure.repositories.user_repository import (
    PostgresUserRepository,
)
from app.api.v1.auth import get_current_user

router = APIRouter(prefix="/users", tags=["user"])


async def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    repository = PostgresUserRepository(db)
    return UserService(repository)


@router.post("/register", response_model=UserDTO)
async def register_user(
    user: UserCreateDTO, service: UserService = Depends(get_user_service)
):
    return await service.create_user(user)


@router.get("/me", response_model=UserDTO)
async def get_current_user_info(current_user: UserDTO = Depends(get_current_user)):
    return current_user


@router.get("/{user_id}", response_model=UserDTO)
async def get_user(user_id: int, service: UserService = Depends(get_user_service)):
    user = await service.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
