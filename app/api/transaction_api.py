from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime
from typing import List, Optional

from app.services.ton_service import TonService
from app.models.transaction import Transaction
from app.database.database import SessionLocal, get_db

router = APIRouter()
ton_service = TonService()

# Dependency для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/transaction/{transaction_hash}")
async def get_transaction(transaction_hash: str):
    """
    Получение данных транзакции по её хэшу без сохранения в БД.
    """
    transaction_data = ton_service.fetch_transaction_data(transaction_hash)
    if not transaction_data:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction_data

@router.post("/transaction/{transaction_hash}")
async def save_transaction(transaction_hash: str, db: Session = Depends(get_db)):
    """
    Сохранение транзакции в базе данных.
    """
    transaction_data = ton_service.fetch_transaction_data(transaction_hash)
    if not transaction_data:
        raise HTTPException(status_code=404, detail="Transaction not found")

    ton_service.process_transaction(transaction_data, db)
    return {"message": "Transaction saved successfully"}

@router.get("/transactions")
async def get_transactions(
    db: Session = Depends(get_db),
    wallet_address: Optional[str] = Query(None, description="Адрес кошелька"),
    start_date: Optional[str] = Query(None, description="Начальная дата в формате YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="Конечная дата в формате YYYY-MM-DD")
):
    """
    Получение транзакций с возможностью фильтрации по адресу кошелька и диапазону дат.
    """
    query = db.query(Transaction)

    filters = []
    if wallet_address:
        filters.append(Transaction.wallet_address == wallet_address)

    if start_date:
        try:
            start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
            filters.append(Transaction.created_at >= start_datetime)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid start_date format. Use YYYY-MM-DD")

    if end_date:
        try:
            end_datetime = datetime.strptime(end_date, "%Y-%m-%d")
            filters.append(Transaction.created_at <= end_datetime)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid end_date format. Use YYYY-MM-DD")

    if filters:
        query = query.filter(and_(*filters))

    transactions = query.all()
    return transactions