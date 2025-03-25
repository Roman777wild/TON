import os
from dotenv import load_dotenv
from pydantic import BaseSettings

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

# Вывод для проверки
print(f"Используется БД: {settings.database_url}")
print(f"API-ключ TON: {settings.ton_api_key}")
print(f"Лимит запросов: {settings.rps_limit}")
print(f"Уровень логирования: {settings.log_level}")
print(f"Режим работы: {settings.env}")
