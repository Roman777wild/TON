import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.transaction import Base, Transaction
from app.database.database import get_db

# Создаем тестовую БД в памяти (можно поменять на файл)
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Фикстура для создания и очистки базы перед каждым тестом
@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)  # Создаем таблицы
    session = TestingSessionLocal()
    yield session  # Передаем сессию в тест
    session.rollback()  # Откатываем изменения
    session.close()

def test_create_transaction(db_session):
    """Тест создания транзакции"""
    transaction = Transaction(
        transaction_id="tx123",
        wallet_address="wallet1",
        source="A",
        destination="B",
        value=100.0,
        fee=0.1
    )
    db_session.add(transaction)
    db_session.commit()

    retrieved = db_session.query(Transaction).filter_by(transaction_id="tx123").first()
    assert retrieved is not None
    assert retrieved.value == 100.0
    assert retrieved.wallet_address == "wallet1"

def test_delete_transaction(db_session):
    """Тест удаления транзакции"""
    transaction = Transaction(
        transaction_id="tx456",
        wallet_address="wallet2",
        source="C",
        destination="D",
        value=200.0,
        fee=0.2
    )
    db_session.add(transaction)
    db_session.commit()

    db_session.delete(transaction)
    db_session.commit()

    retrieved = db_session.query(Transaction).filter_by(transaction_id="tx456").first()
    assert retrieved is None
