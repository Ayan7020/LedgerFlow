from app.core.observability import tracing

from app.models.Interfaces import IDealerRepository,IAsyncSession
from app.models.db import Dealers

from app.utils import UNIQUE_ID_TYPE

class DealerService:
    def __init__(
            self, 
            repo: IDealerRepository,
            Session: IAsyncSession,
        ): 
        self.__repo = repo
        self.__session = Session

    @tracing("DealerService.create")
    async def create(self,name: str,created_by_id: UNIQUE_ID_TYPE) -> None: 
        dealer = Dealers(
            name=name,
            user_id=created_by_id
        )

        await self.__repo.create(data=dealer)
        await self.__session.commit()

        return None