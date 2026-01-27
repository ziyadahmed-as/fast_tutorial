from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ecommerce.database import engine, Base
from ecommerce.routes.auth_routes import router as auth_router
from ecommerce.routes.category_routes import router as category_router
from ecommerce.routes.product_routes import router as product_router
from ecommerce.routes.cart_routes import router as cart_router
from ecommerce.routes.order_routes import router as order_router

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="E-Commerce API",
    description="A simple e-commerce API built with FastAPI",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(category_router)
app.include_router(product_router)
app.include_router(cart_router)
app.include_router(order_router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to E-Commerce API",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
