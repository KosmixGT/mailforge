from typing import Any
from email.utils import parseaddr

class Validator:
    """
    Общие валидаторы для всех сервисов
    """
    @staticmethod
    def validate_email(email: str) -> bool:
        """Проверка корректности email"""
        return '@' in parseaddr(email)[1]

    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Проверка формата телефона"""
        return phone.isdigit() and len(phone) >= 10
