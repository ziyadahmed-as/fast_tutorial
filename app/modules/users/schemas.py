from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, field_validator


class UserCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    email: str
    password: str = Field(min_length=8, max_length=128)
    full_name: str = Field(min_length=2, max_length=255)
    role: str | None = Field(default=None, pattern=r"^(member|admin)$")

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("password must be at least 8 characters")
        if not any(char.isdigit() for char in value):
            raise ValueError("password must contain at least one digit")
        if not any(char.isalpha() for char in value):
            raise ValueError("password must contain at least one letter")
        return value

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        if "@" not in value:
            raise ValueError("email must be a valid address")
        return value


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    full_name: str
    role: str
    is_active: bool


class UserListItem(UserRead):
    pass
