from sqlalchemy import Column, Integer, String
from app.infrastructure.database.base import Base


class DeliveryStatusModel(Base):
    __tablename__ = "deliverystatuses"

    deliverystatusid = Column(Integer, primary_key=True)
    statusname = Column(String(50), nullable=False, unique=True)
