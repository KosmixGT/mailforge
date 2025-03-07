from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from mailforge_shared.core.config.database import get_db
from mailforge_shared.core.interfaces.message_queue import MessageQueue
from app.application.services.mailing_service import MailingService
from app.infrastructure.repositories.mailing import PostgresMailingRepository

async def get_mailing_service(
    message_queue: MessageQueue,
    db: AsyncSession = Depends(get_db)
) -> MailingService:
    repository = PostgresMailingRepository(db)
    return MailingService(repository, message_queue)
