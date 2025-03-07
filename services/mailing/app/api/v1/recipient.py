from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from mailforge_shared.core.config.database import get_db
from app.application.dto.recipient import RecipientDTO, RecipientCreateDTO
from app.application.services.recipient_service import RecipientService
from app.infrastructure.repositories.recipient import PostgresRecipientRepository

router = APIRouter(prefix="/recipients", tags=["recipient"])


async def get_recipient_service(db: AsyncSession = Depends(get_db)) -> RecipientService:
    repository = PostgresRecipientRepository(db)
    return RecipientService(repository)


@router.get("/{recipient_id}", response_model=RecipientDTO)
async def get_recipient(
    recipient_id: int, service: RecipientService = Depends(get_recipient_service)
):
    recipient = await service.get_recipient(recipient_id)
    if not recipient:
        raise HTTPException(status_code=404, detail="Recipient not found")
    return recipient


@router.get("/", response_model=List[RecipientDTO])
async def get_recipients(
    skip: int = 0,
    limit: int = 100,
    service: RecipientService = Depends(get_recipient_service),
):
    return await service.get_recipients(skip, limit)


@router.post("/create", response_model=RecipientDTO)
async def create_recipient(
    recipient: RecipientCreateDTO,
    service: RecipientService = Depends(get_recipient_service),
):
    return await service.create_recipient(recipient)


@router.get("/by_mailing/{mailing_id}", response_model=List[RecipientDTO])
async def get_recipients_by_mailing(
    mailing_id: int, service: RecipientService = Depends(get_recipient_service)
):
    return await service.get_recipients_by_mailing(mailing_id)


@router.get("/load_recipients/{history_id}", response_model=List[RecipientDTO])
async def load_recipients_from_history(
    history_id: int, service: RecipientService = Depends(get_recipient_service)
):
    return await service.get_recipients_by_history(history_id)
