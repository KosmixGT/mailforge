from pydantic import BaseModel, EmailStr
from app.domain.models.user_model import User
from typing import Optional


class UserDTO(BaseModel):
    id: Optional[int]
    name: str
    email: EmailStr
    role_id: int

    @staticmethod
    def from_domain(user: User) -> "UserDTO":
        return UserDTO(
            id=user.id, name=user.name, email=user.email, role_id=user.role_id
        )


class UserCreateDTO(BaseModel):
    name: str
    email: EmailStr
    password: str
    role_id: int
