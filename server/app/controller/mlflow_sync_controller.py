from datetime import datetime
from typing import List, Tuple
from bson import ObjectId
from fastapi import BackgroundTasks, Response
import mlflow
import os
import tempfile
from os import environ
import mlflow.artifacts
from pydantic import BaseModel

from app.controller.database import DatabaseController, ModelMetadata
from app.util.constants import STATUS_DEPLOYED, STATUS_DOWNLOADING
from app.controller.model_controller import ModelController
from app.util.file_utils import convert_size

BASE_URL = "http://localhost:3000"

STATE_QUEUED = "queued"
STATE_ERROR = "error"

class SyncResultEntry(BaseModel):
    model_name: str
    version_selector: str
    status: str
    details: str = None
    versions: List[str] = []

def not_found_result(model_name: str, version_selector: str = None):
    return SyncResultEntry(model_name=model_name, version_selector=version_selector, status=STATE_ERROR, details="Model not found")

class MLFlowModelInfos():
    def __init__(self, model_name: str, model_version: str, model_uri: str, nexon_id: str = None):
        self.nexon_id = nexon_id
        self.model_name = model_name
        self.model_version = model_version
        self.model_uri = model_uri
        # todo: remove this
        self.model_id = model_uri.split("/")[-1]  # Extract model ID from URI

class SyncModelsRequest(BaseModel):
    models: List[Tuple[str, str]]  # List of tuples (model_name, version_specifier)
    
class SyncModelsResponse(BaseModel):
    has_errors: bool
    queued_models: int = 0
    skipped_models: int = 0
    results: List[SyncResultEntry] = []

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

    async def sync_models(self, request: SyncModelsRequest, api_response: Response, background_tasks: BackgroundTasks, db_controller: DatabaseController):
      response = SyncModelsResponse(has_errors=False, results=[])

      for model_name, model_version in request.models:
          print(f"Requested: {model_name} - {model_version}")
          result = None
          try:
            if (model_version == "latest"):
              # auto fetch latest
              result =  await self.fetch_version_uri_latest(model_name)
            elif (model_version.startswith("@")):
              # alias
              result = await self.fetch_version_uri_by_alias(model_name, model_version)
            elif (":" in model_version):
              # tag
              result = await self.fetch_version_uri_by_tag(model_name, model_version)
            else:
              # should be specific version
              result = await self.fetch_version_uri_by_version(model_name, model_version)
          except Exception as e:
            print(f"  no versions found")
          self._push_result(response, result or not_found_result(model_name, model_version))
     
      versions_to_deploy = await self._find_versions_to_deploy(db_controller, response)
      print(f"Versions to deploy: {versions_to_deploy}")
      
      for model_infos in versions_to_deploy:
        now = datetime.now()
        upload_date = f"{now.day}/{now.month}/{now.year}"
        model_metadata = ModelMetadata(
          name= model_infos.model_name,
          upload= upload_date,
          version= int(model_infos.model_version),
          status= STATUS_DOWNLOADING,
        )
        print(f"Model metadata: {model_metadata}")
        register_response = await ModelController(db_controller).register_model(model_metadata)
        print(f"Model registered: {register_response}")
        model_infos.nexon_id = register_response["model_id"]
        
      print(f"Starting background task to download and deploy models: {versions_to_deploy}")
      background_tasks.add_task(self.background_task_download_and_deploy_models, versions_to_deploy, db_controller=db_controller)
      
      if (response.has_errors and response.queued_models > 0):
        api_response.status_code = 207
      return response

    async def _find_versions_to_deploy(self, db_controller: DatabaseController, response: SyncModelsResponse) -> List[MLFlowModelInfos]:
      versions_to_deploy = []
      for result in response.results:
        if result.status == STATE_QUEUED:
          for uri in result.versions:
            split_uri = uri.split("/")
            model_name = split_uri[1]
            model_version = split_uri[2]
            deployed_model_id = await self._get_model_id_from_db(db_controller, model_name, model_version)
            if not deployed_model_id:
              versions_to_deploy.append(MLFlowModelInfos(model_name, model_version, uri))
            else:
              result.details = f"Model {model_name} version {model_version} already deployed."
      return versions_to_deploy
    
    async def _get_model_id_from_db(self, db_controller: DatabaseController, model_name: str, model_version: str):
      deployed_model = await db_controller.find_one({"name": model_name, "version": int(model_version)})
      return deployed_model["_id"] if deployed_model else None
    
    def _push_result(self, response: SyncModelsResponse, result: SyncResultEntry):
      response.results.append(result)
      if result.status == STATE_ERROR:
        response.has_errors = True
        response.skipped_models += 1
      else:
        response.queued_models += 1

    def _get_registered_model(self, model_name: str):
      try:
          return self.mlflow_client.get_registered_model(model_name)
      except Exception:
          return None

    async def fetch_version_uri_latest(self, model_name: str, version_selector: str = "latest"):
      registered_model = self._get_registered_model(model_name)
      if not registered_model:
          return not_found_result(model_name)

      latest_versions = registered_model.latest_versions
      if not latest_versions:
          return not_found_result(model_name)
      version = latest_versions[0].version
      uri = f"models:/{model_name}/{version}"
      print(f"model uri: {uri}")
      artifact_count = len(mlflow.artifacts.list_artifacts(uri))
      return SyncResultEntry(model_name=model_name, version_selector=version_selector, status=STATE_QUEUED, versions=[uri], details=f"Artifacts found: {artifact_count}")

    async def fetch_version_uri_by_version(self, model_name: str, version_selector: str):
      uri = f"models:/{model_name}/{version_selector}"
      print(f"model uri: {uri}")
      registered_model = self._get_registered_model(model_name)
      if not registered_model:
          return not_found_result(model_name, version_selector)

      artifact_count = len(mlflow.artifacts.list_artifacts(uri))
      return SyncResultEntry(model_name=model_name, version_selector=version_selector, status=STATE_QUEUED, versions=[uri], details=f"Artifacts found: {artifact_count}")

    async def fetch_version_uri_by_alias(self, model_name: str, version_selector: str):
      alias = version_selector[1:]  # Remove '@' prefix
      version = self.mlflow_client.get_model_version_by_alias(model_name, alias)
      print(f"version found: {version}")
      if not version:
          return not_found_result(model_name, version_selector)

      version_uri = f"models:/{model_name}/{version.version}"
      print(mlflow.__version__)
      print(f"model uri: {version_uri}")
      artifact_count = len(mlflow.artifacts.list_artifacts(version_uri))
      return SyncResultEntry(model_name=model_name, version_selector=version_selector, status=STATE_QUEUED, versions=[version_uri], details=f"Artifacts found: {artifact_count}")

    async def fetch_version_uri_by_tag(self, model_name: str, version_selector: str):
      tag = version_selector.split(":")
      tagged_versions = self.mlflow_client.search_model_versions(f"name='{model_name}' and tag.{tag[0]}='{tag[1]}'")
      print(f"tagged versions found: {len(tagged_versions)}")
      versions = []
      for v in tagged_versions:
          versions.append(f"models:/{model_name}/{v.version}")
      return SyncResultEntry(model_name=model_name, version_selector=version_selector, status=STATE_QUEUED, versions=versions, details=f"Versions found: {len(tagged_versions)}")

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

    async def background_task_download_and_deploy_models(self, model_infos_list: List[MLFlowModelInfos], db_controller: DatabaseController):
      for model_infos in model_infos_list:
        try:
          print(f"Downloading and deploying model: {model_infos.model_name}, {model_infos.model_version}, {model_infos.model_id}, {model_infos.nexon_id}")
          artifacts = mlflow.artifacts.list_artifacts(model_infos.model_uri)
          for artifact in artifacts:
            if artifact.path.endswith(".onnx"):
              print(f"Found ONNX artifact: {artifact.path}")
              with tempfile.TemporaryDirectory() as tmpdir:
                print(f"Temporary directory created: {tmpdir}")
                print(f"Downloading model artifact from URI: {model_infos.model_uri}")
                artifact_uri = f"{model_infos.model_uri}/{artifact.path}"
                download_result = mlflow.artifacts.download_artifacts(
                    artifact_uri=artifact_uri,
                    dst_path=tmpdir
                )
                local_file_path = os.path.join(tmpdir, artifact.path)
                print(f"Model downloaded to '{local_file_path}': {download_result}")
                # file_path = await self.download_model_artifact(model_infos.model_uri, artifact.path)
                await self.upload_and_update_model(model_infos, local_file_path, artifact.path, db_controller)
        except Exception as e:
          print(f"Error downloading and deploying model {model_infos.model_name} version {model_infos.model_version}: {e}")
          import traceback
          traceback.print_exc()
      
      
    async def download_model_artifact(self, artifact_uri: str, file_name: str) -> str:      
      with tempfile.TemporaryDirectory() as tmpdir:
        print(f"Temporary directory created: {tmpdir}")
        print(f"Downloading model artifact from URI: {artifact_uri}")
        download_result = mlflow.artifacts.download_artifacts(
            artifact_uri=artifact_uri,
            dst_path=tmpdir
        )
        local_file_path = os.path.join(tmpdir, file_name)
        print(f"Model downloaded to '{local_file_path}': {download_result}")
        return local_file_path
      
    async def upload_and_update_model(self, model_infos: MLFlowModelInfos, file_path: str, file_name: str, db_controller: DatabaseController) -> ObjectId:
      with open(file_path, "rb") as file_stream:
          print(f"File opened successfully: {file_stream}")
          # Upload the model file to the database
          print(f"Uploading model file to database...")
          file_id = await db_controller.upload_file(file_name, file_stream)
          now = datetime.now()
          deploy_date = f"{now.day}/{now.month}/{now.year}"
          file_size_bytes = os.fstat(file_stream.fileno()).st_size
          print(f"File size (bytes): {file_size_bytes}")
          file_size_readable = convert_size(file_size_bytes)
          api_endpoint = f"{BASE_URL}/inference/infer/{model_infos.model_name}"
          print(f"Nexon Model ID: {model_infos.nexon_id}, File ID: {file_id}, Deploy Date: {deploy_date}, API Endpoint: {api_endpoint}")
          updated_result = await db_controller.update_one(
            {"_id": ObjectId(model_infos.nexon_id)},
            {"$set": {"status": STATUS_DEPLOYED, "deploy": deploy_date, "file_id": str(file_id), "endpoint": api_endpoint, "size": file_size_readable}},
          )
          print(f"Model metadata updated in database: {updated_result}")
          
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