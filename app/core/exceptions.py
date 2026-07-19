"""Application-specific exception types."""


class AppError(Exception):
    """Base error for domain and application layer failures."""


class ConflictError(AppError):
    """Raised when a requested resource conflicts with existing state."""


class ValidationError(AppError):
    """Raised when input data violates business rules."""
