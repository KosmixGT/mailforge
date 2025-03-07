from sqlalchemy import Column, Integer, String
from mailforge_shared.core.config.database import Base


class UserRoleModel(Base):
    __tablename__ = "userroles"

    roleid = Column(Integer, primary_key=True)
    rolename = Column(String(50), nullable=False, unique=True)
