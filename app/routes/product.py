# app/routers/product.py
from fastapi import APIRouter, HTTPException, Depends
from app.models.product import ProductCreate, ProductResponse, ProductRequest,ProductUpdate,ProductUpdateResponse
from app.dependencies.auth import get_current_user
from datetime import datetime
from app.services.product_service import (
    create_product, get_all_products, get_product_by_id,updateProduct,delete_product
)

router = APIRouter()
 #, current_user: dict = Depends(get_current_user)
@router.post("/", response_model=str)
def add_product(product: ProductCreate):
    product_id = create_product(product)
    return product_id

@router.get("/", response_model=list[ProductResponse])
def list_products(current_user: dict = Depends(get_current_user)):
    return get_all_products()

@router.get("/fetch-product", response_model=ProductResponse)
def fetch_product(request: ProductRequest, current_user: dict = Depends(get_current_user)):
    product = get_product_by_id(request.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    # Convert _id to id (string) before returning
    product["id"] = str(product["_id"])  # Convert ObjectId to string
    del product["_id"]
    return product

@router.put("/{product_id}", response_model=ProductUpdateResponse)
async def update_product(product_id: str, product: ProductUpdate):
    update_data = {k: v for k, v in product.dict(exclude_unset=True).items()}
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided for update")
    
    update_data["updated_at"] = datetime.utcnow()
    result = updateProduct(product_id,update_data)
    #result = products_collection.update_one({"_id": product_id}, {"$set": update_data})
    
    # if result.matched_count == 0:
    #     raise HTTPException(status_code=404, detail="Product not found")
    
    return {"message": "Product updated successfully."}


@router.delete("/{product_id}", response_model=ProductUpdateResponse)
async def delete_product_by_id(product_id: str):
    # Use the service function to delete the product
    result = delete_product(product_id)
    
    # If delete operation doesn't match any product (i.e., no product was deleted), raise 404
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Return a success message
    return {"message": "Product deleted successfully."}