import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Загружаем переменные окружения из .env
load_dotenv()

class Settings(BaseSettings):
    # Настройки базы данных
    database_url: str
    # API-ключи для взаимодействия с TON
    ton_api_key: str
    ton_rpc_url: str
    # Лимит запросов (по умолчанию 10)
    rps_limit: int = 10
    # Уровень логирования
    log_level: str = "info"
    # Режим работы приложения (разработка или продакшен)
    env: str = "development"

    class Config:
        env_file = ".env"  # Указываем, что переменные загружаются из .env

settings = Settings()