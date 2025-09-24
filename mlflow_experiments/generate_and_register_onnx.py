import mlflow
import mlflow.artifacts
import mlflow.onnx
import mlflow.tracking
import onnx
import onnxruntime as ort
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.datasets import make_regression
import pandas as pd
import os
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType

# --- MLflow Configuration ---
# MLFLOW_TRACKING_URI is set via environment variable in docker-compose.yml
# No need to set it programmatically here if running via Docker Compose
# mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")) # Fallback for local run outside docker

mlflow.set_experiment("ONNX Model Generation Experiment")

def create_and_log_onnx_model(model_name, version_description, input_shape=(10, 3), alias: str = None, tags: dict = {}):
    """
    Trains a simple scikit-learn model, converts it to ONNX,
    logs it to MLflow, and registers it in the Model Registry.
    """
    with mlflow.start_run() as run:
        run_id = run.info.run_id
        print(f"MLflow Run ID: {run_id}")

        # 1. Generate synthetic data
        X, y = make_regression(n_samples=input_shape[0], n_features=input_shape[1], random_state=42)
        
        # 2. Train a simple scikit-learn model
        model = LinearRegression()
        model.fit(X, y)

        print("Model trained.")

        # 3. Log parameters and metrics (optional)
        mlflow.log_param("n_samples", input_shape[0])
        mlflow.log_param("n_features", input_shape[1])

        # 4. Convert scikit-learn model to ONNX format
        initial_type = [('input', FloatTensorType([None, input_shape[1]]))]
        onnx_model = convert_sklearn(model, initial_types=initial_type)
        
        # Save the ONNX model to a temporary file (mlflow.onnx.log_model handles this internally,
        # but if you needed a local file, this is how you'd do it manually)
        # temp_onnx_path = "linear_regression_model.onnx"
        # with open(temp_onnx_path, "wb") as f:
        #     f.write(onnx_model.SerializeToString())
        # print(f"ONNX model created temporarily.")

        # 5. Log the ONNX model to MLflow
        model_info = mlflow.onnx.log_model(
            onnx_model=onnx_model,
            
            name="onnx_model",  # Path within the run's artifact directory
            registered_model_name=model_name, # Name to register the model under in the Model Registry
            signature=mlflow.models.infer_signature(X, y), # Infer input/output schema
            input_example=X[:2], # Provide an example input for documentation
            tags=tags,
        )
        print(f"ONNX model logged and registered as '{model_name}'.")
        print(f"Artifact path: {model_info.artifact_path}")

        # 6. Set a description for the registered model version
        client = mlflow.tracking.MlflowClient()
        # Get the latest version of the registered model
        # Note: This might be tricky if two runs register at the same time.
        # For local testing, it's usually fine. In production, consider explicit versioning or waits.
        try:
            latest_version = client.get_latest_versions(model_name, stages=["None"])[0].version
            if alias:
                client.set_registered_model_alias(model_name, alias, latest_version)
            if tags:
              for key, value in tags.items():
                client.set_model_version_tag(model_name, version=latest_version, key=key, value=value)
            client.update_model_version(
                name=model_name,
                version=latest_version,
                description=version_description
            )
            print(f"Registered model '{model_name}' version {latest_version} description updated.")
        except Exception as e:
            print(f"Could not update model version description for {model_name}: {e}")
            print("This might happen if it's the very first registration and no version is immediately available.")


        return run_id

if __name__ == "__main__":
    print("Starting ONNX model generation and registration script...")
    
    # Create and log first version of the model
    # run_id_v1 = create_and_log_onnx_model(
    #     "MyLinearRegressionONNX",
    #     "Initial version of a simple linear regression model converted to ONNX.",
    #     input_shape=(100, 5)
    # )
    # print(f"\nModel 'MyLinearRegressionONNX' version logged from run {run_id_v1}.")

    # # Create and log a second version of the model (simulating a new training run)
    # run_id_v2 = create_and_log_onnx_model(
    #     "MyLinearRegressionONNX",
    #     "Second version with different input features.",
    #     input_shape=(150, 7) # Change input shape to simulate a different model
    # )
    # print(f"\nModel 'MyLinearRegressionONNX' version logged from run {run_id_v2}.")
    
    
    run_id_a_1 = create_and_log_onnx_model(
        "model_a",
        "model_a v1.",
        input_shape=(100, 5),
    )
    print(f"\nModel 'model_a' version logged from run {run_id_a_1}.")
    
    
    run_id_a_2 = create_and_log_onnx_model(
        "model_a",
        "model_a v2.",
        input_shape=(150, 7),
        alias="experimental"
    )
    print(f"\nModel 'model_a' version logged from run {run_id_a_2}.")


    run_id_b_1 = create_and_log_onnx_model(
        "model_b",
        "model_b v1.",
        input_shape=(100, 5),
    )
    print(f"\nModel 'model_b' version logged from run {run_id_b_1}.")


    run_id_b_2 = create_and_log_onnx_model(
        "model_b",
        "model_b v2.",
        input_shape=(150, 7),
        tags={"project": "new_product"},
        alias="stable"
    )
    print(f"\nModel 'model_b' version logged from run {run_id_b_2}.")
    
    
    run_id_b_3 = create_and_log_onnx_model(
        "model_b",
        "model_b v3.",
        input_shape=(170, 9),
        tags={"project": "new_product"},
    )
    print(f"\nModel 'model_b' version logged from run {run_id_b_3}.")
    
    
    run_id_c_1 = create_and_log_onnx_model(
        "model_c",
        "model_c v1.",
        input_shape=(100, 5),
    )
    print(f"\nModel 'model_c' version logged from run {run_id_c_1}.")
    
    
    run_id_c_2 = create_and_log_onnx_model(
        "model_c",
        "model_c v2.",
        input_shape=(150, 7),
        tags={"stage": "production"},
    )
    print(f"\nModel 'model_c' version logged from run {run_id_c_2}.")


    run_id_d_1 = create_and_log_onnx_model(
        "model_d",
        "model_d v1.",
        input_shape=(100, 5),
    )
    print(f"\nModel 'model_d' version logged from run {run_id_d_1}.")


    run_id_d_2 = create_and_log_onnx_model(
        "model_d",
        "model_d v2.",
        input_shape=(150, 7),
        tags={"stage": "production"},
    )
    print(f"\nModel 'model_d' version logged from run {run_id_d_2}.")

    print("\nScript finished. Check the MLflow UI at http://localhost:5000 to see your runs and registered models.")