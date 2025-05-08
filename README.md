# Докеризированный MLflow/FastAPI сервис для классификации ирисов

Этот проект демонстрирует, как создать и развернуть MLflow/FastAPI сервис для классификации цветков ириса
с использованием scikit-learn и докеризации.  Также включена базовая интеграция с CI/CD.

## Описание

Проект состоит из следующих частей:

*   **`app/app.py`**: Содержит код для обучения, сохранения модели классификации ирисов (scikit-learn) и
                      FastAPI приложение для обработки запросов и предсказания классов ирисов.
*   **`app/Dockerfile`**: Файл для сборки Docker образа для FastAPI.
*   **`docker-compose.yml`**: Файл для управления контейнерами MLflow и FastAPI.
*   **`Dockerfile`**: Файл для сборки Docker образа для MLflow.
*   **`mlruns/`**: это директория, в которой MLflow хранит метаданные, артефакты и логи, связанные с 
                   запусками экспериментов машинного обучения.
*   **`mlartifacts/`**: служит для сохранения файлов (моделей, данных, графиков) вместе с результатами
                        экспериментов ML, обеспечивая их воспроизводимость и отслеживаемость.
*   **`.github/workflows/`**: Содержит пример workflow для GitHub Actions CI/CD.
*   **`README.md`**: Этот файл.
*   **`git.ignore`**: Файл с исключениями для Git.
*   **`iris_test.csv`**: Файл для тестирования модели через FastAPI.

## Предварительные требования

*   Docker и Docker Compose установлены.
*   Python 3.8+
*   Аккаунт на GitHub (для CI/CD с GitHub Actions).

## Инструкция по развертыванию

1.  **Клонируйте репозиторий:**

    ```bash
    git clone https://github.com/KormazovaVer/MLflow_Project
    cd MLflow_Project
    ```

2.  **Соберите и запустите Docker контейнеры:**

    ```bash
    docker-compose up --build
    ```
    Это создаст и запустит два контейнера:
    * FastAPI сервис на порту 8000
    * MLflow tracking server на порту 5000

3. **Доступ к сервисам**
   *  API FastAPI: `http://localhost:8000/docs` (для документации Swagger UI)
   *  MLflow UI: `http://localhost:5000`

## Обучение модели

Модель можно обучить, запустив скрипт в директории `app/`:

```bash
    python app/app.py 
```
Это обучит модель, сохранит ее в MLflow.

## Использование API

Отправьте POST запрос к API для классификации ириса:

```bash
    curl -X POST -F "file=@iris_test.csv" http://localhost:8000/predict
```

## CI/CD (GitHub Actions)

Проект включает пример workflow для GitHub Actions в .github/workflows/.
Он выполняет следующие шаги:

1. Собирает Docker образ.
2. Тестирует API (пример: pytest api/test_api.py).
3. Публикует Docker образ в Docker Hub.

Чтобы настроить CI/CD:

1. Создайте репозиторий на GitHub.
2. Загрузите код в репозиторий.
3. Включите GitHub Actions для вашего репозитория.
4. Настройте секреты GitHub Actions (имя пользователя и пароль Docker Hub) для публикации образа.
