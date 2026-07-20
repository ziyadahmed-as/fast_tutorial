from fastapi import FastAPI
from app.api.v1.router import api_router
from app.middleware.request_id import RequestIDMiddleware
from app.middleware.db_session_middleware import DBSessionMiddleware
from app.infrastructure.logger import logger

def create_app() -> FastAPI:
    app = FastAPI(title="FastTutorial ERP", version="0.1.0")
    # Middleware
    app.add_middleware(RequestIDMiddleware)
    app.add_middleware(DBSessionMiddleware)
    # Routers
    app.include_router(api_router)
    return app

app = create_app()
