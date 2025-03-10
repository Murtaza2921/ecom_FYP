from app.db.database import products_collection
from app.services.groq_api import generate_query

def get_products(user_prompt):
    """Generate MongoDB query using Groq API and fetch results."""
    mongo_query = generate_query(user_prompt)  # Generate MongoDB query
    products = list(products_collection.find(mongo_query, {"_id": 0}))  # Query MongoDB

    if len(products) > 1:
        return format_comparison(products)
    
    return products  # Return product details

def format_comparison(products):
    """Format product data for chatbot comparison."""
    return {
        "Comparison": [p["name"] for p in products],
        "Details": [
            {
                "name": p["name"],
                "price": p["price"],
                "stock": p["stock"],
                "category": p["category"],
                "description": p["description"],
                "images": p["images"]
            }
            for p in products
        ]
    }
