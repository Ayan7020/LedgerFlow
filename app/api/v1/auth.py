from fastapi import APIRouter,Depends,Response,Request
from app.core import REFRESH_COOKIE_MAX_AGE,ACCESS_TOKEN_EXPIRES_SECONDS
from .dependencies import (
    get_auth_service
)
from app.core.exceptions import BadRequestException

from app.services import AuthService
from app.models.http import AuthGoogleRequest

auth_router = APIRouter(prefix="/auth",tags=["Auth"])

@auth_router.post("/google")
async def google_auth(body: AuthGoogleRequest,response: Response,service: AuthService = Depends(get_auth_service)):
    result = await service.auth_google(body.token)
    
    return {
        "success": True,
        "message": "Authenticated",
        "data": { "_id": result.id,"access_token": result.access_token,"refresh_token": result.refresh_token },
    }

@auth_router.get("/refresh-access-token")
async def refresh_access_token(request: Request,response: Response,service: AuthService = Depends(get_auth_service)):
    refresh_token = request.cookies.get("refresh_token",None)
    if not refresh_token:
        BadRequestException("Please provide the refresh token")

    result = await service.refresh_access_token(refresh_token) 

    return {
        "success": True,
        "message": "",
        "data": { 
            "access_token": result.access_token
        },
    }
