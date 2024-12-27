from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId

def objectid_to_str(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    return obj

class ProductRequest(BaseModel):
    product_id: str

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    stock: int
    category: str

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