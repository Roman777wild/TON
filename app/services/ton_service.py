import requests
import json
from app.models.transaction import Transaction
from app.database.database import Session
from app.config import TON_API_URL


class TonService:
    def __init__(self):
        self.session = Session()

    def fetch_transaction_data(self, transaction_hash: str):
        """
        Получение данных о транзакции по её хэшу.
        """
        url = f"{TON_API_URL}/transaction/{transaction_hash}"
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            return None

    def process_transaction(self, transaction_data: dict):
        """
        Обработка данных транзакции и сохранение их в базу данных.
        """
        transaction = Transaction(
            transaction_id=transaction_data.get('transaction_id'),
            source=transaction_data.get('source'),
            destination=transaction_data.get('destination'),
            value=float(transaction_data.get('value', 0)),
            fee=float(transaction_data.get('fee', 0)),
            created_at=transaction_data.get('created_at'),
            body_hash=transaction_data.get('body_hash'),
            message=transaction_data.get('message')
        )

        self.session.add(transaction)
        self.session.commit()

    def track_transactions(self, transaction_hashes: list):
        """
        Отслеживание и сохранение информации о транзакциях.
        """
        for tx_hash in transaction_hashes:
            tx_data = self.fetch_transaction_data(tx_hash)
            if tx_data:
                self.process_transaction(tx_data)