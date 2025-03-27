from fastapi import FastAPI
from app.api.transaction_api import router as transaction_router
from app.config import settings
from app.database.database import engine, Base
from sqlalchemy.orm import sessionmaker
import logging

# Настройка логирования
logging.basicConfig(level=settings.log_level.upper())

# Создание приложения FastAPI
app = FastAPI()

# Инициализация базы данных
Base.metadata.create_all(bind=engine)

# Подключение маршрутов
app.include_router(transaction_router)

# Главная страница (опционально)
@app.get("/")
async def read_root():
    return {"message": "Welcome to TON Swap Tracker API!"}
