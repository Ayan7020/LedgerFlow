from typing import Protocol


class IAsyncSession(Protocol):
    async def commit(self) -> None: ...
