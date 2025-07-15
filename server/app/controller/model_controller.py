from app.controller.database import DatabaseController
from app.util.constants import STATUS_DEPLOYED, STATUS_UPLOADED
from app.util.errors import BadRequestError, NotFoundError
from bson import ObjectId

class ModelController:
    """
    Controller for managing model uploads and metadata.
    """
    def __init__(self, db_controller: DatabaseController):
      self.db_controller = db_controller

    async def get_models(self, *args):
      models = await self.db_controller.find(*args)
      for model in models:
        model["_id"] = str(model["_id"])
        model["file_id"] = str(model["file_id"])
          
      return models
      
    async def get_all_models(self):
      return await self.get_models()
      
    async def get_deployed_models(self):
      return await self.get_models({"status": STATUS_DEPLOYED})

    async def get_undeployed_models(self):
      return await self.get_models({"status": STATUS_UPLOADED})

    async def delete_model(self, model_name: str, model_version: int):
      """
      Deletes a model by name from the database and GridFS storage.
      """
      model = await self.db_controller.find_one({"name": model_name, "version": model_version})
      if not model:
          raise NotFoundError("Model not found.")

      # Ensure the file_id exists
      file_id = model.get("file_id")
      if not file_id:
          raise BadRequestError("Model does not have a valid file ID.")

      try:
          # Delete the file from GridFS
          await self.db_controller.delete_file(ObjectId(file_id))  # Ensure we pass an ObjectId

          # Delete model metadata
          delete_result = await self.db_controller.delete_one({"_id": model["_id"]})

          if delete_result.deleted_count == 1:
              return {"message": f"Model '{model_name}' deleted successfully"}
          else:
              raise Exception("Failed to delete model.")

      except Exception as e:
          raise Exception(f"Error deleting model: {str(e)}")