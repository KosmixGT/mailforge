from typing import List, Optional
from app.domain.models.address import Address
from app.domain.interfaces.address_repository import AddressRepository
from app.application.dto.address import AddressDTO, AddressCreateDTO, AddressUpdateDTO


class AddressService:
    def __init__(self, address_repository: AddressRepository):
        self.repository = address_repository

    async def get_address(self, address_id: int) -> Optional[AddressDTO]:
        address = await self.repository.get_by_id(address_id)
        return AddressDTO.from_domain(address) if address else None

    async def get_addresses(self, skip: int = 0, limit: int = 100) -> List[AddressDTO]:
        addresses = await self.repository.get_all(skip, limit)
        return [AddressDTO.from_domain(address) for address in addresses]

    async def get_addresses_by_type(self, type_id: int) -> List[AddressDTO]:
        addresses = await self.repository.get_by_type(type_id)
        return [AddressDTO.from_domain(address) for address in addresses]

    async def get_addresses_by_address(self, address: str) -> List[AddressDTO]:
        addresses = await self.repository.get_by_address(address)
        return [AddressDTO.from_domain(address) for address in addresses]

    async def create_address(self, address_dto: AddressCreateDTO) -> AddressDTO:
        address = Address(
            id=None, type_id=address_dto.type_id, address=address_dto.address
        )
        created_address = await self.repository.create(address)
        return AddressDTO.from_domain(created_address)

    async def update_address(
        self, address_id: int, address_dto: AddressUpdateDTO
    ) -> Optional[AddressDTO]:
        existing_address = await self.repository.get_by_id(address_id)
        if not existing_address:
            return None

        updated_address = Address(
            id=address_id, type_id=address_dto.type_id, address=address_dto.address
        )

        result = await self.repository.update(updated_address)
        return AddressDTO.from_domain(result) if result else None

    async def delete_address(self, address_id: int) -> bool:
        return await self.repository.delete(address_id)
