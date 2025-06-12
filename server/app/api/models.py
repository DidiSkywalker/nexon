from fastapi import FastAPI
from app.controller import model_controller
from app.util.errors import ErrorWithStatusCode

app = FastAPI()


@app.get("/deployedModels")
async def getUploadedModels():
  return await model_controller.get_deployed_models()


@app.get("/uploadedModels")
async def getUploadedModels():
  return await model_controller.get_undeployed_models()
  
  
@app.get("/allModels")
async def getAllModels():
  return await model_controller.get_all_models()
  
  
@app.delete("/deleteModel/{model_name}/{model_version}")
async def delete_model(model_name: str, model_version: int):
  try:
    return await model_controller.delete_model(model_name, model_version)
  except ErrorWithStatusCode as e:
    raise e.as_http_exception()