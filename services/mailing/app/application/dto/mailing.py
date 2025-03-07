from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.domain.models.mailing import Mailing


class MailingDTO(BaseModel):
    id: int
    title: str
    message_text: str
    scheduled_time: Optional[datetime]
    user_id: int
    status_id: int

    @staticmethod
    def from_domain(mailing: Mailing) -> "MailingDTO":
        if not mailing:
            return None
        return MailingDTO(
            id=mailing.id,
            title=mailing.title,
            message_text=mailing.message_text,
            scheduled_time=mailing.scheduled_time,
            user_id=mailing.user_id,
            status_id=mailing.status_id,
        )


class MailingCreateDTO(BaseModel):
    title: str
    message_text: str
    scheduled_time: Optional[datetime] = None


class MailingUpdateDTO(MailingCreateDTO):
    status_id: Optional[int] = None


class MailingResponseDTO(MailingDTO):
    status_name: str
    user_name: str
