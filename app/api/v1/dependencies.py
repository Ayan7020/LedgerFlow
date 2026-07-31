from fastapi import Depends

from app.services import (
    AuthService
)
from app.core import (
    get_config,
    Config
)

def get_auth_service(
    config: Config = Depends(get_config)
): 
    return AuthService(GOOGLE_CLIENT_ID=config.GOOGLE_CLIENT_ID)