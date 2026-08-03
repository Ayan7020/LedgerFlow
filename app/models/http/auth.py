from dataclasses import dataclass


@dataclass(frozen=True)
class AuthTokensResult:
    access_token: str
    refresh_token: str
