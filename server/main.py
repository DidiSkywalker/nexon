from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.services.inference import app as inference_app
from app.services.deployment import app as deployment_app
from app.services.upload import app as upload_app
from app.services.database import fs, models_collection

# Create the main FastAPI app
app = FastAPI()

# Mount the inference API to the main app (if modularized)
app.mount("/inference", inference_app)
app.mount("/deployment", deployment_app)
app.mount("/upload", upload_app)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Root endpoint (optional)
@app.get("/")
async def root():
    return {"message": "Welcome to the ONNX Inference API!"}


@app.get("/deployedModels")
async def getUploadedModels():
    models = await models_collection.find({"status": "Deployed"}).to_list()
    for model in models:
        model["_id"] = str(model["_id"])
        model["file_id"] = str(model["file_id"])
        
    return models

@app.get("/uploadedModels")
async def getUploadedModels():
    models = await models_collection.find({"status": "Uploaded"}).to_list()
    for model in models:
        model["_id"] = str(model["_id"])
        model["file_id"] = str(model["file_id"])
        
    return models

@app.get("/allModels")
async def getAllModels():
    models = await models_collection.find().to_list()
    for model in models:
        model["_id"] = str(model["_id"])
        model["file_id"] = str(model["file_id"])
        
    return models
    


# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server.
    app.run()