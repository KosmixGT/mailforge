from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from mailforge_shared.core.config.database import Base
from app.domain.models.user_model import User as DomainUser
from app.infrastructure.database.models.user_role import UserRoleModel


class UserModel(Base):
    __tablename__ = "users"

    userid: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    roleid: Mapped[int] = mapped_column(ForeignKey("userroles.roleid"), nullable=False)

    userrole = relationship(UserRoleModel)

    def to_domain(self) -> DomainUser:
        return DomainUser(
            id=self.userid,
            name=self.name,
            email=self.email,
            password=self.password,
            role_id=self.roleid,
        )

    @staticmethod
    def from_domain(user: DomainUser) -> "UserModel":
        return UserModel(
            userid=user.id,
            name=user.name,
            email=user.email,
            password=user.password,
            roleid=user.role_id,
        )
