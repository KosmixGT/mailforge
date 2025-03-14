from pydantic import BaseModel
from app.domain.models.address import Address


class AddressDTO(BaseModel):
    id: int
    type_id: int
    address: str

    @staticmethod
    def from_domain(address: Address) -> "AddressDTO":
        return AddressDTO(
            id=address.id, type_id=address.type_id, address=address.address
        )


class AddressCreateDTO(BaseModel):
    type_id: int
    address: str


class AddressUpdateDTO(AddressCreateDTO):
    pass
