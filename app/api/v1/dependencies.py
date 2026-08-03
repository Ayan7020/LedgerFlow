from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_async_db_session

from app.repositories import (
    TokenSqlAlchemyRepository,
    UserSQlAlchemyRepository   
)

from app.services import (
    AuthService
)
from app.core import (
    get_config,
    Config
)



def get_auth_service(
    config: Config = Depends(get_config),
    session: AsyncSession = Depends(get_async_db_session)
): 
    return AuthService(
        GOOGLE_CLIENT_ID=config.GOOGLE_CLIENT_ID,
        secret_key=config.SECRET_KEY,
        Session=session,
        User_repo=UserSQlAlchemyRepository(session=session),
        Refresh_token_repo=TokenSqlAlchemyRepository(session=session),
    )