from typing import List, Optional
from app.domain.models.recipient import Recipient
from app.domain.interfaces.repositories.recipient import RecipientRepository
from app.application.dto.recipient import RecipientDTO, RecipientCreateDTO


class RecipientService:
    def __init__(self, recipient_repository: RecipientRepository):
        self.repository = recipient_repository

    async def get_recipient(self, recipient_id: int) -> Optional[RecipientDTO]:
        recipient = await self.repository.get_by_id(recipient_id)
        return RecipientDTO.from_domain(recipient) if recipient else None

    async def get_recipients(
        self, skip: int = 0, limit: int = 100
    ) -> List[RecipientDTO]:
        recipients = await self.repository.get_all(skip, limit)
        return [RecipientDTO.from_domain(recipient) for recipient in recipients]

    async def create_recipient(self, recipient_dto: RecipientCreateDTO) -> RecipientDTO:
        recipient = Recipient(
            id=None,
            mailing_id=recipient_dto.mailing_id,
            address_id=recipient_dto.address_id,
            delivery_status_id=recipient_dto.delivery_status_id,
            history_id=recipient_dto.history_id,
        )
        created_recipient = await self.repository.create(recipient)
        return RecipientDTO.from_domain(created_recipient)

    async def get_recipients_by_mailing(self, mailing_id: int) -> List[RecipientDTO]:
        recipients = await self.repository.get_by_mailing_id(mailing_id)
        return [RecipientDTO.from_domain(recipient) for recipient in recipients]

    async def get_recipients_by_history(self, history_id: int) -> List[RecipientDTO]:
        recipients = await self.repository.get_by_history_id(history_id)
        return [RecipientDTO.from_domain(recipient) for recipient in recipients]
