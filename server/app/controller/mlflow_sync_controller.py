from datetime import datetime
from bson import ObjectId
from fastapi import BackgroundTasks
import mlflow
import os
import tempfile
from os import environ
import mlflow.artifacts
from pydantic import BaseModel

from app.controller.database import DatabaseController, ModelMetadata
from app.util.constants import STATUS_DEPLOYED, STATUS_DOWNLOADING
from app.controller.model_controller import ModelController

BASE_URL = "http://localhost:3000"

class MLFlowModelInfos():
    def __init__(self, model_name: str, model_version: str, model_uri: str):
        self.model_name = model_name
        self.model_version = model_version
        self.model_uri = model_uri
        self.model_id = model_uri.split("/")[-1]  # Extract model ID from URI

class SyncModelsRequest(BaseModel):
    models: dict    

class MLFlowSyncController:
    def __init__(self):
        self._set_mlflow_tracking_uri()
        self.mlflow_client = mlflow.tracking.MlflowClient()

    def _set_mlflow_tracking_uri(self):
        """
        Sets the MLflow tracking URI from environment variable.
        """
        mlflow_tracking_uri = os.getenv("MLFLOW_TRACKING_URI")
        if not mlflow_tracking_uri:
            raise ValueError("MLFLOW_TRACKING_URI environment variable not set.")
        mlflow.set_tracking_uri(mlflow_tracking_uri)
        print(f"MLflow tracking URI set to: {mlflow_tracking_uri}")

    async def sync_models(self, request: SyncModelsRequest):
      # iterate over models in dictionary
      for model_name, model_version in request.models.items():
          print(f"Requested: {model_name}:{model_version}")
          try:
            registered_model = self.mlflow_client.get_registered_model(model_name)
            print(f"  registered_model: {registered_model}")
            latest_versions = registered_model.latest_versions
            print(f"  latest versions: {[v.version for v in latest_versions]}")
          except Exception as e:
            print(f"  no versions found")
      # Fetch models from MLflow Model Registry
      # Check deployed models
      
      # Determine which models to download
      
      # Start async job to download models from MLflow Model Registry
      return "test"
    
    async def deploy_one_model(self, model_name, background_tasks: BackgroundTasks, db_controller: DatabaseController):
      try:
        registered_model = self.mlflow_client.get_registered_model(model_name)
        latest_versions = registered_model.latest_versions
        latest_version = latest_versions[0]
        
        
        print(f"Registered Model: {registered_model}")
        
        print(f"v1: {latest_versions[0].source} - {latest_versions[0].description} [{latest_versions[0].run_id}]")
        # print(f"v2: {latest_versions[1].source} - {latest_versions[1].description} [{latest_versions[1].run_id}]")

        print(f"{latest_version}")
        now = datetime.now()
        upload_date = f"{now.day}/{now.month}/{now.year}"
        model_metadata = ModelMetadata(
          name= model_name,
          upload= upload_date,
          version= latest_version.version,
          status= STATUS_DOWNLOADING,
        )
        print(f"Model metadata: {model_metadata}")
        register_response = await ModelController(db_controller).register_model(model_metadata)
        print(f"Model registered: {register_response}")
        nexon_model_id = register_response["model_id"]
        mlflow_model_infos = MLFlowModelInfos(model_name, latest_version.version, latest_version.source)
        print(f"Starting background task to deploy model: {model_name}, {latest_version.run_id}, {mlflow_model_infos}")
        background_tasks.add_task(self.background_task_deploy_model, nexon_model_id, mlflow_model_infos, latest_version.run_id, db_controller=db_controller)
        return f"Latest version for {model_name}: {latest_version.version}"
      except Exception as e:
        return f"No versions found: {e}"
        
    async def background_task_deploy_model(self, nexon_model_id: str, model_infos: MLFlowModelInfos, run_id: str, db_controller: DatabaseController):
      """
      Background task to deploy a model.
      This is a placeholder for the actual deployment logic.
      """
      try:
        model_id, model_name, model_version = model_infos.model_id, model_infos.model_name, model_infos.model_version
        print(f"Deploying model {model_name} in the background...")
        # aws_secret = environ['AWS_SECRET_ACCESS_KEY']
        # aws_key = environ['AWS_ACCESS_KEY_ID']
        # print(f"Using AWS credentials: {aws_key}, {aws_secret}")
        
        print(f"Fetching Run ID: {run_id}")
        run = self.mlflow_client.get_run(run_id)
        print(f"Run details: {run}")
        
        
        print(f"Listing artifacts for logged model... {model_id}")
        artifacts = self.mlflow_client.list_logged_model_artifacts(model_id)
        print(f"Artifacts for logged model:")
        for artifact in artifacts:
            print(f"- Path: {artifact.path}, Is Directory: {artifact.is_dir}, File Size: {artifact.file_size}") 
            
        # ==== TODO =======
        # Versuchen via artifact UI und mlflow.artifacts.download_artifacts
            
        
        # print(f"Listing artifacts...")
        # artifacts = self.mlflow_client.list_artifacts(run_id=run_id)
        # print(f"Artifacts for run {run_id}:")
        # for artifact in artifacts:
        #     print(f"- Path: {artifact.path}, Is Directory: {artifact.is_dir}, File Size: {artifact.file_size}") 
        
        # Here you would implement the actual deployment 
        with tempfile.TemporaryDirectory() as tmpdir:
          print(f"Temporary directory created: {tmpdir}")
          # artifacts = self.mlflow_client.list_artifacts(run_id=run_id)
          # print(f"Artifacts for run {run_id}:")
          # for artifact in artifacts:
          #     print(f"- Path: {artifact.path}, Is Directory: {artifact.is_dir}, File Size: {artifact.file_size}")
          
          print(f"Temp dir: {tmpdir}")
          
          artifact_uri = f"models:/{model_name}/{model_version}/model.onnx"
          print(f"Downloading model artifact from URI: {artifact_uri}")
          download_result = mlflow.artifacts.download_artifacts(
              artifact_uri=artifact_uri,
              dst_path=tmpdir
          )
          print(f"Model downloaded to temporary directory '{tmpdir}': {download_result}")
          local_file_path = tmpdir + "/model.onnx"
          print(f"Uploading file path: {local_file_path}")
          with open(local_file_path, "rb") as file_stream:
            print(f"File opened successfully: {file_stream}")
            # Upload the model file to the database
            print(f"Uploading model file to database...")
            file_id = await db_controller.upload_file("model.onnx", file_stream)
            now = datetime.now()
            deploy_date = f"{now.day}/{now.month}/{now.year}"
            api_endpoint = f"{BASE_URL}/inference/infer/{model_name}"
            print(f"Nexon Model ID: {nexon_model_id}, File ID: {file_id}, Deploy Date: {deploy_date}, API Endpoint: {api_endpoint}")
            updated_result = await db_controller.update_one(
              {"_id": ObjectId(nexon_model_id)},
              {"$set": {"status": STATUS_DEPLOYED, "deploy": deploy_date, "file_id": str(file_id), "endpoint": api_endpoint}},
            )
            print(f"Model metadata updated in database: {updated_result}")
        # For example, you might call a deployment service or update a database
        print(f"Model deployed successfully.")
      except Exception as e:
        print(f"Error during model deployment: {e}")
        import traceback
        traceback.print_exc() 