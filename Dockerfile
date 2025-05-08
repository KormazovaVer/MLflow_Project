# Dockerfile для MLflow
FROM python:3.9-slim-buster

WORKDIR /app

# Установите MLflow и другие зависимости
RUN pip install mlflow==2.9.2

# Установите gunicorn для обслуживания MLflow UI
RUN pip install gunicorn

# Скопируйте конфигурационный файл, если требуется
#COPY mlflow.yml /app/mlflow.yml

# Укажите порт, на котором будет работать MLflow
EXPOSE 5000

# Запустите MLflow UI с помощью gunicorn
CMD ["gunicorn", "--workers", "1", "--worker-class", "gthread", "--threads", "4", "-b", "0.0.0.0:5000", "mlflow.ui.wsgi_app:app"]