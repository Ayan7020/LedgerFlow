from fastapi import Depends,Request,Security
from fastapi.security import APIKeyHeader

from jwt import DecodeError, ExpiredSignatureError, InvalidSignatureError
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import UnauthorizedException,BadRequestException
from app.db.session import get_async_db_session

from app.repositories import (
    TokenSqlAlchemyRepository,
    UserSQlAlchemyRepository,
    DealerSqlAlchemyRepository 
)

from app.services import (
    AuthService,
    UserService,
    DealerService
)
from app.core import (
    app_logger,
    get_config,
    Config
)

from app.core.security import (
    verify_access_token
)

access_token_header = APIKeyHeader(
    name="access_token",
    auto_error=False,
)

def get_current_user(
    req: Request, 
    config: Config = Depends(get_config),
    access_token_header: str | None = Security(access_token_header),
):  
    try: 
        access_token = req.cookies.get("access_token") or access_token_header
        if not access_token:
            raise BadRequestException("Access token missing")
        
        payload = verify_access_token(access_token,config.SECRET_KEY)
        user_id = payload.get("sub")
        if user_id is None:
            pass  
        return str(user_id)
    
    except ExpiredSignatureError:
        app_logger.warning("JWT has expired")
        raise UnauthorizedException("Invalid Jwt Token")

    except InvalidSignatureError:
        app_logger.warning("JWT signature is invalid")
        raise UnauthorizedException("Invalid Jwt Token")

    except DecodeError as exc: 
        app_logger.opt(exception=exc).critical("Malformed JWT") 
        raise UnauthorizedException("Invalid Jwt Token")
    
    

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

def get_user_service(
    session: AsyncSession = Depends(get_async_db_session)
):
    return UserService(
        user_repo=UserSQlAlchemyRepository(session=session)
    )

def get_dealer_service(
    session: AsyncSession = Depends(get_async_db_session)
):
    return DealerService(
        repo=DealerSqlAlchemyRepository(session=session),
        Session=session
    )