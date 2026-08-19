from typing import Protocol

from app.models.db import RefreshToken


class IRefreshTokenRepository(Protocol):
    async def create(self, data: RefreshToken) -> RefreshToken: ...

    async def get_by_token(self,token_hash: str) -> RefreshToken | None: ...

    async def remove_token(self,token_hash: str) -> int: ...