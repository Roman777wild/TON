from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    transaction_id = Column(String, nullable=False, unique=True)
    source = Column(String, nullable=False)   # откуда шла транзакция
    destination = Column(String, nullable=False)    # на какой адрес пришло
    value = Column(Float, nullable=False)
    fee = Column(Float, nullable=False)    # комиссия
    created_at = Column(Integer, nullable=False)  # Время создания транзакции в формате Unix timestamp
    body_hash = Column(String, nullable=True)
    message = Column(String, nullable=True)

    def __repr__(self):
        return f"<Transaction(id={self.id}, transaction_id={self.transaction_id}, source={self.source}, destination={self.destination}, value={self.value})>"