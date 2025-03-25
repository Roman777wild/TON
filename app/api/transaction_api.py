from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
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
async def get_transaction(transaction_hash: str, db: Session = Depends(get_db)):
    """
    Получение данных транзакции по её хэшу
    """
    transaction_data = ton_service.fetch_transaction_data(transaction_hash)
    if not transaction_data:
        raise HTTPException(status_code=404, detail="Transaction not found")

    # Сохранение в базе данных
    ton_service.process_transaction(transaction_data, db)

    return transaction_data

@router.get("/transactions")
async def get_transactions(db: Session = Depends(get_db)):
    """
    Получение всех транзакций из базы данных
    """
    transactions = db.query(Transaction).all()
    return transactions
