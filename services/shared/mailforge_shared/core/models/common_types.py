from enum import Enum
from typing import TypeVar, Dict, Any

class DeliveryStatus(Enum):
    """Статусы доставки"""
    SUCCESSFUL = 1
    FAILED = 2

class MailingStatus(Enum):
    """Статусы рассылок"""
    PLANNED = 1
    SENT = 2
    COMPLETED = 3

class MailingType(Enum):
    """Типы рассылок"""
    EMAIL = 1
    TG = 2

JsonDict = Dict[str, Any]
ModelType = TypeVar("ModelType")
