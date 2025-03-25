from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, '../../ton_swap_db.db')}"  # Путь к локальной SQLite БД

# Создаем подключение к базе данных
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})  # Используем аргумент только при многозадачности

# Создаем сессионный менеджер
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Определяем базовый класс для моделей
Base = declarative_base()

# Функция для получения сессии базы данных
def get_db():
    db = SessionLocal()  # Создаем сессию
    try:
        yield db  # Передаем сессию в контекст
    finally:
        db.close()  # Закрываем сессию после выполнения
