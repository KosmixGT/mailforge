from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from mailforge_shared.core.config.database import get_db
from app.application.dto.history import MailingHistoryDTO, MailingHistoryCreateDTO
from app.application.services.history_service import MailingHistoryService
from app.infrastructure.repositories.history import PostgresMailingHistoryRepository

router = APIRouter(prefix="/history", tags=["mailing_history"])


async def get_history_service(
    db: AsyncSession = Depends(get_db),
) -> MailingHistoryService:
    repository = PostgresMailingHistoryRepository(db)
    return MailingHistoryService(repository)


@router.get("/{history_id}", response_model=MailingHistoryDTO)
async def get_mailing_history(
    history_id: int, service: MailingHistoryService = Depends(get_history_service)
):
    history = await service.get_history(history_id)
    if not history:
        raise HTTPException(status_code=404, detail="Mailing history not found")
    return history


@router.get("/by_user/{user_id}", response_model=List[MailingHistoryDTO])
async def get_mailing_histories_by_user(
    user_id: int, service: MailingHistoryService = Depends(get_history_service)
):
    return await service.get_histories_by_user(user_id)


@router.post("/create", response_model=MailingHistoryDTO)
async def create_mailing_history(
    history: MailingHistoryCreateDTO,
    service: MailingHistoryService = Depends(get_history_service),
):
    return await service.create_history(history)
