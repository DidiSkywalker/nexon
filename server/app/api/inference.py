from fastapi import FastAPI
from app.controller import inference_controller
from app.util.errors import ErrorWithStatusCode

app = FastAPI()

@app.post("/infer/{model_name}")
async def infer(request: inference_controller.InferenceRequest, model_name):
    """
    Runs inference on the uploaded ONNX model with the given inputs.
    """
    try:
      return await inference_controller.infer(model_name, request)
    except ErrorWithStatusCode as e:
      raise e.as_http_exception()
    