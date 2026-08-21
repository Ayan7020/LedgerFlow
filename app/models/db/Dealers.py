from datetime import datetime

from app.db import Base
from app.utils import UNIQUE_ID_TYPE,get_unique_id

from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import Uuid,String,DateTime,ForeignKey

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .User import User

class Dealers(Base):
    __tablename__="dealers"

    user_id: Mapped[UNIQUE_ID_TYPE] = mapped_column(
        Uuid,
        ForeignKey("users.id", ondelete="CASCADE")
    )
    
    name:str = mapped_column(
        String(255),
    )

    id: Mapped[UNIQUE_ID_TYPE] = mapped_column(
        Uuid,
        primary_key=True,
        default_factory=get_unique_id
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now
    )

    user: Mapped["User | None"] = relationship(
        back_populates="dealers",
        init=False
    )
