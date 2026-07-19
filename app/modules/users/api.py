from __future__ import annotations

from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.modules.users.dependencies import get_db
from app.modules.users.schemas import UserCreate, UserRead
from app.modules.users.services import UserService

router = APIRouter(prefix="/users", tags=["users"])


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, service: UserService = Depends(get_user_service)) -> UserRead:
    user = service.create_user(payload)
    return UserRead.model_validate(user)


@router.get("/", response_model=list[UserRead])
def list_users(
    x_user_role: str | None = Header(default=None, alias="X-User-Role"),
    service: UserService = Depends(get_user_service),
) -> list[UserRead]:
    if x_user_role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="admin permission required")
    users = service.list_users()
    return [UserRead.model_validate(user) for user in users]
