from sqlalchemy import Column, Integer, String
from app.infrastructure.database.base import Base


class UserRoleModel(Base):
    __tablename__ = "userroles"

    roleid = Column(Integer, primary_key=True)
    rolename = Column(String(50), nullable=False, unique=True)
