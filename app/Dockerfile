# Dockerfile для FastAPI
FROM python:3.9-slim-buster

WORKDIR /app

# Скопируйте зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Скопируйте исходный код
COPY app.py .

# Укажите порт
EXPOSE 8000

# Запустите FastAPI с помощью uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]