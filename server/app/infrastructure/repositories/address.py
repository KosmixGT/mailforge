from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.interfaces.repositories.address import AddressRepository
from app.domain.models.address import Address
from app.infrastructure.database.models.address import AddressModel


class PostgresAddressRepository(AddressRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: int) -> Optional[Address]:
        result = await self.session.execute(
            select(AddressModel).where(AddressModel.addressid == id)
        )
        db_address = result.scalar_one_or_none()
        return db_address.to_domain() if db_address else None

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Address]:
        result = await self.session.execute(
            select(AddressModel).offset(skip).limit(limit)
        )
        return [address.to_domain() for address in result.scalars().all()]

    async def get_by_type(self, type_id: int) -> List[Address]:
        result = await self.session.execute(
            select(AddressModel).where(AddressModel.typeid == type_id)
        )
        return [address.to_domain() for address in result.scalars().all()]

    async def get_by_address(self, address: str) -> List[Address]:
        result = await self.session.execute(
            select(AddressModel).where(AddressModel.address == address)
        )
        return [address.to_domain() for address in result.scalars().all()]

    async def create(self, address: Address) -> Address:
        db_address = AddressModel.from_domain(address)
        self.session.add(db_address)
        await self.session.commit()
        await self.session.refresh(db_address)
        return db_address.to_domain()

    async def update(self, address: Address) -> Optional[Address]:
        db_address = await self.session.get(AddressModel, address.id)
        if db_address:
            updated = AddressModel.from_domain(address)
            for key, value in updated.__dict__.items():
                if key != "_sa_instance_state":
                    setattr(db_address, key, value)
            await self.session.commit()
            return db_address.to_domain()
        return None

    async def delete(self, id: int) -> bool:
        db_address = await self.session.get(AddressModel, id)
        if db_address:
            await self.session.delete(db_address)
            await self.session.commit()
            return True
        return False
