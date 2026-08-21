from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,delete 

from app.models.db import Dealers
from app.utils import UNIQUE_ID_TYPE

class DealerSqlAlchemyRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    async def create(self, data: Dealers) -> Dealers: 
        self.__session.add(data)
        # await self.__session.flush()
        # await self.__session.refresh(data)
        return data

    async def get_all_by_user_id(self,user_id: UNIQUE_ID_TYPE) -> list[Dealers]:
        result = await self.__session.execute(
            select(Dealers).where(Dealers.user_id == user_id)
        )

        return result.scalars().all()

 