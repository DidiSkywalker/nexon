from app.controller import deployment_controller
from app.controller.upload_controller import upload_file
from app.util.errors import ErrorWithStatusCode
from bson import ObjectId
from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.post("/deploy-file/")
async def deploy_file(file: UploadFile = File(...)):
    """
    Uploads an ONNX model file and initializes an inference session.
    """
    try:
      uploaded_model = await upload_file(file)
      model_id = ObjectId(uploaded_model["model_id"])
      model_name = uploaded_model["name"]
      return await deployment_controller.deploy_model(
          deployment_controller.DeployRequest(
              model_name=model_name, model_id=str(model_id)
          )
      )
    except ErrorWithStatusCode as e:  
      raise e.as_http_exception()


@app.post("/deploy-model/")
async def deploy_model(request: deployment_controller.DeployRequest):
    """
    Deploys an already uploaded model
    """
    try:
      return await deployment_controller.deploy_model(request)
    except ErrorWithStatusCode as e:  
      raise e.as_http_exception()
    

@app.put("/undeploy/{model_name}")
async def undeploy_model(request: deployment_controller.UndeployRequest):
    """
    Undeploys a model by updating its status in the database.
    """
    try:
      return await deployment_controller.undeploy_model(request)
    except ErrorWithStatusCode as e:  
      raise e.as_http_exception()
