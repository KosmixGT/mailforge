from typing import Optional
from pydantic import ConfigDict, BaseModel

class RecipientBase(BaseModel):
    recipientid: int
    mailingid: int
    addressid: int
    deliverystatusid: Optional[int] = None
    historyid: int
    model_config = ConfigDict(from_attributes=True)

class RecipientCreate(BaseModel):
    mailingid: int
    addressid: int
    deliverystatusid: Optional[int] = None
    historyid: int
    model_config = ConfigDict(from_attributes=True)
