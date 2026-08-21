from typing import Protocol

from app.models.db import Dealers
from app.utils import UNIQUE_ID_TYPE

class IDealerRepository(Protocol): 

    async def create(self, data: Dealers) -> Dealers: ...
    async def get_all_by_user_id(self, user_id: UNIQUE_ID_TYPE) -> list[Dealers]: ...

