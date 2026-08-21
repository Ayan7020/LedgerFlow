from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,delete 

from app.models.db import Dealers


class DealerSqlAlchemyRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    async def create(self, data: Dealers) -> Dealers: 
        self.__session.add(data)
        # await self.__session.flush()
        # await self.__session.refresh(data)
        return data
 