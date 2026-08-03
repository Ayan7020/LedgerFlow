from datetime import datetime, timedelta, timezone
import re

from google.oauth2 import id_token
from google.auth.transport import requests

from app.core import ACCESS_TOKEN_EXPIRES_MINUTES, REFRESH_TOKEN_EXPIRES_DAYS, app_logger
from app.core.exceptions import UnauthorizedException, BadRequestException
from app.core.security import hash_token, create_access_token, create_refresh_token

from app.models.Interfaces import IUserRepository, IRefreshTokenRepository, IAsyncSession
from app.models.db import RefreshToken, User
from app.models.http.auth import AuthTokensResult


class AuthService:
    def __init__(
        self,
        GOOGLE_CLIENT_ID: str,
        secret_key: str,
        User_repo: IUserRepository,
        Session: IAsyncSession,
        Refresh_token_repo: IRefreshTokenRepository,
    ):
        self._GOOGLE_CLIENT_ID = GOOGLE_CLIENT_ID
        self._user_repo = User_repo
        self._refresh_token_repo = Refresh_token_repo
        self.__session = Session
        self.__secret_key = secret_key

    async def auth_google(self, token: str) -> AuthTokensResult:
        id_info = self._verify_google_token(token)

        email = id_info.get("email")
        google_sub = id_info.get("sub")

        if not email or not google_sub:
            raise BadRequestException("Google token missing required claims")

        if not id_info.get("email_verified", False):
            raise UnauthorizedException("Google email is not verified")

        user = await self._get_or_create_user(
            email,
            google_sub,
            id_info.get("name"),
        ) 
        
        print("USER: ",user)
        
        access_token = create_access_token(
            user_id=user.id,
            access_token_expire_minutes=ACCESS_TOKEN_EXPIRES_MINUTES,
            key=self.__secret_key,
        )
        raw_refresh_token = create_refresh_token(
            user_id=user.id,
            refresh_token_expire_days=REFRESH_TOKEN_EXPIRES_DAYS,
            key=self.__secret_key,
        )
 
        refresh_token_obj = RefreshToken(
            user_id=user.id,
            token_hash=hash_token(raw_refresh_token),
            expires_at=datetime.now(timezone.utc)
            + timedelta(days=REFRESH_TOKEN_EXPIRES_DAYS),
        )

        await self._refresh_token_repo.create(data=refresh_token_obj)
        print("BEFORE COMMTING")
        await self.__session.commit()

        return AuthTokensResult(
            access_token=access_token,
            refresh_token=raw_refresh_token,
        )

    async def _get_or_create_user(
        self,
        email: str,
        google_sub: str,
        name: str | None,
    ) -> User:
        user = await self._user_repo.get_by_google_sub(google_sub)
        if user:
            return user


        user_name = self._derive_username(email, name) 
        return await self._user_repo.create(
            data=User(
                email=email,
                userName=user_name,
                google_sub=google_sub,
            )
        )

     

    def _derive_username(self, email: str, name: str | None) -> str:
        if not email:
            raise ValueError("Email not found while creating the username")

        if name:
            username = name.strip().lower()
        else:
            username = email.split("@", 1)[0].lower()

        if not username:
            raise ValueError("Could not derive a valid username.")

        return username

    def _verify_google_token(self, token: str) -> dict:
        try:
            return id_token.verify_oauth2_token(
                token,
                requests.Request(),
                self._GOOGLE_CLIENT_ID,
            )
        except ValueError:
            raise UnauthorizedException("Invalid or expired Google token") from None
