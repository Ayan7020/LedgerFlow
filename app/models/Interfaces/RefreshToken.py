from typing import Protocol

from app.models.db import RefreshToken


class IRefreshTokenRepository(Protocol):
    async def create(self, data: RefreshToken) -> RefreshToken: ...
