FROM sregistry.mts.ru/fintech/base-images/python:3.14-slim

# Рабочая директория
WORKDIR /app

COPY pip.conf /etc/pip.conf

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . .

EXPOSE 8080

# Команда запуска
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]