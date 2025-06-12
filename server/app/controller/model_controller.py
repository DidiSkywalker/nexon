from app.controller.database import models_collection, fs
from app.util.constants import STATUS_DEPLOYED, STATUS_UPLOADED
from app.util.errors import BadRequestError, InternalServerError, NotFoundError
from bson import ObjectId

async def get_models(*args):
  models = await models_collection.find(args).to_list()
  for model in models:
    model["_id"] = str(model["_id"])
    model["file_id"] = str(model["file_id"])
      
  return models
  
async def get_all_models():
  return get_models()
  
async def get_deployed_models():
  return get_models({"status": STATUS_DEPLOYED})

async def get_undeployed_models():
  return get_models({"status": STATUS_UPLOADED})

async def delete_model(model_name: str, model_version: int):
  """
  Deletes a model by name from the database and GridFS storage.
  """
  model = await models_collection.find_one({"name": model_name, "version": model_version})
  if not model:
      raise NotFoundError("Model not found.")

  # Ensure the file_id exists
  file_id = model.get("file_id")
  if not file_id:
      raise BadRequestError("Model does not have a valid file ID.")

  try:
      # Delete the file from GridFS
      await fs.delete(ObjectId(file_id))  # Ensure we pass an ObjectId

      # Delete model metadata
      delete_result = await models_collection.delete_one({"_id": model["_id"]})

      if delete_result.deleted_count == 1:
          return {"message": f"Model '{model_name}' deleted successfully"}
      else:
          raise InternalServerError("Failed to delete model.")

  except Exception as e:
      raise InternalServerError(f"Error deleting model: {str(e)}")