from typing import Optional
from datetime import datetime
from pydantic import ConfigDict, BaseModel

class MailingHistoryBase(BaseModel):
    historyid: int
    mailingid: int
    senttime: datetime
    deliverystatusid: int
    model_config = ConfigDict(from_attributes=True)

class MailingHistoryCreate(BaseModel):
    mailingid: int
    senttime: datetime
    deliverystatusid: int
    model_config = ConfigDict(from_attributes=True)
