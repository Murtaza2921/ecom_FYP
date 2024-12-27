from fastapi import FastAPI
from app.routes import auth, product, order,notification, analytics, activity, push,order_tracking,inventory,report,promotion,chat

app = FastAPI()

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)