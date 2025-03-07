from sqlalchemy import Column, Integer
from mailforge_shared.core.config.database import Base

class MailingModel(Base):
    """
    Локальная версия модели рассылки для сервиса истории.
    Содержит только поля, необходимые для связи с историей и фильтрации.
    """
    __tablename__ = "mailings"
    
    # Первичный ключ рассылки, используется для связи с историей
    mailingid = Column(Integer, primary_key=True)
    # ID пользователя, необходим для фильтрации истории по пользователю
    userid = Column(Integer)