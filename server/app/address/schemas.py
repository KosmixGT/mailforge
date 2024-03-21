from typing import Optional
from pydantic import BaseModel

class AddressBase(BaseModel):
    addressid: int
    typeid: int
    address: str


    class Config:
        orm_mode = True


class AddressCreate(BaseModel):
    typeid: int
    address: str

    class Config:
        orm_mode = True