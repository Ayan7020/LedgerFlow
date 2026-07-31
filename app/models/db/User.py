from app.db import Base
from app.utils import UNIQUE_ID_TYPE,get_unique_id

from sqlalchemy import String,Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

class User(Base):
    __tablename__="users"

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True
    )

    userName: Mapped[str] = mapped_column(
        String(60),
        unique=True
    )

    id: Mapped[UNIQUE_ID_TYPE] =  mapped_column(
        Uuid,
        primary_key=True,
        default_factory=get_unique_id
    )