import onnxruntime as ort
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from datetime import datetime
from .database import fs, models_collection
from bson import ObjectId
import math

app = FastAPI()

# Global variables to store session and model information
session = None
model_name = None
input_name = None
output_name = None


class DeployRequest(BaseModel):
    model_name: str
    model_id: str


class InferenceRequest(BaseModel):
    inputs: list

def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("Bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])


@app.post("/deploy-file/")
async def deploy_file(file: UploadFile = File(...)):
    """
    Uploads an ONNX model file and initializes an inference session.
    """
    global session, model_name, input_name, output_name

    if not file.filename.endswith(".onnx"):
        raise HTTPException(status_code=400, detail="Only ONNX files are allowed.")

    try:
        file_id = await fs.upload_from_stream(file.filename, file.file)

        size = convert_size(file.size)
        date = f"{datetime.now().day}/{datetime.now().month}/{datetime.now().year}"

        model_metadata = {
        "file_id": str(file_id),
        "name": file.filename,
        "upload": date,
        "deploy": date,
        "size": size,
        "status": "Deployed",
        }

        result = await models_collection.insert_one(model_metadata)

        return {
          "message": f"Model {file.filename} uploaded successfuly!",
          "model_id": str(result.inserted_id),
          "file_id": str(file_id),
          "model_name": model_name,
          "inference_endpoint": f"http://127.0.0.1:8000/inference/infer/{file.filename}"
        }
        # # Save the uploaded model to disk
        # model_path = f"app/deployedModels/{file.filename}"
        # with open(model_path, "wb") as f:
        #     f.write(await file.read())

        # # Initialize ONNX session
        # session = ort.InferenceSession(model_path)
        # model_name = file.filename
        # input_name = session.get_inputs()[0].name
        # output_name = session.get_outputs()[0].name

        # return {
        #     "message": f"Model '{os.path.splitext(file.filename)[0]}' uploaded and deployed successfully.",
        #     "model_name": model_name,
        #     "inference_endpoint": f"http://127.0.0.1:8000/inference/infer/{model_name}"
        # }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deploying model: {str(e)}")


@app.post("/deploy-model/")
async def deploy_model(request: DeployRequest):
    """
    Deploys an already uploaded model by loading it into an ONNX session.
    """
    global session, model_name, input_name, output_name

    try:

        date = f"{datetime.now().day}/{datetime.now().month}/{datetime.now().year}"

        updated_result = models_collection.update_one(
            {"_id": ObjectId(request.model_id)},
            {"$set": {"status": "Deployed", "deploy": date}},
        )

        return {
          "message": f"Model {request.model_name} deployed successfuly!",
          "inference_endpoint": f"http://127.0.0.1:8000/inference/infer/{request.model_name}"
        }
    # try:
    #     # Initialize ONNX session
    #     session = ort.InferenceSession(model_path)
    #     model_name = request.model_name
    #     input_name = session.get_inputs()[0].name
    #     output_name = session.get_outputs()[0].name

    #     os.makedirs("app/deployedModels", exist_ok=True)

    #     # Move the model to deployedModels directory
    #     shutil.move(model_path, "app/deployedModels")

    #     return {
    #         "message": f"Model {model_name} deployed successfully.",
    #         "model_name": model_name,
    #         "inference_endpoint": f"http://127.0.0.1:8000/inference/infer/{model_name}"
    #     }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deploying model: {str(e)}")
