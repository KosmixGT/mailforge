from typing import Any, Callable
from abc import ABC, abstractmethod

class MessageQueue(ABC):
    """
    Интерфейс для асинхронного обмена сообщениями между сервисами.
    Используется для событий и коммуникации между микросервисами.
    """
    @abstractmethod
    async def publish(self, topic: str, message: Any) -> None:
        """Публикация сообщения в очередь"""
        pass

    @abstractmethod
    async def subscribe(self, topic: str, callback: Callable) -> None:
        """Подписка на сообщения из очереди"""
        pass
