from app.db.database import db
from datetime import datetime
from bson.objectid import ObjectId
from app.models.product import ProductResponse,ProductCreate
products_collection = db['products']

# def create_product(product_data: ProductCreate):
#     product = {
#         "name": product_data.name,
#         "description": product_data.description,
#         "price": product_data.price,
#         "stock": product_data.stock,
#         "category": product_data.category,
#         "images": product_data.images,  # Add images here
#         "created_at": datetime.utcnow(),
#         "updated_at": datetime.utcnow()
#     }
#     result = products_collection.insert_one(product)
#     return str(result.inserted_id)

def create_product(product_data: ProductCreate):
    product = {
        "actual_price": product_data.actual_price,
        "average_rating": product_data.average_rating,
        "brand": product_data.brand,
        "category": product_data.category,
        "crawled_at": datetime.utcnow().strftime("%d/%m/%Y, %H:%M:%S"),
        "description": product_data.description,
        "discount": product_data.discount,
        "images": product_data.images,
        "out_of_stock": product_data.out_of_stock,
        "pid": product_data.pid,
        "product_details": product_data.product_details,
        "seller": product_data.seller,
        "selling_price": product_data.selling_price,
        "sub_category": product_data.sub_category,
        "title": product_data.title,
        "url": product_data.url,
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

# def update_product(product_id, updates):
#     updates["updated_at"] = datetime.utcnow()
#     products_collection.update_one({"_id": ObjectId(product_id)}, {"$set": updates})


def updateProduct(product_id, updates):
    try:
        # Ensure the product_id is an ObjectId
        product_id = ObjectId(product_id)
        
        # Add the updated_at field to the update dictionary
        updates["updated_at"] = datetime.utcnow()
        
        # Perform the update operation
        result = products_collection.update_one(
            {"_id": product_id},  # Filter by the product ID
            {"$set": updates}  # Set the new values
        )
        
        # Check if the product was updated
        if result.modified_count > 0:
            return {"success": True, "message": "Product updated successfully."}
        else:
            return {"success": False, "message": "No changes made, the product may not exist or is already up to date."}
    
    except Exception as e:
        return {"success": False, "message": f"Error updating product: {str(e)}"}


def delete_product(product_id):
    products_collection.delete_one({"_id": ObjectId(product_id)})



