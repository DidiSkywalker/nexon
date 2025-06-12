from bson import ObjectId
from datetime import datetime
from pydantic import BaseModel
from app.controller.database import models_collection
from app.util.constants import STATUS_DEPLOYED, STATUS_UPLOADED
from app.util.errors import BadRequestError, InternalServerError, NotFoundError

BASE_URL = "http://localhost:3000"

class DeployRequest(BaseModel):
    model_name: str
    model_id: str

    
async def deploy_model(request: DeployRequest):
  """
  Deploys an already uploaded model
  """
  model_id = ObjectId(request.model_id)
  try:
    models = await models_collection.find({"name": request.model_name}).to_list(None)   
    for model in models:
      if (model["status"] == STATUS_DEPLOYED):
        if model["_id"] == model_id:
          raise BadRequestError("This version is already deployed!")
        else:
          raise BadRequestError("Another version of this model is already deployed!")

    date = f"{datetime.now().day}/{datetime.now().month}/{datetime.now().year}"
    api_endpoint = f"{BASE_URL}/inference/infer/{request.model_name}"

    updated_result = await models_collection.update_one(
        {"_id": model_id},
        {"$set": {"status": STATUS_DEPLOYED, "deploy": date, "endpoint": api_endpoint}},
    )
    if updated_result.modified_count > 0:
      return {
      "message": f"Model {request.model_name} deployed successfuly!",
      "inference_endpoint": api_endpoint
      }
    else:
        raise NotFoundError("Model does not exist")
  except Exception as e:
        raise InternalServerError(f"Error deploying model: {str(e)}")
 
 
class UndeployRequest(BaseModel):
    model_name: str
    model_version: int     
      
async def undeploy_model(request: UndeployRequest):
    """
    Undeploys a model by updating its status in the database.
    """
    # Find the specific model by name and version
    model = await models_collection.find_one({"name": request.model_name, "version": request.model_version})

    if(model["status"] != STATUS_DEPLOYED) :
       raise BadRequestError("Model is not deployed")

    if not model:
        raise NotFoundError("Model not found.")

    # Update model status to 'Pending'
    update_result = await models_collection.update_one(
        {"_id": model["_id"]}, 
        {"$set": {"status": STATUS_UPLOADED}}
    )

    if update_result.modified_count == 0:
        raise InternalServerError("Failed to undeploy model.")

    return {"message": f"Model '{request.model_name}' (v{request.model_version}) undeployed successfully."}