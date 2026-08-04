from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.db import User


class UserSQlAlchemyRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    async def get_by_google_sub(self, sub: str) -> User | None:
        result = await self.__session.execute(
            select(User).where(User.google_sub == sub)
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        result = await self.__session.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> User | None:
        result = await self.__session.execute(
            select(User).where(User.userName == username)
        )
        return result.scalar_one_or_none()

    async def create(self, data: User) -> User: 
        self.__session.add(data) 
        # await self.__session.flush()
        # await self.__session.refresh(data) 
        return data
