from fastapi import APIRouter

from .auth import auth_router

V1Router = APIRouter(prefix="/api/v1")

V1Router.include_router(auth_router)

