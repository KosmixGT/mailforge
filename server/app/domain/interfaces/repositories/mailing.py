from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models.mailing import Mailing


class MailingRepository(ABC):
    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[Mailing]:
        pass

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Mailing]:
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> List[Mailing]:
        pass

    @abstractmethod
    async def create(self, mailing: Mailing) -> Mailing:
        pass

    @abstractmethod
    async def update(self, mailing: Mailing) -> Optional[Mailing]:
        pass

    @abstractmethod
    async def delete(self, id: int) -> bool:
        pass
