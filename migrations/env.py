import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, create_engine, pool
from alembic import context
from app.models.transaction import Base  # Импортируем модели

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Берем URL БД из переменной окружения или используем SQLite по умолчанию
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///ton_swap_db.db")

target_metadata = Base.metadata  # Передаем метаданные моделей


def run_migrations_offline() -> None:
    """Запуск миграций в 'offline' режиме."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Запуск миграций в 'online' режиме."""
    connectable = create_engine(DATABASE_URL, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
