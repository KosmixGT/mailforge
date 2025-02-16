from typing import List, Optional
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.interfaces.repositories.history import MailingHistoryRepository
from app.domain.models.history import MailingHistory
from app.infrastructure.database.models.history import MailingHistoryModel
from app.infrastructure.database.models.mailing import MailingModel


class PostgresMailingHistoryRepository(MailingHistoryRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: int) -> Optional[MailingHistory]:
        result = await self.session.execute(
            select(MailingHistoryModel).where(MailingHistoryModel.historyid == id)
        )
        db_history = result.scalar_one_or_none()
        return db_history.to_domain() if db_history else None

    async def get_by_mailing_id(self, mailing_id: int) -> List[MailingHistory]:
        result = await self.session.execute(
            select(MailingHistoryModel).where(
                MailingHistoryModel.mailingid == mailing_id
            )
        )
        return [history.to_domain() for history in result.scalars().all()]

    async def get_by_user_id(self, user_id: int) -> List[MailingHistory]:
        result = await self.session.execute(
            select(MailingHistoryModel)
            .join(MailingModel)
            .where(MailingModel.userid == user_id)
        )
        return [history.to_domain() for history in result.scalars().all()]

    async def create(self, history: MailingHistory) -> MailingHistory:
        db_history = MailingHistoryModel.from_domain(history)
        self.session.add(db_history)
        await self.session.commit()
        await self.session.refresh(db_history)
        return db_history.to_domain()

    async def get_by_mailing_and_time(
        self, mailing_id: int, sent_time: datetime
    ) -> Optional[MailingHistory]:
        result = await self.session.execute(
            select(MailingHistoryModel).where(
                MailingHistoryModel.mailingid == mailing_id,
                MailingHistoryModel.senttime == sent_time,
            )
        )
        db_history = result.scalar_one_or_none()
        return db_history.to_domain() if db_history else None
