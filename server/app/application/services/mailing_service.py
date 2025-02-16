from datetime import datetime
from typing import List
from app.domain.interfaces.repositories.mailing import MailingRepository
from app.domain.models.mailing import Mailing
from app.application.dto.mailing import MailingDTO, MailingCreateDTO


class MailingService:
    def __init__(self, mailing_repository: MailingRepository):
        self.repository = mailing_repository

    async def get_mailing(self, mailing_id: int) -> MailingDTO:
        mailing = await self.repository.get_by_id(mailing_id)
        return MailingDTO.from_domain(mailing)

    async def get_mailings(self, skip: int = 0, limit: int = 100) -> List[MailingDTO]:
        mailings = await self.repository.get_all(skip, limit)
        return [MailingDTO.from_domain(mailing) for mailing in mailings]

    async def get_mailings_by_user_id(self, user_id: int) -> List[MailingDTO]:
        mailings = await self.repository.get_by_user_id(user_id)
        return [MailingDTO.from_domain(mailing) for mailing in mailings]

    async def create_mailing(
        self, mailing_dto: MailingCreateDTO, user_id: int
    ) -> MailingDTO:
        mailing = Mailing(
            id=None,
            title=mailing_dto.title,
            message_text=mailing_dto.message_text,
            user_id=user_id,
            scheduled_time=mailing_dto.scheduled_time or datetime.now(),
            status_id=1,
        )
        created_mailing = await self.repository.create(mailing)
        return MailingDTO.from_domain(created_mailing)

    async def update_mailing(
        self, mailing_id: int, mailing_dto: MailingCreateDTO
    ) -> MailingDTO:
        existing_mailing = await self.repository.get_by_id(mailing_id)
        if not existing_mailing:
            return None

        updated_mailing = Mailing(
            id=mailing_id,
            title=mailing_dto.title,
            message_text=mailing_dto.message_text,
            user_id=existing_mailing.user_id,
            scheduled_time=mailing_dto.scheduled_time
            or existing_mailing.scheduled_time,
            status_id=existing_mailing.status_id,
        )

        result = await self.repository.update(updated_mailing)
        return MailingDTO.from_domain(result)

    async def delete_mailing(self, mailing_id: int) -> bool:
        return await self.repository.delete(mailing_id)
