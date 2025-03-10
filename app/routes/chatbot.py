from fastapi import APIRouter,HTTPException
from app.services.chatbot_service import get_products
from app.services.groq_api import generate_query

from pydantic import BaseModel

router = APIRouter()

class ChatRequest(BaseModel):
    message: str  # User input message

@router.post("/chatbot/")
async def chatbot_api(request: ChatRequest):
    user_prompt = request.message
    query = generate_query(user_prompt)  # Generate MongoDB query
    results = get_products(user_prompt)  # Fetch data from MongoDB

    if not results:
        raise HTTPException(status_code=404, detail="No products found")

    return {"response": results}
