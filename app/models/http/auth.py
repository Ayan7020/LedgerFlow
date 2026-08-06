from dataclasses import dataclass
from pydantic import BaseModel

@dataclass(frozen=True)
class AuthTokensResult:
    access_token: str
    refresh_token: str

class AuthGoogleRequest(BaseModel):
    token: str