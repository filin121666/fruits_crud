from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

from core.config import settings


class Base(DeclarativeBase):
    metadata = MetaData(
        naming_convention=settings.database.naming_convention,
    )
