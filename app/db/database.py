from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve the Mongo URI from environment variables
# MONGO_URI = os.getenv("MONGO_URI")
MONGO_URI = "mongodb+srv://ghulammurtaza:estrats1122@cluster0.mlylm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Initialize MongoDB client
client = MongoClient(MONGO_URI)

# Function to check the connection to MongoDB
def check_connection():
    try:
        # Attempt to get server info to verify the connection
        client.server_info()  # This will raise an exception if the connection fails
        print("MongoDB connection successful!")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")

# Check the connection
check_connection()

# Access the database and collections
db = client['ecommerce']  # Database name
users_collection = db['users']  # Collection name for users
products_collection = db['products']  # Collection name for products
