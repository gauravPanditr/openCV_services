import os
from pymongo import MongoClient
import gridfs
from dotenv import load_dotenv


load_dotenv()


MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")
GRIDFS_BUCKET = os.getenv("GRIDFS_BUCKET")


client = MongoClient(MONGO_URI)
db = client[MONGO_DB]

fs = gridfs.GridFS(db)


col = db[GRIDFS_BUCKET]