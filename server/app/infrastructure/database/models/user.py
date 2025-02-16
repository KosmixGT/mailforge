from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.infrastructure.database.base import Base
from app.domain.models.user import User as DomainUser
from app.infrastructure.database.models.user_role import UserRoleModel


class UserModel(Base):
    __tablename__ = "users"

    userid = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    roleid = Column(ForeignKey("userroles.roleid"), nullable=False)

    userrole = relationship("UserRoleModel")

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
