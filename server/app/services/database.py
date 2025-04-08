from motor.motor_asyncio import AsyncIOMotorClient
from gridfs import GridFS
from motor.motor_asyncio import AsyncIOMotorGridFSBucket
from os import environ

# Database connection
MONGO_URI = f"mongodb://{environ['NEXON_MONGO_USER']}:{environ['NEXON_MONGO_PASS']}@{environ['NEXON_MONGO_HOST']}:{environ['NEXON_MONGO_PORT']}"
DB_NAME = environ['NEXON_MONGO_DB']

client = AsyncIOMotorClient(MONGO_URI)
database = client[DB_NAME]  
models_collection = database["models"]  
fs = AsyncIOMotorGridFSBucket(database)  
