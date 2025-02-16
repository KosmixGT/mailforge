from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models.recipient import Recipient


class RecipientRepository(ABC):
    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[Recipient]:
        pass

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Recipient]:
        pass

    @abstractmethod
    async def create(self, recipient: Recipient) -> Recipient:
        pass

    @abstractmethod
    async def get_by_mailing_id(self, mailing_id: int) -> List[Recipient]:
        pass

    @abstractmethod
    async def get_by_history_id(self, history_id: int) -> List[Recipient]:
        pass
