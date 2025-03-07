from typing import Optional
from pydantic import BaseModel
from app.domain.models.recipient import Recipient


class RecipientDTO(BaseModel):
    id: int
    mailing_id: int
    address_id: int
    delivery_status_id: Optional[int] = None
    history_id: int

    @staticmethod
    def from_domain(recipient: Recipient) -> "RecipientDTO":
        return RecipientDTO(
            id=recipient.id,
            mailing_id=recipient.mailing_id,
            address_id=recipient.address_id,
            delivery_status_id=recipient.delivery_status_id,
            history_id=recipient.history_id,
        )


class RecipientCreateDTO(BaseModel):
    mailing_id: int
    address_id: int
    delivery_status_id: Optional[int] = None
    history_id: int
