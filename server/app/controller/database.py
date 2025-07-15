from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from motor.motor_asyncio import AsyncIOMotorGridFSBucket
from os import environ

# Database connection
MONGO_URI = f"mongodb://{environ['NEXON_MONGO_USER']}:{environ['NEXON_MONGO_PASS']}@{environ['NEXON_MONGO_HOST']}:{environ['NEXON_MONGO_PORT']}"
DB_NAME = environ['NEXON_MONGO_DB']

client = AsyncIOMotorClient(MONGO_URI)
database = client[DB_NAME]  
models_collection = database["models"]  
fs = AsyncIOMotorGridFSBucket(database)  

def get_db_controller():
    """
    Returns the database client.
    """
    return DatabaseController()
      

class ModelMetadata():
    def __init__(self, file_id: str, name: str, upload: str, version: int, deploy: str, size: str, status: str):
        self.file_id = file_id
        self.name = name
        self.upload = upload
        self.version = version
        self.deploy = deploy
        self.size = size
        self.status = status

    def to_dict(self):
        return {
            "file_id": self.file_id,
            "name": self.name,
            "upload": self.upload,
            "version": self.version,
            "deploy": self.deploy,
            "size": self.size,
            "status": self.status,
        }      
        
class DatabaseController():
    """
    Database controller for managing model metadata.
    """
    def __init__(self):
      self.db_client = AsyncIOMotorClient(MONGO_URI)
      self.database = self.db_client[DB_NAME]
      self.models_collection = self.db_client[DB_NAME]["models"]
      self.fs = AsyncIOMotorGridFSBucket(self.database)
        
    def debug(self):
      return "Live DB Controller"
    
    async def find(self, *args: any):
      return self.models_collection.find(*args).to_list(None)
    
    async def find_one(self, query, sort=None):
      return self.models_collection.find_one(query, sort=sort)
    
    async def delete_one(self, query):
      return self.models_collection.delete_one(query)
    
    async def upload_file(self, filename: str, file: any):
      return self.fs.upload_from_stream(filename, file)
    
    async def download_file(self, file_id: ObjectId):
      return self.fs.open_download_stream(file_id=file_id)
    
    async def delete_file(self, file_id: ObjectId):
      return self.fs.delete(file_id)
    
    async def insert_model(self, model_metadata: ModelMetadata):
      """
      Inserts a model metadata into the database.
      """
      model_dict = model_metadata.to_dict()
      result = await models_collection.insert_one(model_dict)
      return str(result.inserted_id)  # Return the inserted ID as a string
    
    async def update_one(self, query, update):
      """
      Updates a model metadata in the database.
      """
      return await self.models_collection.update_one(query, update)
      
