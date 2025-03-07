from typing import Generic, TypeVar, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar('T')

class BaseRepository(Generic[T]):
    """
    Базовый интерфейс репозитория, определяющий общие CRUD операции.
    Используется как шаблон для всех репозиториев в микросервисах.
    
    Общий тип T представляет тип доменной модели, с которой работает репозиторий.
    Пример: UserRepository(BaseRepository[User])
    """
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: int) -> Optional[T]:
        """Получить одну сущность по ID"""
        pass

    async def get_all(self) -> List[T]:
        """Получить все сущности"""
        pass

    async def create(self, entity: T) -> T:
        """Создать новую сущность"""
        pass

    async def update(self, entity: T) -> T:
        """Обновить существующую сущность"""
        pass

    async def delete(self, id: int) -> None:
        """Удалить сущность по ID"""
        pass
