from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class MailingHistoryBase(BaseModel):
    historyid: int
    mailingid: int
    senttime: datetime
    deliverystatusid: int

    class Config:
        orm_mode = True

class MailingHistoryCreate(BaseModel):
    mailingid: int
    senttime: datetime
    deliverystatusid: int

    class Config:
        orm_mode = True
