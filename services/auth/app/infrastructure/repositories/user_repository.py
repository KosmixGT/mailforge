from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from services.auth.app.domain.interfaces.user_repository_impl import UserRepository
from services.auth.app.domain.models.user_model import User
from services.auth.app.infrastructure.database.models.user_db_model import UserModel


class PostgresUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: int) -> Optional[User]:
        result = await self.session.execute(
            select(UserModel).where(UserModel.userid == id)
        )
        db_user = result.scalar_one_or_none()
        return db_user.to_domain() if db_user else None

    async def get_by_username(self, username: str) -> Optional[User]:
        result = await self.session.execute(
            select(UserModel).where(UserModel.name == username)
        )
        db_user = result.scalar_one_or_none()
        return db_user.to_domain() if db_user else None

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        db_user = result.scalar_one_or_none()
        return db_user.to_domain() if db_user else None

    async def create(self, user: User) -> User:
        db_user = UserModel.from_domain(user)
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        return db_user.to_domain()
