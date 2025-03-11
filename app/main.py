from fastapi import FastAPI
from app.routes import auth, product, order,notification, analytics, activity, push,order_tracking,inventory,report,promotion,chat,chatbot
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to specific origins for better security
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(product.router, prefix="/products", tags=["Products"])
app.include_router(order.router, prefix="/orders", tags=["Orders"])
app.include_router(notification.router, prefix="/notifications", tags=["Notifications"])
app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
app.include_router(activity.router, prefix="/activity", tags=["User Activity"])
app.include_router(push.router, prefix="/push", tags=["Push Notifications"])
app.include_router(order_tracking.router, prefix="/orders/tracking", tags=["Order Tracking"])
app.include_router(inventory.router, prefix="/inventory", tags=["Inventory"])
app.include_router(report.router, prefix="/reports", tags=["Reports"])
app.include_router(promotion.router, prefix="/promotions", tags=["Promotions"])
app.include_router(chat.router, prefix="/support", tags=["Chat"])
#app.include_router(chatbot.router, prefix="/chatbot", tags=["Chatbot"])
app.include_router(chatbot.router, prefix="/search", tags=["search"])
app.include_router(chatbot.router, prefix="/query", tags=["query"])
app.include_router(chatbot.router, prefix="/search", tags=["upload_docs"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)