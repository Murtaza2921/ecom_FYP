from pymongo import MongoClient
#from app.core.config import settings
from dotenv import load_dotenv
import os

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")


client = MongoClient(MONGO_URI)
db = client['ecommerce']  # Database name
users_collection = db['users']  # Collection name
products_collection = db['products']
