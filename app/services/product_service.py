from app.db.database import db
from datetime import datetime
from bson.objectid import ObjectId
from app.models.product import ProductResponse
products_collection = db['products']

def create_product(product_data):
    product = {
        "name": product_data.name,
        "description": product_data.description,
        "price": product_data.price,
        "stock": product_data.stock,
        "category": product_data.category,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    result = products_collection.insert_one(product)
    return str(result.inserted_id)

def get_all_products():
    products = list(products_collection.find({}))
    # Convert MongoDB documents to ProductResponse instances
    return [ProductResponse.from_mongo(product) for product in products]

def get_product_by_id(product_id):
    return products_collection.find_one({"_id": ObjectId(product_id)})

def update_product(product_id, updates):
    updates["updated_at"] = datetime.utcnow()
    products_collection.update_one({"_id": ObjectId(product_id)}, {"$set": updates})

def delete_product(product_id):
    products_collection.delete_one({"_id": ObjectId(product_id)})
