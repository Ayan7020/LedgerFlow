from dataclasses import dataclass
from pydantic import BaseModel
from app.utils import UNIQUE_ID_TYPE

@dataclass(frozen=True)
class AuthTokensResult: 
    access_token: str
    refresh_token: str

class AuthGoogleRequest(BaseModel):
    token: str