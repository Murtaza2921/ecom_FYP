from fastapi import FastAPI, HTTPException, APIRouter,BackgroundTasks, UploadFile, File
from pydantic import BaseModel
import re
import json
from dotenv import load_dotenv
import os
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from pymongo import MongoClient
from langchain_groq import ChatGroq
from app.services.chatbot_service import query_groq, format_price_in_filter, ecomm_agent, process_and_store_documents
from bson import ObjectId
from decimal import Decimal

load_dotenv()
router = APIRouter()
MONGO_URI = "mongodb+srv://ghulammurtaza:estrats1122@cluster0.mlylm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DATABASE_NAME = "ecommerce"
COLLECTION_NAME = "products"

# MongoDB client
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# Helper function to convert ObjectId to string
def str_objectid(obj_id):
    return str(obj_id) if isinstance(obj_id, ObjectId) else obj_id

# Helper function to handle decimal prices
def format_price(price):
    if isinstance(price, (Decimal, float, int)):  
        return str(price)  # Convert numbers to string
    return price  # Return as-is if it's already a string
# Define the request model
class SearchRequest(BaseModel):
    query: str

UPLOAD_DIR = "uploaded_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Define the product model based on MongoDB document
class Product(BaseModel):
    id: str
    name: str
    description: str
    price: str  # Assuming price is stored as a Decimal type in MongoDB
    stock: int
    category: str
    images: list
    created_at: str
    updated_at: str

    class Config:
        # Convert MongoDB ObjectId and Decimal to str
        json_encoders = {
            ObjectId: str,
            Decimal: lambda v: str(v)
        }

@router.post("/")
async def search_product(search_request: SearchRequest):
    query = search_request.query  # Extract the query from the request body

    # Extract the MongoDB query from the user query using Groq
    try:
        filter_query, projection = query_groq(query)
        filter_query = format_price_in_filter(filter_query)  # Format the filter_query
        print("Generated MongoDB filter:", filter_query)  # Log the generated filter
        print("Generated MongoDB projection:", projection)  # Log the generated projection
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query with Groq: {str(e)}")

    # Query the database using the generated filter and projection
    try:
        # Apply filter and projection
        products_cursor = collection.find(filter_query, projection)

        # Apply sorting (if specified in the query)
        if "sort" in query.lower():
            products_cursor = products_cursor.sort("average_rating", -1)  # Sort by average_rating in descending order

        # Apply limit (if specified in the query)
        if "top" in query.lower() or "limit" in query.lower():
            limit_match = re.search(r"top\s+(\d+)", query, re.IGNORECASE)
            if limit_match:
                limit = int(limit_match.group(1))
                products_cursor = products_cursor.limit(limit)

        # Convert the cursor to a list of products
        product_list = [
            Product(
                id=str_objectid(product.get("_id")),
                name=product.get("name", "N/A"),
                description=product.get("description", "N/A"),
                price=format_price(product.get("price", "N/A")),
                stock=product.get("stock", 0),
                category=product.get("category", "N/A"),
                images=product.get("images", []),
                created_at=str(product.get("created_at", "")),
                updated_at=str(product.get("updated_at", ""))
            )
            for product in products_cursor
        ]

        if not product_list:
            raise HTTPException(status_code=404, detail="No products found")
        
        top_products = product_list[:5]

        # Format the response in a human-like way
        response_message = f"I found the following products:\n\n"
        for product in top_products:
            response_message += (
                f"- **{product.name}** (Category: {product.category}, "
                f"Price: {product.price}, Stock: {product.stock}, "
                f"Availability: {'Available' if product.stock > 0 else 'Out of stock'})\n"
            )

        return {"message": response_message, "products": top_products}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error querying the database: {str(e)}")


@router.post("/query")
def query_ecomm_agent(user_query: SearchRequest):
    """
    Unified endpoint to handle product & company queries.
    Routes the query to MongoDB Query Tool or RAG Tool dynamically.
    """
    try:
        response = ecomm_agent.run(user_query)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# ✅ Endpoint to Upload Documents into ChromaDB (RAG)
@router.post("/upload-docs")
async def upload_documents(files: list[UploadFile] = File(...)):
    """
    Uploads multiple documents (PDF, DOCX, CSV) and stores them in ChromaDB.
    """
    file_paths = []
    
    for file in files:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        
        with open(file_path, "wb") as f:
            f.write(await file.read())
        
        file_paths.append(file_path)

    # Process and store documents in ChromaDB
    process_and_store_documents(file_paths)

    return {"message": "Files uploaded and processed successfully"}