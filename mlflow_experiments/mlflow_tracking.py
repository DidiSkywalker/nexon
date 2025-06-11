import os
from random import random, randint

import mlflow
import mlflow.sklearn

from sklearn.datasets import make_regression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split


MLFLOW_URI="http://mlflow:5000"
mlflow.set_tracking_uri(MLFLOW_URI)
print(f"MLflow is using tracking server at ${mlflow.get_tracking_uri()}")

def experiment_model():
    with mlflow.start_run() as run:
        print("  running model experiment")
        X, y = make_regression(n_features=4, n_informative=2, random_state=0, shuffle=False)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        params = {"max_depth": 2, "random_state": 42}
        model = RandomForestRegressor(**params)
        model.fit(X_train, y_train)

        # Log parameters and metrics using the MLflow APIs
        mlflow.log_params(params)

        y_pred = model.predict(X_test)
        mlflow.log_metrics({"mse": mean_squared_error(y_test, y_pred)})

        # Log the sklearn model and register as version 1
        mlflow.sklearn.log_model(
            sk_model=model,
            name="sklearn-model",
            input_example=X_train,
            registered_model_name="sk-learn-random-forest-reg-model",
        )

def experiment_artifact():
    with mlflow.start_run() as run:
        print("  running artifact experiment")

        mlflow.log_param("param1", randint(0, 100))
        
        mlflow.log_metric("foo", random())
        mlflow.log_metric("foo", random() + 1)
        mlflow.log_metric("foo", random() + 2)

        if not os.path.exists("outputs"):
            os.makedirs("outputs")
        with open("outputs/test.txt", "w") as f:
            f.write("hello world!")

        mlflow.log_artifacts("outputs")

if __name__ == "__main__":
    print("Run experiment to log artifact...")
    experiment_artifact()
    print("Run experiment to log model...")
    experiment_model()