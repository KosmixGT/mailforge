from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.interfaces.recipient_repository import RecipientRepository
from app.domain.models.recipient import Recipient
from app.infrastructure.database.models.recipient import RecipientModel


class PostgresRecipientRepository(RecipientRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: int) -> Optional[Recipient]:
        result = await self.session.execute(
            select(RecipientModel).where(RecipientModel.recipientid == id)
        )
        db_recipient = result.scalar_one_or_none()
        return db_recipient.to_domain() if db_recipient else None

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Recipient]:
        result = await self.session.execute(
            select(RecipientModel).offset(skip).limit(limit)
        )
        return [recipient.to_domain() for recipient in result.scalars().all()]

    async def create(self, recipient: Recipient) -> Recipient:
        db_recipient = RecipientModel.from_domain(recipient)
        self.session.add(db_recipient)
        await self.session.commit()
        await self.session.refresh(db_recipient)
        return db_recipient.to_domain()

    async def get_by_mailing_id(self, mailing_id: int) -> List[Recipient]:
        result = await self.session.execute(
            select(RecipientModel).where(RecipientModel.mailingid == mailing_id)
        )
        return [recipient.to_domain() for recipient in result.scalars().all()]

    async def get_by_history_id(self, history_id: int) -> List[Recipient]:
        result = await self.session.execute(
            select(RecipientModel).where(RecipientModel.historyid == history_id)
        )
        return [recipient.to_domain() for recipient in result.scalars().all()]
