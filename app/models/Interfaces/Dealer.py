from typing import Protocol

from app.models.db import Dealers


class IDealerRepository(Protocol): 

    async def create(self, data: Dealers) -> Dealers: ...
