from sqlalchemy.orm import DeclarativeBase

from basic_template.db.meta import meta


class Base(DeclarativeBase):
    """Base for all models."""

    metadata = meta
