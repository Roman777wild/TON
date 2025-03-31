from fastapi.testclient import TestClient
from app.main import app
from app.database.database import SessionLocal
from app.models.transaction import Transaction
from datetime import datetime

client = TestClient(app)

# Создаем тестовую БД
def setup_module():
    db = SessionLocal()
    db.add(Transaction(wallet_address="EQB3ncyBUTjZUA5EnFKR5_EnOMI9V1tTEAAPaiU71gc4TiUt", value=100, created_at=datetime.utcnow()))
    db.commit()
    db.close()

# Тест запроса всех транзакций
def test_get_transactions():
    response = client.get("/transactions")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

# Тест запроса транзакций по адресу кошелька
def test_get_transactions_by_wallet():
    response = client.get("/transactions?wallet_address=EQB3ncyBUTjZUA5EnFKR5_EnOMI9V1tTEAAPaiU71gc4TiUt")
    assert response.status_code == 200
    transactions = response.json()
    assert len(transactions) > 0
    assert transactions[0]["wallet_address"] == "EQB3ncyBUTjZUA5EnFKR5_EnOMI9V1tTEAAPaiU71gc4TiUt"
