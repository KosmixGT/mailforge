from sqlalchemy import Column, Integer, String
from mailforge_shared.core.config.database import Base


class MailingTypeModel(Base):
    __tablename__ = "mailingtypes"

    typeid = Column(Integer, primary_key=True)
    typename = Column(String(50), nullable=False, unique=True)
