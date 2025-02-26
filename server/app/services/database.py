from motor.motor_asyncio import AsyncIOMotorClient
from gridfs import GridFS
from motor.motor_asyncio import AsyncIOMotorGridFSBucket

# Database connection
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "onnx_platform"

client = AsyncIOMotorClient(MONGO_URI)
database = client[DB_NAME]  
models_collection = database["models"]  
fs = AsyncIOMotorGridFSBucket(database)  
