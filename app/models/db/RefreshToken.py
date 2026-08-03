from app.db import Base
from app.utils import UNIQUE_ID_TYPE, get_unique_id

from sqlalchemy import String, Uuid, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from datetime import datetime, timezone

if TYPE_CHECKING:
    from .User import User


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    user_id: Mapped[UNIQUE_ID_TYPE] = mapped_column(
        Uuid,
        ForeignKey("users.id", ondelete="CASCADE")
    )

    token_hash: Mapped[str] = mapped_column(
        String(72),
        unique=True,
        index=True,
    )

    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    revoked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        default=None,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default_factory=lambda: datetime.now(timezone.utc),
    )

    id: Mapped[UNIQUE_ID_TYPE] = mapped_column(
        Uuid,
        primary_key=True,
        default_factory=get_unique_id,
    )

    user: Mapped["User | None"] = relationship(
        back_populates="refresh_tokens",
        init=False,
    )
