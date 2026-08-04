from fastapi import APIRouter

from .auth import auth_router
from .user import user_router

V1Router = APIRouter(prefix="/api/v1")

V1Router.include_router(auth_router)
V1Router.include_router(user_router)

