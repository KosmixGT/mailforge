import os
from dotenv import load_dotenv

from pathlib import Path
env_path = Path('.') / '.env'

load_dotenv(dotenv_path=env_path)

class Settings:
    PROJECT_NAME:str = "mailing app"
    PROJECT_VERSION: str = "1.0.0"
    SECRET_KEY : str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv('ALGORITHM')
    ACCESS_TOKEN_EXPIRES_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRES_MINUTES")
    DATABASE_URL: str = str(os.getenv('DATABASE_URL'))

settings = Settings()