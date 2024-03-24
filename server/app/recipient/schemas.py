from typing import Optional
from pydantic import BaseModel

class RecipientBase(BaseModel):
    recipientid: int
    mailingid: int
    addressid: int
    deliverystatusid: Optional[int]
    historyid: int

    class Config:
        orm_mode = True

class RecipientCreate(BaseModel):
    mailingid: int
    addressid: int
    deliverystatusid: Optional[int]
    historyid: int
    
    class Config:
        orm_mode = True
