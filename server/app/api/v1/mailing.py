from typing import List
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database.base import get_db
from app.application.dto.mailing import MailingDTO, MailingCreateDTO
from app.application.services.mailing_service import MailingService
from app.application.services.file_processing_service import FileProcessingService
from app.infrastructure.repositories.mailing import PostgresMailingRepository
from app.api.v1.auth import get_current_user
from app.domain.models.user import User

router = APIRouter(prefix="/mailings", tags=["mailing"])


async def get_mailing_service(db: AsyncSession = Depends(get_db)) -> MailingService:
    repository = PostgresMailingRepository(db)
    return MailingService(repository)


@router.get("/{mailing_id}", response_model=MailingDTO)
async def get_mailing(
    mailing_id: int, service: MailingService = Depends(get_mailing_service)
):
    mailing = await service.get_mailing(mailing_id)
    if not mailing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mailing with id {mailing_id} not found",
        )
    return MailingDTO.from_domain(mailing)


@router.get("/", response_model=List[MailingDTO])
async def get_mailings(
    skip: int = 0,
    limit: int = 100,
    service: MailingService = Depends(get_mailing_service),
    current_user: User = Depends(get_current_user),
):
    return await service.get_mailings(skip, limit)


@router.get("/by_user/{user_id}", response_model=List[MailingDTO])
async def get_mailings_by_user_id(
    user_id: int, service: MailingService = Depends(get_mailing_service)
):
    return await service.get_mailings_by_user_id(user_id)


@router.post("/create", response_model=MailingDTO)
async def create_mailing(
    mailing: MailingCreateDTO,
    service: MailingService = Depends(get_mailing_service),
    current_user: User = Depends(get_current_user),
):
    return await service.create_mailing(mailing, current_user.id)


@router.put("/update/{mailing_id}", response_model=MailingDTO)
async def update_mailing(
    mailing_id: int,
    mailing: MailingCreateDTO,
    service: MailingService = Depends(get_mailing_service),
):
    updated_mailing = await service.update_mailing(mailing_id, mailing)
    if not updated_mailing:
        raise HTTPException(status_code=404, detail="Mailing not found")
    return updated_mailing


@router.delete("/delete/{mailing_id}")
async def delete_mailing(
    mailing_id: int, service: MailingService = Depends(get_mailing_service)
):
    if not await service.delete_mailing(mailing_id):
        raise HTTPException(status_code=404, detail="Mailing not found")
    return {"message": "Mailing deleted successfully"}


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    service: MailingService = Depends(get_mailing_service),
    file_service: FileProcessingService = Depends(),
    current_user: User = Depends(get_current_user),
):
    if not file.filename.endswith((".csv", ".xls", ".xlsx")):
        raise HTTPException(
            status_code=400, detail="Допустимые форматы файлов: CSV, XLS, XLSX"
        )

    contents = await file.read()
    mailings = await file_service.process_file(contents, file.filename)

    for mailing in mailings:
        await service.create_mailing(mailing, current_user.id)

    return {"message": "Файл успешно загружен и данные добавлены в базу данных"}
