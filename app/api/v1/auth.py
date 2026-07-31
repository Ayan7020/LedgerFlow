from fastapi import APIRouter,Depends

from .dependencies import (
    get_auth_service
)

from app.services import AuthService

auth_router = APIRouter(prefix="/auth",tags=["Auth"])

@auth_router.post("/google")
async def google_auth(token: str,service: AuthService = Depends(get_auth_service)):
    service.auth_google(token)
