from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.services.inference import app as inference_app
from flask import Flask
import numpy

# Create the main FastAPI app
app = FastAPI()

# Mount the inference API to the main app (if modularized)
app.mount("/inference", inference_app)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add your frontend URL here
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Root endpoint (optional)
@app.get("/")
async def root():
    return {"message": "Welcome to the ONNX Inference API!"}

# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server.
    app.run()