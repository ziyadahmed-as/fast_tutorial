from __future__ import annotations

from typing import Generator

from fastapi import Request
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.modules.users.models import Base


def create_session_factory(database_url: str = "sqlite:///./app.db"):
    engine_kwargs = {"future": True}
    if database_url.startswith("sqlite:///:memory:"):
        engine_kwargs.update(
            {
                "connect_args": {"check_same_thread": False},
                "poolclass": StaticPool,
            }
        )
    engine = create_engine(database_url, **engine_kwargs)
    Base.metadata.create_all(bind=engine)
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db(request: Request) -> Generator[Session, None, None]:
    session_factory = request.app.state.db_session_factory
    db = session_factory()
    try:
        yield db
    finally:
        db.close()
