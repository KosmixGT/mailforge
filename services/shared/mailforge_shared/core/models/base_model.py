from datetime import datetime
from typing import Optional

class BaseModel:
    """
    Базовая модель, предоставляющая общие атрибуты для всех доменных моделей.
    Используется как родительский класс для всех моделей в микросервисах.
    
    Атрибуты:
        id: Уникальный идентификатор
        created_at: Временная метка создания
        updated_at: Временная метка последнего обновления
    """
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
