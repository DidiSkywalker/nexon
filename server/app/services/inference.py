import onnxruntime as ort
import numpy as np
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Global variables to store session and model information
session = None
input_name = None
output_name = None


# Request body for inference
class InferenceRequest(BaseModel):
    input: list


@app.post("/upload-model/")
async def upload_model(file: UploadFile = File(...)):
    """
    Uploads an ONNX model file and initializes an inference session.
    """
    global session, input_name, output_name

    if not file.filename.endswith(".onnx"):
        raise HTTPException(status_code=400, detail="Only ONNX files are allowed.")

    try:
        # Save the uploaded model to disk
        model_path = f"app/models/{file.filename}"
        with open(model_path, "wb") as f:
            f.write(await file.read())

        # Initialize ONNX session
        session = ort.InferenceSession(model_path)

        # Get input and output details
        input_name = session.get_inputs()[0].name
        output_name = session.get_outputs()[0].name

        return {
            "message": f"Model {file.filename} uploaded and initialized successfully.",
            "input_name": input_name,
            "output_name": output_name,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error initializing model: {str(e)}")


@app.post("/infer/{model_name}")
async def infer(request: InferenceRequest, model_name):
    """
    Runs inference on the uploaded ONNX model with the given inputs.
    """
    global session, input_name, output_name

    model_path = f"app/deployedModels/{model_name}"

    if session is None:
         session = ort.InferenceSession(model_path)

    try:
        # Convert input data to NumPy array
        input_data = np.array(request.input).astype(np.float32)
        input_name = session.get_inputs()[0].name
        output_name = session.get_outputs()[0].name

        # Check input shape compatibility
        expected_shape = session.get_inputs()[0].shape
        if list(input_data.shape) != expected_shape:
            raise HTTPException(
                status_code=400,
                detail=f"Input shape mismatch. Expected: {expected_shape}, Received: {list(input_data.shape)}",
            )

        # Run inference
        results = session.run([output_name], {input_name: input_data})

        json_results = [result.tolist() for result in results]
        return {"results": json_results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")
