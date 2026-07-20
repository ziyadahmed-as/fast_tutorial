"""Application-specific exception types."""


class AppError(Exception):
    """Base error for domain and application layer failures."""


class ConflictError(AppError):
    """Raised when a requested resource conflicts with existing state."""


class ValidationError(AppError):
    """Raised when input data violates business rules."""

from fastapi import HTTPException
from starlette import status

class BusinessException(HTTPException):
    def __init__(self, detail: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(status_code=status_code, detail=detail)
