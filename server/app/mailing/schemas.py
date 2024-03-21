from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class MailingBase(BaseModel):
    mailingid: int
    title: str
    messagetext: str
    scheduledtime: Optional[datetime] = None
    userid: int

    class Config:
        orm_mode = True

class MailingCreate(BaseModel):
    title: str
    messagetext: str
    scheduledtime: Optional[datetime] = None

    class Config:
        orm_mode = True
