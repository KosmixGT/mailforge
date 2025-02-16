from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models.history import MailingHistory
from datetime import datetime


class MailingHistoryRepository(ABC):
    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[MailingHistory]:
        pass

    @abstractmethod
    async def get_by_mailing_id(self, mailing_id: int) -> List[MailingHistory]:
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> List[MailingHistory]:
        pass

    @abstractmethod
    async def create(self, history: MailingHistory) -> MailingHistory:
        pass

    @abstractmethod
    async def get_by_mailing_and_time(
        self, mailing_id: int, sent_time: datetime
    ) -> Optional[MailingHistory]:
        pass
