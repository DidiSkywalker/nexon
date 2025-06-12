from fastapi import FastAPI, File, UploadFile, HTTPException
from app.controller import upload_controller

app = FastAPI()

@app.post("/")
async def upload_file(file: UploadFile = File(...)):
    """
    Uploads an ONNX model file
    """
    try:
      return await upload_controller.upload_file(file)
    except ValueError as ve:
      raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:  
      raise HTTPException(status_code=500, detail=str(e))