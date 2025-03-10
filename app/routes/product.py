# app/routers/product.py
from fastapi import APIRouter, HTTPException, Depends
from app.models.product import ProductCreate, ProductResponse, ProductRequest
from app.dependencies.auth import get_current_user
from app.services.product_service import (
    create_product, get_all_products, get_product_by_id
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