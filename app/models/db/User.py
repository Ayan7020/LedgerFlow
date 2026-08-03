from app.db import Base
from app.utils import UNIQUE_ID_TYPE, get_unique_id

from sqlalchemy import String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .RefreshToken import RefreshToken


class User(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
    )

    userName: Mapped[str] = mapped_column(
        String(60),
        unique=True,
    )

    google_sub: Mapped[str | None] = mapped_column(
        String(255),
        unique=True,
        index=True,
        default=None,
    )

    id: Mapped[UNIQUE_ID_TYPE] = mapped_column(
        Uuid,
        primary_key=True,
        default_factory=get_unique_id,
    )

    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(
        back_populates="user",
        default_factory=list,
    )
