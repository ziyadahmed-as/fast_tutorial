from sqlalchemy.orm import declarative_base
from .base import BaseMixin

# Declarative base class used by all models
Base = declarative_base(cls=BaseMixin)
