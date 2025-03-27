from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    transaction_id = Column(String, nullable=False, unique=True)
    wallet_address = Column(String, nullable=False)  # Адрес кошелька
    source = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    fee = Column(Float, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    body_hash = Column(String, nullable=True)
    message = Column(String, nullable=True)

    def __repr__(self):
        return f"<Transaction(id={self.id}, transaction_id={self.transaction_id}, source={self.source}, destination={self.destination}, value={self.value})>"