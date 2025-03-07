from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from mailforge_shared.core.config.database import get_db
from app.application.dto.address import AddressDTO, AddressCreateDTO, AddressUpdateDTO
from app.application.services.address_service import AddressService
from app.infrastructure.repositories.address import PostgresAddressRepository

router = APIRouter(prefix="/addresses", tags=["address"])


async def get_address_service(db: AsyncSession = Depends(get_db)) -> AddressService:
    repository = PostgresAddressRepository(db)
    return AddressService(repository)


@router.get("/{address_id}", response_model=AddressDTO)
async def get_address(
    address_id: int, service: AddressService = Depends(get_address_service)
):
    address = await service.get_address(address_id)
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    return address


@router.get("/", response_model=List[AddressDTO])
async def get_addresses(
    skip: int = 0,
    limit: int = 100,
    service: AddressService = Depends(get_address_service),
):
    return await service.get_addresses(skip, limit)


@router.get("/by_type/{type_id}", response_model=List[AddressDTO])
async def get_addresses_by_type(
    type_id: int, service: AddressService = Depends(get_address_service)
):
    return await service.get_addresses_by_type(type_id)


@router.get("/by_address/{address_value}", response_model=List[AddressDTO])
async def get_addresses_by_address(
    address_value: str, service: AddressService = Depends(get_address_service)
):
    return await service.get_addresses_by_address(address_value)


@router.post("/create", response_model=AddressDTO)
async def create_address(
    address: AddressCreateDTO, service: AddressService = Depends(get_address_service)
):
    return await service.create_address(address)


@router.put("/update/{address_id}", response_model=AddressDTO)
async def update_address(
    address_id: int,
    address: AddressUpdateDTO,
    service: AddressService = Depends(get_address_service),
):
    updated_address = await service.update_address(address_id, address)
    if not updated_address:
        raise HTTPException(status_code=404, detail="Address not found")
    return updated_address


@router.delete("/delete/{address_id}")
async def delete_address(
    address_id: int, service: AddressService = Depends(get_address_service)
):
    if not await service.delete_address(address_id):
        raise HTTPException(status_code=404, detail="Address not found")
    return {"message": "Address deleted successfully"}
