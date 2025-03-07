from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models.address import Address


class AddressRepository(ABC):
    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[Address]:
        pass

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Address]:
        pass

    @abstractmethod
    async def get_by_type(self, type_id: int) -> List[Address]:
        pass

    @abstractmethod
    async def get_by_address(self, address: str) -> List[Address]:
        pass

    @abstractmethod
    async def create(self, address: Address) -> Address:
        pass

    @abstractmethod
    async def update(self, address: Address) -> Optional[Address]:
        pass

    @abstractmethod
    async def delete(self, id: int) -> bool:
        pass
