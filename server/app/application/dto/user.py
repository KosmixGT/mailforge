from pydantic import BaseModel, EmailStr
from typing import Optional
from app.domain.models.user import User


class UserDTO(BaseModel):
    id: int
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
