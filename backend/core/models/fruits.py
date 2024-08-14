from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from core.models import Base
from core.models.mixins import IdPkMixin


class FruitModel(Base, IdPkMixin):
    __tablename__ = "fruits"

    title: Mapped[str] = mapped_column(String(64), nullable=False)
    price: Mapped[int] = mapped_column(nullable=False, default=0)
    description: Mapped[str] = mapped_column()
