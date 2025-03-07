from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.interfaces.mailing_repository import MailingRepository
from app.domain.models.mailing import Mailing
from app.infrastructure.database.models.mailing import MailingModel


class PostgresMailingRepository(MailingRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: int) -> Optional[Mailing]:
        result = await self.session.execute(
            select(MailingModel).where(MailingModel.mailingid == id)
        )
        db_mailing = result.scalar_one_or_none()
        return db_mailing.to_domain() if db_mailing else None

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Mailing]:
        result = await self.session.execute(
            select(MailingModel).offset(skip).limit(limit)
        )
        return [mailing.to_domain() for mailing in result.scalars().all()]

    async def get_by_user_id(self, user_id: int) -> List[Mailing]:
        result = await self.session.execute(
            select(MailingModel).where(MailingModel.userid == user_id)
        )
        return [mailing.to_domain() for mailing in result.scalars().all()]

    async def create(self, mailing: Mailing) -> Mailing:
        db_mailing = MailingModel.from_domain(mailing)
        self.session.add(db_mailing)
        await self.session.commit()
        await self.session.refresh(db_mailing)
        return db_mailing.to_domain()

    async def update(self, mailing: Mailing) -> Optional[Mailing]:
        db_mailing = await self.session.get(MailingModel, mailing.id)
        if db_mailing:
            updated = MailingModel.from_domain(mailing)
            for key, value in updated.__dict__.items():
                if key != "_sa_instance_state":
                    setattr(db_mailing, key, value)
            await self.session.commit()
            return db_mailing.to_domain()
        return None

    async def delete(self, id: int) -> bool:
        db_mailing = await self.session.get(MailingModel, id)
        if db_mailing:
            await self.session.delete(db_mailing)
            await self.session.commit()
            return True
        return False
