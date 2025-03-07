from datetime import datetime
from pydantic import BaseModel
from app.domain.models.history import MailingHistory


class MailingHistoryDTO(BaseModel):
    id: int
    mailing_id: int
    sent_time: datetime
    delivery_status_id: int

    @staticmethod
    def from_domain(history: MailingHistory) -> "MailingHistoryDTO":
        return MailingHistoryDTO(
            id=history.id,
            mailing_id=history.mailing_id,
            sent_time=history.sent_time,
            delivery_status_id=history.delivery_status_id,
        )


class MailingHistoryCreateDTO(BaseModel):
    mailing_id: int
    sent_time: datetime
    delivery_status_id: int
