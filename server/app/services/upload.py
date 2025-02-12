import onnxruntime as ort
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
import os
import shutil

app = FastAPI()




@app.post("/")
async def upload_file(file: UploadFile = File(...)):
    """
    Uploads an ONNX model file
    """

    if not file.filename.endswith(".onnx"):
        raise HTTPException(status_code=400, detail="Only ONNX files are allowed.")

    try:
        # Save the uploaded model to disk
        model_path = f"app/models/{file.filename}"
        with open(model_path, "wb") as f:
            f.write(await file.read())

        return {
            "message": f"Model '{os.path.splitext(file.filename)[0]}' uploaded successfully.",
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading model: {str(e)}")
