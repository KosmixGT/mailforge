from sqlalchemy import Column, Integer, String
from app.infrastructure.database.base import Base


class MailingStatusModel(Base):
    __tablename__ = "mailingstatuses"

    statusid = Column(Integer, primary_key=True)
    statusname = Column(String(50), nullable=False, unique=True)
