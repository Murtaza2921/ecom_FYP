# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# import re
# import json
# from dotenv import load_dotenv
# import os
# from langchain.prompts import PromptTemplate
# from langchain.schema.runnable import RunnablePassthrough
# from pymongo import MongoClient
# from langchain_groq import ChatGroq

# load_dotenv()


# MONGO_URI = os.getenv("MONGO_URI")
# #DATABASE_NAME = os.getenv("DATABASE_NAME")
# #COLLECTION_NAME = os.getenv("COLLECTION_NAME")
# DATABASE_NAME = "ecommerce"
# COLLECTION_NAME = "products"

# # MongoDB client
# client = MongoClient(MONGO_URI)
# db = client[DATABASE_NAME]
# collection = db[COLLECTION_NAME]

# GROQ_API_KEY = "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"

# groq_chat = ChatGroq(api_key=GROQ_API_KEY,temperature=0.7, model_name="mixtral-8x7b-32768")

# # Define the request model
# class SearchRequest(BaseModel):
#     query: str

# # Define the updated product model
# class Product(BaseModel):
#     id: str
#     name: str
#     description: str
#     price: float
#     stock: int
#     category: str
#     images: list
#     created_at: int
#     updated_at: int


# # Function to format the price in the filter_query
# def format_price_in_filter(filter_query):
#     if isinstance(filter_query, dict):
#         for key, value in filter_query.items():
#             if key == "price":
#                 # Handle cases where price is a comparison operator (e.g., {'$lt': 2000})
#                 if isinstance(value, dict):
#                     for op, op_value in value.items():
#                         if isinstance(op_value, (int, float, str)) and str(op_value).replace('.', '', 1).isdigit():
#                             value[op] = float(op_value)  # Ensure it's formatted as a float
#                 elif isinstance(value, (int, float, str)) and str(value).replace('.', '', 1).isdigit():
#                     filter_query[key] = float(value)  # Convert price to float
#             elif isinstance(value, dict):
#                 format_price_in_filter(value)
#             elif isinstance(value, list):
#                 for item in value:
#                     if isinstance(item, dict):
#                         format_price_in_filter(item)
#     return filter_query


# def validate_projection(projection):
#     """
#     Ensures MongoDB projection does not mix inclusion (1) and exclusion (0).
#     - If mixed, defaults to inclusion (1) and removes all exclusions (0).
#     - Always ensures `_id` handling is consistent.
#     """
#     if not projection:
#         return {}

#     inclusion_fields = {k: v for k, v in projection.items() if v == 1}
#     exclusion_fields = {k: v for k, v in projection.items() if v == 0 and k != "_id"}  # Exclude _id from check

#     if inclusion_fields and exclusion_fields:
#         print("Warning: Mixed inclusion and exclusion found. Defaulting to inclusion only.")
#         return inclusion_fields  # Keep only inclusion fields

#     return projection  # If valid, return as-is


# def query_groq(user_query: str):
#     """
#     Use ChatGroq to interpret the user query and generate a MongoDB query.
#     """
#     try:
#         # Prepare the prompt for the Groq model
#         prompt = PromptTemplate(
#             input_variables=["user_query"],
#             template=(
#                 "You are tasked with generating a MongoDB query based on a user query.\n"
#                 "The query should be based on a product schema with the following fields:\n"
#                 "  - _id (ObjectId as String)\n"
#                 "  - name (String)\n"
#                 "  - description (String)\n"
#                 "  - price (Float)\n"
#                 "  - stock (Integer)\n"
#                 "  - category (String)\n"
#                 "  - images (Array of Strings, optional)\n"
#                 "  - created_at (Timestamp as Integer)\n"
#                 "  - updated_at (Timestamp as Integer)\n"
                
#                 "Generate a MongoDB query that:\n"
#                 "- Applies filters on the fields based on the user query.\n"
#                 "- Specifies the fields to return in the result (projection).\n"
#                 "- The projection must only include field inclusion/exclusion (e.g., 1 or 0).\n"
#                 "- Do not include aggregation expressions (e.g., $substr, $cond) in the projection.\n"
#                 "- Sorts the results if specified by the user.\n"
#                 "- Limits the number of results if specified by the user.\n"
#                 "- The `price` field must be treated as a float in both the filter and projection.\n"
#                 "Format the response as a valid JSON object with two keys: 'filter' and 'projection'.\n"
#                 "Do not include explanations or additional text.\n"
#                 "Here is the user query: {user_query}"
#             )
#         )

#         # Create a RunnableSequence with the prompt and LLM
#         chain = (
#             {"user_query": RunnablePassthrough()}  # Pass the user query directly
#             | prompt  # Apply the prompt template
#             | groq_chat  # Use the LLM to generate the response
#         )

#         # Run the chain with the user query
#         response = chain.invoke(user_query)
#         print(f"Groq Response: {response}")  # Log the response

#         # Extract the content from the AIMessage object
#         response_text = response.content

#         # Use regex to extract the JSON object from the response
#         json_match = re.search(r"\{.*\}", response_text, re.DOTALL)
#         if not json_match:
#             raise ValueError("No JSON object found in the response.")

#         json_str = json_match.group(0)

#         # Parse the MongoDB query from the response
#         try:
#             query_dict = json.loads(json_str)
#             filter_query = query_dict.get("filter", {})
#             projection = query_dict.get("projection", {})

#             # Remove invalid keys like $limit and $sort from the filter
#             if "$limit" in filter_query:
#                 del filter_query["$limit"]
#             if "$sort" in filter_query:
#                 del filter_query["$sort"]

#             # Ensure the projection follows MongoDB rules
#             projection = validate_projection(projection)

#             return filter_query, projection
#         except json.JSONDecodeError as e:
#             raise ValueError(f"Failed to parse MongoDB query from response: {json_str}")
#     except Exception as e:
#         print(f"Groq Error: {e}")
#         raise HTTPException(status_code=500, detail=f"Error processing query with Groq: {str(e)}")

import os
import json
import re
import PyPDF2
import docx
import csv
import chromadb
from pymongo import MongoClient
from fastapi import HTTPException
from langchain import PromptTemplate
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType
from langchain_groq import ChatGroq
from sentence_transformers import SentenceTransformer

# ✅ MongoDB Connection
mongo_client = MongoClient("mongodb+srv://ghulammurtaza:estrats1122@cluster0.mlylm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = mongo_client["ecommerce"]
products_collection = db["products"]

# ✅ Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path="chroma_db")
# ✅ Initialize Groq API
GROQ_API_KEY = "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"
groq_chat = ChatGroq(api_key=GROQ_API_KEY, temperature=0.7, model_name="mixtral-8x7b-32768")

# ✅ Initialize embedding function
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def get_chroma_collection():
    """Ensures collection exists and returns it lazily."""
    collection_name = "rag_docs"
    try:
        return chroma_client.get_collection(collection_name)
    except ValueError:
        print(f"Collection '{collection_name}' not found. Creating new collection...")
        return chroma_client.create_collection(name=collection_name)
 

# ✅ Query Groq to Generate MongoDB Query
def query_groq(user_query: str):
    try:
        prompt = PromptTemplate(
            input_variables=["user_query"],
            template=(
                "You are tasked with generating a MongoDB query based on a user query.\n"
                "The query should be based on a product schema with the following fields:\n"
                "- _id (ObjectId as String)\n"
                "- name (String)\n"
                "- description (String)\n"
                "- price (Float)\n"
                "- stock (Integer)\n"
                "- category (String)\n"
                "- images (Array of Strings, optional)\n"
                "- created_at (Timestamp as Integer)\n"
                "- updated_at (Timestamp as Integer)\n\n"
                "Generate a MongoDB query that:\n"
                "- Applies filters on the fields based on the user query.\n"
                "- Specifies the fields to return in the result (projection).\n"
                "- The projection must only include field inclusion/exclusion (e.g., 1 or 0).\n"
                "- Do not include aggregation expressions (e.g., $substr, $cond) in the projection.\n"
                "- Sorts the results if specified by the user.\n"
                "- Limits the number of results if specified by the user.\n"
                "- The `price` field must be treated as a float in both the filter and projection.\n"
                "Format the response as a valid JSON object with two keys: 'filter' and 'projection'.\n"
                "Here is the user query: {user_query}"
            )
        )

        groq_chat = ChatGroq(api_key=GROQ_API_KEY, temperature=0.7, model_name="mixtral-8x7b-32768")

        response = groq_chat.invoke(prompt.format(user_query=user_query))

        json_match = re.search(r"\{.*\}", response.content, re.DOTALL)
        if not json_match:
            raise ValueError("No JSON object found in response.")

        query_dict = json.loads(json_match.group(0))
        return query_dict.get("filter", {}), query_dict.get("projection", {})

    except Exception as e:
        return f"Groq Query Error: {str(e)}"

# ✅ Query MongoDB for Products
def query_mongodb(user_query: str):
    try:
        filter_query, projection = query_groq(user_query)
        products = list(products_collection.find(filter_query, projection))

        for product in products:
            product["_id"] = str(product["_id"])

        return products
    except Exception as e:
        return f"MongoDB Query Error: {str(e)}"

# ✅ Extract Text from Files
def extract_text(file_path):
    ext = file_path.split(".")[-1].lower()

    if ext == "pdf":
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            return " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
    
    elif ext == "docx":
        doc = docx.Document(file_path)
        return " ".join([para.text for para in doc.paragraphs])
    
    elif ext == "csv":
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            return " ".join([" ".join(row) for row in reader])
    
    return None

def process_and_store_documents(file_paths):
    """Extract text, generate embeddings, and store in ChromaDB."""
    collection = get_chroma_collection()  # ✅ Ensure collection exists only when needed
    
    for file_path in file_paths:
        text = extract_text(file_path)
        if text:
            embedding = embedding_model.encode(text).tolist()
            collection.add(
                documents=[text],
                embeddings=[embedding],
                ids=[os.path.basename(file_path)]
            )

# ✅ Query ChromaDB (RAG)
def query_rag(user_query: str):
    try:
        collection = get_chroma_collection()  # ✅ Ensure collection exists only when needed
        query_embedding = embedding_model.encode([user_query]).tolist()
        results = collection.query(query_embeddings=query_embedding, n_results=3)
        return results["documents"]
    except Exception as e:
        return f"RAG Query Error: {str(e)}"


# Function to format the price in the filter_query
def format_price_in_filter(filter_query):
    if isinstance(filter_query, dict):
        for key, value in filter_query.items():
            if key == "price":
                # Handle cases where price is a comparison operator (e.g., {'$lt': 2000})
                if isinstance(value, dict):
                    for op, op_value in value.items():
                        if isinstance(op_value, (int, float, str)) and str(op_value).replace('.', '', 1).isdigit():
                            value[op] = float(op_value)  # Ensure it's formatted as a float
                elif isinstance(value, (int, float, str)) and str(value).replace('.', '', 1).isdigit():
                    filter_query[key] = float(value)  # Convert price to float
            elif isinstance(value, dict):
                format_price_in_filter(value)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        format_price_in_filter(item)
    return filter_query




# ✅ Define Ecomm Agent tools
tools = [
    Tool(name="MongoDB Query Tool", func=query_mongodb, description="Search products in MongoDB"),
    Tool(name="RAG Tool", func=query_rag, description="Retrieve company info from ChromaDB")
]

# ✅ Initialize the Ecomm Agent
ecomm_agent = initialize_agent(
    agent=AgentType.OPENAI_FUNCTIONS,
    tools=tools,
    llm=groq_chat,
    verbose=True
)

# ✅ Query Ecomm Agent
def query_ecomm_agent(user_query: str):
    try:
        return ecomm_agent.run(user_query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
