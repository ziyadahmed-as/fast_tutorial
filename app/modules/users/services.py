from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError, ValidationError
from app.core.security import hash_password, verify_password
from app.modules.users.models import User
from app.modules.users.repositories import UserRepository
from app.modules.users.schemas import UserCreate
from app.modules.users.validators import UserValidator


class UserService:
    def __init__(self, session: Session) -> None:
        self.repository = UserRepository(session)
        self.session = session

    def create_user(self, payload: UserCreate) -> User:
        if self.repository.get_by_email(str(payload.email)) is not None:
            raise ConflictError("A user with this email already exists")

        role = UserValidator.ensure_supported_role(payload.role)
        if role == "admin" and not payload.role:
            raise ValidationError("admin role requires explicit assignment")

        user = User(
            email=str(payload.email),
            password_hash=hash_password(payload.password),
            full_name=payload.full_name,
            role=role,
            is_active=True,
        )
        return self.repository.add(user)

    def list_users(self) -> list[User]:
        return list(self.repository.list_all())

    def authenticate(self, email: str, password: str) -> User | None:
        user = self.repository.get_by_email(email)
        if user is None:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user
