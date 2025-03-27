# import requests
# from sqlalchemy.orm import Session
# from sqlalchemy.exc import IntegrityError
# from app.models.transaction import Transaction
# from app.database.database import get_db
# from app.config import settings
# from datetime import datetime
#
#
# class TonService:
#     def __init__(self):
#         self.api_url = settings.ton_api_key  # Исправлено на корректный импорт
#
#     def fetch_transaction_data(self, transaction_hash: str):
#         """
#         Получение данных о транзакции по её хэшу.
#         """
#         url = f"{self.api_url}/transaction/{transaction_hash}"
#         response = requests.get(url)
#
#         if response.status_code == 200:
#             return response.json()
#         return None
#
#     def process_transaction(self, transaction_data: dict, db: Session):
#         """
#         Обработка данных транзакции и сохранение их в базу данных,
#         если такой транзакции ещё нет.
#         """
#         transaction_id = transaction_data.get("transaction_id")
#         existing_transaction = db.query(Transaction).filter_by(transaction_id=transaction_id).first()
#
#         if existing_transaction:
#             return {"message": "Transaction already exists"}
#
#         new_transaction = Transaction(
#             transaction_id=transaction_id,
#             source=transaction_data.get("source"),
#             destination=transaction_data.get("destination"),
#             value=float(transaction_data.get("value", 0)),
#             fee=float(transaction_data.get("fee", 0)),
#             created_at=transaction_data.get("created_at"),
#             body_hash=transaction_data.get("body_hash"),
#             message=transaction_data.get("message")
#         )
#
#         try:
#             db.add(new_transaction)
#             db.commit()
#             return {"message": "Transaction saved successfully"}
#         except IntegrityError:
#             db.rollback()
#             return {"error": "Transaction already exists (race condition)"}
#
#     def track_transactions(self, transaction_hashes: list, db: Session):
#         """
#         Отслеживание и пакетное сохранение информации о транзакциях.
#         """
#         new_transactions = []
#         existing_ids = {tx.transaction_id for tx in db.query(Transaction.transaction_id).all()}
#
#         for tx_hash in transaction_hashes:
#             tx_data = self.fetch_transaction_data(tx_hash)
#             if tx_data and tx_data["transaction_id"] not in existing_ids:
#                 new_transactions.append(Transaction(
#                     transaction_id=tx_data.get("transaction_id"),
#                     source=tx_data.get("source"),
#                     destination=tx_data.get("destination"),
#                     value=float(tx_data.get("value", 0)),
#                     fee=float(tx_data.get("fee", 0)),
#                     created_at=datetime.fromisoformat(tx_data.get("created_at").replace("Z", "")),  # <-- FIX
#                     body_hash=tx_data.get("body_hash"),
#                     message=tx_data.get("message")
#                 ))
#
#         if new_transactions:
#             db.bulk_save_objects(new_transactions)
#             db.commit()
#
#         return {"message": f"Processed {len(new_transactions)} new transactions"}


import requests
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.transaction import Transaction
from app.database.database import get_db
from app.config import settings
from datetime import datetime


class TonService:
    def __init__(self):
        self.api_url = settings.ton_api_key  # Исправлено на корректный импорт
        print(f"Инициализирован TonService. API URL: {self.api_url}")

    def fetch_transaction_data(self, transaction_hash: str):
        """
        Получение данных о транзакции по её хэшу.
        """
        url = f"{self.api_url}/transaction/{transaction_hash}"
        print(f"Запрос к API: {url}")

        response = requests.get(url)
        print(f"Статус ответа: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"Данные получены: {data}")
            return data

        print("Ошибка получения данных или транзакция не найдена.")
        return None

    def process_transaction(self, transaction_data: dict, db: Session):
        """
        Обработка данных транзакции и сохранение их в базу данных,
        если такой транзакции ещё нет.
        """
        transaction_id = transaction_data.get("transaction_id")
        print(f"Обрабатываем транзакцию: {transaction_id}")

        existing_transaction = db.query(Transaction).filter_by(transaction_id=transaction_id).first()
        if existing_transaction:
            print(f"Транзакция {transaction_id} уже существует!")
            return {"message": "Transaction already exists"}

        new_transaction = Transaction(
            transaction_id=transaction_id,
            source=transaction_data.get("source"),
            destination=transaction_data.get("destination"),
            value=float(transaction_data.get("value", 0)),
            fee=float(transaction_data.get("fee", 0)),
            created_at=transaction_data.get("created_at"),
            body_hash=transaction_data.get("body_hash"),
            message=transaction_data.get("message")
        )

        try:
            db.add(new_transaction)
            db.commit()
            print(f"✅ Транзакция {transaction_id} успешно сохранена в базе!")
            return {"message": "Transaction saved successfully"}
        except IntegrityError:
            db.rollback()
            print(f"⚠️ Ошибка: транзакция {transaction_id} уже существует (race condition).")
            return {"error": "Transaction already exists (race condition)"}

    def track_transactions(self, transaction_hashes: list, db: Session):
        """
        Отслеживание и пакетное сохранение информации о транзакциях.
        """
        print("\n🔍 Начинаем отслеживание транзакций...")
        new_transactions = []

        # Получаем список уже существующих транзакций
        existing_ids = {tx.transaction_id for tx in db.query(Transaction.transaction_id).all()}
        print(f"Уже есть в базе: {existing_ids}")

        for tx_hash in transaction_hashes:
            print(f"\n🔹 Проверяем хеш транзакции: {tx_hash}")
            tx_data = self.fetch_transaction_data(tx_hash)

            if tx_data:
                if tx_data["transaction_id"] in existing_ids:
                    print(f"⚠️ Транзакция {tx_data['transaction_id']} уже есть в базе.")
                    continue

                print(f"✅ Добавляем новую транзакцию: {tx_data['transaction_id']}")
                new_transactions.append(Transaction(
                    transaction_id=tx_data.get("transaction_id"),
                    source=tx_data.get("source"),
                    destination=tx_data.get("destination"),
                    value=float(tx_data.get("value", 0)),
                    fee=float(tx_data.get("fee", 0)),
                    created_at=datetime.fromisoformat(tx_data.get("created_at").replace("Z", "")),  # <-- FIX
                    body_hash=tx_data.get("body_hash"),
                    message=tx_data.get("message")
                ))

        if new_transactions:
            print(f"\n💾 Сохраняем {len(new_transactions)} новых транзакций...")
            db.bulk_save_objects(new_transactions)
            db.commit()
            print("✅ Все новые транзакции сохранены!")
        else:
            print("📭 Новых транзакций не найдено.")

        return {"message": f"Processed {len(new_transactions)} new transactions"}
