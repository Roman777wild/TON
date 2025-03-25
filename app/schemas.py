from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TransactionBase(BaseModel):
    wallet_address: str  # Адрес кошелька
    token_symbol: str  # Символ токена (например, TON, USDT)
    amount: float  # Количество токенов
    transaction_hash: str  # Хеш транзакции
    timestamp: datetime  # Время транзакции


class TransactionCreate(TransactionBase):
    """Схема для создания новой транзакции"""
    pass


class TransactionResponse(TransactionBase):
    """Схема ответа при получении данных о транзакции"""
    id: int  # ID транзакции в базе данных

    class Config:
        from_attributes = True  # Позволяет Pydantic работать с SQLAlchemy-моделями


class TransactionSearchRequest(BaseModel):
    """Схема для поиска транзакций по кошельку и диапазону дат"""
    wallet_address: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
