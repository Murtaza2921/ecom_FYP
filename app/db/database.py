from pymongo import MongoClient
from app.core.config import settings

client = MongoClient(settings.MONGO_URI)
db = client['ecommerce']  # Database name
users_collection = db['users']  # Collection name
