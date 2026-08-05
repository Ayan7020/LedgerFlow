from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.db import RefreshToken


class TokenSqlAlchemyRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    async def create(self, data: RefreshToken) -> RefreshToken: 
        self.__session.add(data)
        # await self.__session.flush()
        # await self.__session.refresh(data)
        return data

    async def get_by_token(self,token_hash) -> RefreshToken | None:
        result = await self.__session.execute(
            select(RefreshToken).where(RefreshToken.token_hash == token_hash)
        )
        return result.scalar_one_or_none()
