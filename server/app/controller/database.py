from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from motor.motor_asyncio import AsyncIOMotorGridFSBucket
from os import environ

# Database connection
MONGO_URI = f"mongodb://{environ['NEXON_MONGO_USER']}:{environ['NEXON_MONGO_PASS']}@{environ['NEXON_MONGO_HOST']}:{environ['NEXON_MONGO_PORT']}"
DB_NAME = environ['NEXON_MONGO_DB']
      

class ModelMetadata():
    def __init__(self, file_id: str = None, name: str = None, upload: str = None, version: int = None, deploy: str = None, size: str = None, status: str = None):
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
    def __init__(self, client: AsyncIOMotorClient, database, fs_bucket: AsyncIOMotorGridFSBucket):
      self.db_client = client
      self.database = database
      self.models_collection = self.database["models"]
      self.fs = fs_bucket

    def debug(self):
      return "Live DB Controller"
    
    async def find(self, *args: any):
      return await self.models_collection.find(*args).to_list(None)
    
    async def find_one(self, query, sort=None):
      return await self.models_collection.find_one(query, sort=sort)
    
    async def delete_one(self, query):
      return await self.models_collection.delete_one(query)
    
    async def upload_file(self, filename: str, file: any):
      return await self.fs.upload_from_stream(filename, file)
    
    async def download_file(self, file_id: ObjectId):
      return await self.fs.open_download_stream(file_id=file_id)
    
    async def delete_file(self, file_id: ObjectId):
      return await self.fs.delete(file_id)
    
    async def insert_model(self, model_metadata: ModelMetadata):
      """
      Inserts a model metadata into the database.
      """
      model_dict = model_metadata.to_dict()
      result = await self.models_collection.insert_one(model_dict)
      return str(result.inserted_id)  # Return the inserted ID as a string
    
    async def update_one(self, query, update):
      """
      Updates a model metadata in the database.
      """
      return await self.models_collection.update_one(query, update)
      

db_client: AsyncIOMotorClient = None
db_databse = None
db_gridfs: AsyncIOMotorGridFSBucket = None
db_controller: DatabaseController = None

async def connect_to_mongo():
  """Initializes the MongoDB client, database, and GridFS bucket."""
  global db_client, db_database, db_gridfs, db_controller
  db_client = AsyncIOMotorClient(MONGO_URI)
  db_database = db_client[DB_NAME]
  db_gridfs = AsyncIOMotorGridFSBucket(db_database)
  db_controller = DatabaseController(db_client, db_database, db_gridfs)
  print(f"Successfully connected to MongoDB at {MONGO_URI} and initialized GridFS for '{DB_NAME}'.")


async def close_mongo_connection():
  """Closes the MongoDB connection."""
  global db_client
  if db_client:
      db_client.close()
      print("MongoDB connection closed.")


def get_gridfs_bucket() -> AsyncIOMotorGridFSBucket:
  """Dependency for FastAPI to inject the GridFS bucket."""
  if db_gridfs is None:
      raise RuntimeError("MongoDB connection not initialized. Ensure connect_to_mongo() runs on startup.")
  return db_gridfs

def get_db_controller() -> DatabaseController:
  """Dependency for FastAPI to inject the database controller."""
  if db_controller is None:
      raise RuntimeError("MongoDB connection not initialized. Ensure connect_to_mongo() runs on startup.")
  return db_controller
