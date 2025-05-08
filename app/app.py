import mlflow
import pandas as pd
from fastapi import FastAPI, HTTPException, UploadFile, File
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
import io


# Загрузите данные и обучите модель (только при первом запуске)
def train_model():
    iris = load_iris()
    X, y = iris.data, iris.target
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    with mlflow.start_run() as run:
        # Логирование параметров
        params = {"n_estimators": 100, "random_state": 42}
        mlflow.log_params(params)

        # Обучение модели
        model = RandomForestClassifier(**params)
        model.fit(X_train, y_train)

        # Логирование метрик
        accuracy = model.score(X_test, y_test)
        mlflow.log_metric("accuracy", accuracy)

        # Логирование модели
        mlflow.sklearn.log_model(model, "random_forest_model")

        # Возвращаем run_id для дальнейшего использования
        return run.info.run_id


# Загрузка модели из MLflow (один раз при старте приложения)
mlflow.set_tracking_uri("http://localhost:5000")  # Укажите URL вашего MLflow сервера
try:
    run_id = train_model() # Обучаем модель, если она еще не обучена
    model_uri = f"runs:/{run_id}/random_forest_model"
    model = mlflow.sklearn.load_model(model_uri)

except Exception as e:
    raise Exception(f"Failed to load model: {e}")

app = FastAPI()


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Принимает CSV файл с данными для предсказания классов ирисов.
    """
    try:
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))

        # Валидация входных данных (кол-во колонок)
        if df.shape[1] != 4:
            raise HTTPException(status_code=400, detail="CSV file must have 4 columns")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid CSV file: {e}")

    try:
        predictions = model.predict(df.values)
        return {"predictions": predictions.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {e}")