import os
from random import random, randint

import mlflow
import mlflow.sklearn
import mlflow.onnx

from sklearn.datasets import make_regression, load_iris
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType


MLFLOW_URI="http://mlflow:5000"
mlflow.set_tracking_uri(MLFLOW_URI)
print(f"MLflow is using tracking server at ${mlflow.get_tracking_uri()}")

def experiment_onnx_model():
  mlflow.set_experiment("ONNX_Model_Experiment")

  with mlflow.start_run():
      # Load and split data
      iris = load_iris()
      X_train, X_test, y_train, y_test = train_test_split(
          iris.data, iris.target, test_size=0.2, random_state=42)

      # Train a model
      clf = RandomForestClassifier(n_estimators=10)
      clf.fit(X_train, y_train)

      # Convert to ONNX
      initial_type = [("input", FloatTensorType([None, X_train.shape[1]]))]
      onnx_model = convert_sklearn(clf, initial_types=initial_type)

      # Save ONNX model to disk
      onnx_model_path = "model.onnx"
      with open(onnx_model_path, "wb") as f:
          f.write(onnx_model.SerializeToString())

      # Log ONNX model to MLflow
      mlflow.onnx.log_model(
          onnx_model=onnx_model,
          artifact_path="onnx_model",
          registered_model_name="IrisClassifierONNX"  # Register model!
      )

      # Log parameters/metrics if needed
      mlflow.log_param("n_estimators", clf.n_estimators)

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
    print("Run experiment to log ONNX model...")
    experiment_onnx_model()