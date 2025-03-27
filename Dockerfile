# Базовый образ Python
FROM python:3.11.2-slim

# Устанавливаем необходимые зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY . /app

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Указываем переменную окружения для SQLite
ENV DATABASE_URL=sqlite:///ton_swap_db.db

# Открываем порт
EXPOSE 8000

# Команда для запуска приложения
CMD ["python", "main.py"]

