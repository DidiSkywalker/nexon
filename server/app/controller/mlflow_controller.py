import mlflow
import numpy as np
import os

class MLFlowController:
    def __init__(self, model_name: str, model_version_or_stage: str = "latest"):
        """
        Initializes the service to load a specific ONNX model from MLflow Model Registry.
        :param model_name: The name of the registered model (e.g., "MyLinearRegressionONNX").
        :param model_version_or_stage: The version number (e.g., "1", "2") or stage (e.g., "Production", "Staging")
                                       of the model to load. Use "latest" for the latest version.
        """
        self.model_name = model_name
        self.model_version_or_stage = model_version_or_stage
        self.model = None # To store the loaded ONNX model (pyfunc)
        self.ort_session = None # To store the ONNX Runtime session if using native ONNX
        
        self._set_mlflow_tracking_uri()
        self._load_model()

    def _set_mlflow_tracking_uri(self):
        """
        Sets the MLflow tracking URI from environment variable.
        """
        mlflow_tracking_uri = os.getenv("MLFLOW_TRACKING_URI")
        if not mlflow_tracking_uri:
            raise ValueError("MLFLOW_TRACKING_URI environment variable not set.")
        mlflow.set_tracking_uri(mlflow_tracking_uri)
        print(f"MLflow tracking URI set to: {mlflow_tracking_uri}")

    def _load_model(self):
        """
        Loads the ONNX model from the MLflow Model Registry.
        Loads as pyfunc for broader compatibility.
        """
        model_uri = f"models:/{self.model_name}/{self.model_version_or_stage}"
        print(f"Attempting to load model from URI: {model_uri}")
        
        try:
            # We'll load as pyfunc, as it's generally more robust for various model types
            self.model = mlflow.pyfunc.load_model(model_uri)
            print("Model loaded successfully as mlflow.pyfunc.")
            
            # If you specifically need the native ONNX model and ONNX Runtime:
            # onnx_model_path = mlflow.onnx.load_model(model_uri)
            # self.ort_session = ort.InferenceSession(onnx_model_path, providers=['CPUExecutionProvider'])
            # print("Model loaded successfully as native ONNX model for ONNX Runtime.")

        except Exception as e:
            print(f"Failed to load model {self.model_name} version/stage {self.model_version_or_stage}: {e}")
            raise

    def predict(self, input_data: np.ndarray):
        """
        Performs inference using the loaded ONNX model.
        :param input_data: Input data for prediction (numpy array).
                           Ensure it matches the model's expected input shape and type.
                           If your model expects a pandas DataFrame, convert it:
                           e.g., pd.DataFrame(input_data, columns=['feature1', 'feature2', ...])
        :return: Model predictions.
        """
        if self.model: # Using pyfunc model
            # For most scikit-learn models converted to ONNX, a 2D numpy array is expected.
            # If your model's signature expects a DataFrame, you'll need to convert `input_data` to pd.DataFrame
            if len(input_data.shape) == 1:
                input_data = input_data.reshape(1, -1) # Ensure 2D for single sample
            
            # If the model's signature requires specific column names, you'd need:
            # columns = [f'feature_{i}' for i in range(input_data.shape[1])] # Or actual feature names
            # input_df = pd.DataFrame(input_data, columns=columns)
            # predictions = self.model.predict(input_df)

            predictions = self.model.predict(input_data)
            return predictions
        # elif self.ort_session: # Using native ONNX Runtime session
        #     input_data = input_data.astype(np.float32) # Ensure correct dtype for ONNX
        #     input_name = self.ort_session.get_inputs()[0].name
        #     output_name = self.ort_session.get_outputs()[0].name
        #     predictions = self.ort_session.run([output_name], {input_name: input_data})[0]
        #     return predictions
        else:
            raise RuntimeError("Model not loaded. Please check initialization.")