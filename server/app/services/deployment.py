import onnxruntime as ort
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
import os
import shutil

app = FastAPI()

# Global variables to store session and model information
session = None
model_name = None
input_name = None
output_name = None


class DeployRequest(BaseModel):
    model_name: str


class InferenceRequest(BaseModel):
    inputs: list


@app.post("/deploy-file/")
async def deploy_file(file: UploadFile = File(...)):
    """
    Uploads an ONNX model file and initializes an inference session.
    """
    global session, model_name, input_name, output_name

    if not file.filename.endswith(".onnx"):
        raise HTTPException(status_code=400, detail="Only ONNX files are allowed.")

    try:
        # Save the uploaded model to disk
        model_path = f"app/deployedModels/{file.filename}"
        with open(model_path, "wb") as f:
            f.write(await file.read())

        # Initialize ONNX session
        session = ort.InferenceSession(model_path)
        model_name = file.filename
        input_name = session.get_inputs()[0].name
        output_name = session.get_outputs()[0].name

        return {
            "message": f"Model '{os.path.splitext(file.filename)[0]}' uploaded and deployed successfully.",
            "model_name": model_name,
            "inference_endpoint": f"http://127.0.0.1:8000/inference/infer/{model_name}"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deploying model: {str(e)}")


@app.post("/deploy-model/")
async def deploy_model(request: DeployRequest):
    """
    Deploys an already uploaded model by loading it into an ONNX session.
    """
    global session, model_name, input_name, output_name

    model_path = f"app/models/{request.model_name}"

    if not os.path.exists(model_path):
        raise HTTPException(status_code=404, detail="Model not found.")

    try:
        # Initialize ONNX session
        session = ort.InferenceSession(model_path)
        model_name = request.model_name
        input_name = session.get_inputs()[0].name
        output_name = session.get_outputs()[0].name

        os.makedirs("app/deployedModels", exist_ok=True)

        # Move the model to deployedModels directory
        shutil.move(model_path, "app/deployedModels")

        return {
            "message": f"Model {model_name} deployed successfully.",
            "model_name": model_name,
            "inference_endpoint": f"http://127.0.0.1:8000/inference/infer/{model_name}"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deploying model: {str(e)}")
