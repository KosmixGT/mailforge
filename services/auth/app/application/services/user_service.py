from typing import Optional
from app.domain.models.user import User
from app.domain.interfaces.user_repository import UserRepository
from app.application.dto.user import UserDTO, UserCreateDTO
from mailforge_shared.core.utils.password_utils import Hash


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.repository = user_repository

    async def get_by_id(self, user_id: int) -> Optional[UserDTO]:
        user = await self.repository.get_by_id(user_id)
        return UserDTO.from_domain(user) if user else None

    async def get_by_username(self, username: str) -> Optional[UserDTO]:
        user = await self.repository.get_by_username(username)
        return UserDTO.from_domain(user) if user else None

    async def create_user(self, user_dto: UserCreateDTO) -> UserDTO:
        hashed_password = Hash.get_hashed_password(user_dto.password)
        user = User(
            id=None,
            name=user_dto.name,
            email=user_dto.email,
            password=hashed_password,
            role_id=user_dto.role_id,
        )
        created_user = await self.repository.create(user)
        return UserDTO.from_domain(created_user)

    async def authenticate_user(
        self, username: str, password: str
    ) -> Optional[UserDTO]:
        user = await self.repository.get_by_username(username)
        if not user:
            user = await self.repository.get_by_email(username)
            if not user:
                return None
        if not Hash.verify_hashed_password(password, user.password):
            return None
        return UserDTO.from_domain(user)
