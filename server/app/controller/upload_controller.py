from fastapi import UploadFile, File
from datetime import datetime
from app.controller.database import fs, models_collection
from app.util.file_utils import convert_size
from app.util.constants import STATUS_UPLOADED

async def upload_file(file: UploadFile = File(...)):
  """
  Uploads an ONNX model file
  """
  if not file.filename.endswith(".onnx"):
    raise ValueError("Only ONNX files are allowed.")
  
  try:
    latest_model = await models_collection.find_one(
        {"name": file.filename}, sort=[("version", -1)]
     )
    new_version = 1 if latest_model is None else latest_model["version"] + 1

    file_id = await fs.upload_from_stream(file.filename, file.file)
    size = convert_size(file.size)
    upload_date = f"{datetime.now().day}/{datetime.now().month}/{datetime.now().year}"

    model_metadata = {
        "file_id": str(file_id),
        "name": file.filename,
        "upload": upload_date,
        "version": new_version,
        "deploy": "",
        "size": size,
        "status": STATUS_UPLOADED,
    }

    result = await models_collection.insert_one(model_metadata)

    return {
        "message": f"Model {file.filename} uploaded successfully!",
        "model_id": str(result.inserted_id),
        **model_metadata
    }
    
  except Exception as e:
    raise Exception(f"Error uploading model: {str(e)}")