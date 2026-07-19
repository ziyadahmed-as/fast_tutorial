"""Validation helpers for the user module."""

from app.core.exceptions import ValidationError


class UserValidator:
    @staticmethod
    def ensure_supported_role(role: str | None) -> str:
        normalized_role = (role or "member").lower()
        if normalized_role not in {"member", "admin"}:
            raise ValidationError("role must be either member or admin")
        return normalized_role
