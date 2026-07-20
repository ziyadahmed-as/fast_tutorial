from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.exceptions import AppError, ConflictError, ValidationError
from app.core.logging import configure_logging
from app.modules.users.api import router as users_router
from app.modules.users.dependencies import create_session_factory


def create_app(database_url: str | None = None) -> FastAPI:
    configure_logging()
    app = FastAPI(
        title="ERP Platform Foundation",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    app.state.db_session_factory = create_session_factory(database_url or "sqlite:///./app.db")
    app.include_router(users_router, prefix="/api/v1")

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(_request: Request, exc: RequestValidationError) -> JSONResponse:
        return JSONResponse(status_code=422, content={"detail": exc.errors()})

    @app.exception_handler(AppError)
    async def app_exception_handler(_request: Request, exc: AppError) -> JSONResponse:
        if isinstance(exc, ConflictError):
            status_code = 409
        elif isinstance(exc, ValidationError):
            status_code = 400
        else:
            status_code = 400
        return JSONResponse(status_code=status_code, content={"detail": str(exc)})

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
