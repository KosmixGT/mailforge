import os
from dotenv import load_dotenv
from pathlib import Path

# Проверяем наличие .env файла и загружаем его, если он существует (для локальной разработки)
env_path = Path(".env")
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

class Settings:
    PROJECT_NAME: str = "mailing app"
    PROJECT_VERSION: str = "1.0.0"
    
    # Загружаем переменные окружения из .env файла (если он существует) или из GitHub Actions (если переменные настроены там)
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRES_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRES_MINUTES")
    
    # DATABASE_URL берем из переменных окружения (локально из .env или из GitHub Actions)
    DATABASE_URL: str = os.getenv("DATABASE_URL")

settings = Settings()
