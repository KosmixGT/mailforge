from typing import Optional
from datetime import datetime
from pydantic import ConfigDict, BaseModel

class MailingBase(BaseModel):
    mailingid: int
    title: str
    messagetext: str
    scheduledtime: Optional[datetime] = None
    userid: int
    model_config = ConfigDict(from_attributes=True)

class MailingCreate(BaseModel):
    title: str
    messagetext: str
    scheduledtime: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)
