from fastapi import BackgroundTasks, Depends, FastAPI
import numpy as np

from app.controller.mlflow_controller import MLFlowController
from app.controller.mlflow_sync_controller import MLFlowSyncController, SyncModelsRequest
from app.controller.database import DatabaseController, get_db_controller

app = FastAPI()



@app.get("/test")
async def get_mlflow_test():
  mlflow_controller = MLFlowController("MyLinearRegressionONNX")
  dummy_input_v1 = np.array([[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0]], dtype=np.float64) 
  print(f"\nAttempting prediction with input (v1 expected): {dummy_input_v1}")
  predictions_v1 = mlflow_controller.predict(dummy_input_v1)
  print(f"Prediction (v1 expected): {predictions_v1}")
  return {"input": f"{dummy_input_v1}", "predictions": f"{predictions_v1}"}


@app.post("/sync")
async def post_mlflow_sync(models: SyncModelsRequest):
  print(f"Received models for sync: {models}")
  return await MLFlowSyncController().sync_models(models)

@app.post("/deployone")
async def post_mlflow_deploy_one(model_name: str, background_tasks: BackgroundTasks, db_controller: DatabaseController = Depends(get_db_controller)):
  return await MLFlowSyncController().deploy_one_model(model_name, background_tasks=background_tasks, db_controller=db_controller)