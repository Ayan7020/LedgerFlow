  
import jwt
from datetime import datetime, timedelta, timezone
from uuid import UUID 



ALGORITHM = "HS256"


def _create_token(
    user_id: UUID | str,
    token_type: str,
    expires_delta: timedelta,
    key: str,
    algorithm: str,
) -> str:
    now = datetime.now(timezone.utc)

    payload = {
        "sub": str(user_id),
        "type": token_type,
        "iat": now,
        "exp": now + expires_delta,
    }

    return jwt.encode(payload, key=key, algorithm=algorithm)


def create_access_token(
    user_id: UUID | str,
    access_token_expire_minutes: int,
    key: str,
) -> str:
    return _create_token(
        user_id=user_id,
        token_type="access",
        expires_delta=timedelta(minutes=access_token_expire_minutes),
        algorithm=ALGORITHM,
        key=key,
    )


def create_refresh_token(
    user_id: UUID | str,
    refresh_token_expire_days: int,
    key: str,
) -> str:
    return _create_token(
        user_id=user_id,
        token_type="refresh",
        expires_delta=timedelta(days=refresh_token_expire_days),
        algorithm=ALGORITHM,
        key=key,
    )


def verify_access_token(token: str,key: str): 
    payload = jwt.decode(
        jwt=token,
        key=key,
        algorithms=[ALGORITHM]
    )
    return payload