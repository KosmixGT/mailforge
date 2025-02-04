from typing import Optional
from pydantic import ConfigDict, BaseModel

class AddressBase(BaseModel):
    addressid: int
    typeid: int
    address: str
    model_config = ConfigDict(from_attributes=True)


class AddressCreate(BaseModel):
    typeid: int
    address: str
    model_config = ConfigDict(from_attributes=True)