from sqlalchemy import Column, Integer, String
from app.infrastructure.database.base import Base


class MailingTypeModel(Base):
    __tablename__ = "mailingtypes"

    typeid = Column(Integer, primary_key=True)
    typename = Column(String(50), nullable=False, unique=True)
