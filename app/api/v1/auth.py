from fastapi import APIRouter,Depends,Response
from app.core import REFRESH_COOKIE_MAX_AGE
from .dependencies import (
    get_auth_service
)

from app.services import AuthService

auth_router = APIRouter(prefix="/auth",tags=["Auth"])

@auth_router.post("/google")
async def google_auth(token: str,response: Response,service: AuthService = Depends(get_auth_service)):
    result = await service.auth_google(token)
    
    response.set_cookie(
        key="refresh_token",
        value=result.refresh_token,
        httponly=True,
        secure=False,          
        samesite="lax",       
        max_age=REFRESH_COOKIE_MAX_AGE,           
    )
    
    return {
        "success": True,
        "message": "Authenticated",
        "data": {"access_token": result.access_token, "token_type": "bearer"},
    }
