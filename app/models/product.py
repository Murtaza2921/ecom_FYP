from pydantic import BaseModel, Field
from typing import Optional,List
from datetime import datetime
from bson import ObjectId

def objectid_to_str(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    return obj

class ProductRequest(BaseModel):
    product_id: str

class ProductCreate(BaseModel):
    actual_price: str
    average_rating: str
    brand: str
    category: str
    crawled_at: str
    description: str
    discount: str
    images: Optional[List[str]] = []
    out_of_stock: bool
    pid: str
    product_details: List[dict]
    seller: str
    selling_price: str
    sub_category: str
    title: str
    url: str


class ProductUpdate(BaseModel):
    actual_price: Optional[str] = None
    average_rating: Optional[str] = None
    brand: Optional[str] = None
    category: Optional[str] = None
    crawled_at: Optional[str] = None
    description: Optional[str] = None
    discount: Optional[str] = None
    images: Optional[List[str]] = None
    out_of_stock: Optional[bool] = None
    pid: Optional[str] = None
    product_details: Optional[List[dict]] = None
    seller: Optional[str] = None
    selling_price: Optional[str] = None
    sub_category: Optional[str] = None
    title: Optional[str] = None
    url: Optional[str] = None


class ProductResponse(ProductCreate):
    id: str
    created_at: datetime
    updated_at: datetime

class ProductResponse(BaseModel):
    id: str
    name: str
    description: str
    price: float
    stock: int
    category: str
    created_at: datetime
    updated_at: datetime

class ProductUpdateResponse(BaseModel):
    message: str

    class Config:
        # This config option tells Pydantic to use the objectid_to_str function
        json_encoders = {
            ObjectId: objectid_to_str
        }

    @classmethod
    def from_mongo(cls, mongo_dict):
        """
        Convert a MongoDB document (which contains _id) to a Pydantic model instance.
        """
        mongo_dict['id'] = str(mongo_dict['_id'])  # Convert _id to id
        del mongo_dict['_id']  # Remove the _id field
        return cls(**mongo_dict)