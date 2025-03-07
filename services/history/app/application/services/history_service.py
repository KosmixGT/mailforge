from typing import List, Optional
from datetime import datetime
from app.domain.models.history import MailingHistory
from app.domain.interfaces.history_repository import MailingHistoryRepository
from app.application.dto.history import MailingHistoryDTO, MailingHistoryCreateDTO


class MailingHistoryService:
    def __init__(self, history_repository: MailingHistoryRepository):
        self.repository = history_repository

    async def get_history(self, history_id: int) -> Optional[MailingHistoryDTO]:
        history = await self.repository.get_by_id(history_id)
        return MailingHistoryDTO.from_domain(history) if history else None

    async def get_histories_by_mailing(
        self, mailing_id: int
    ) -> List[MailingHistoryDTO]:
        histories = await self.repository.get_by_mailing_id(mailing_id)
        return [MailingHistoryDTO.from_domain(history) for history in histories]

    async def get_histories_by_user(self, user_id: int) -> List[MailingHistoryDTO]:
        histories = await self.repository.get_by_user_id(user_id)
        return [MailingHistoryDTO.from_domain(history) for history in histories]

    async def create_history(
        self, history_dto: MailingHistoryCreateDTO
    ) -> MailingHistoryDTO:
        history = MailingHistory(
            id=None,
            mailing_id=history_dto.mailing_id,
            sent_time=history_dto.sent_time,
            delivery_status_id=history_dto.delivery_status_id,
        )
        created_history = await self.repository.create(history)
        return MailingHistoryDTO.from_domain(created_history)

    async def get_history_by_mailing_and_time(
        self, mailing_id: int, sent_time: datetime
    ) -> Optional[MailingHistoryDTO]:
        history = await self.repository.get_by_mailing_and_time(mailing_id, sent_time)
        return MailingHistoryDTO.from_domain(history) if history else None
