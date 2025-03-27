FROM python:3.11.2-slim  # Базовый образ Python 3.11

# Устанавливаем необходимые инструменты для сборки
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*  # Устанавливаем зависимости для компиляции

WORKDIR /app  # Устанавливаем рабочую директорию

COPY . /app  # Копируем файлы проекта в контейнер

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]  # Команда для запуска вашего приложения
