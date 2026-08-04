from fastapi import APIRouter,Depends,Request

from .dependencies import get_user_service

from app.services import UserService

auth_router = APIRouter(prefix="/user",tags=["User"])

@auth_router.get("/me")
async def get_me(req: Request,service: UserService = Depends(get_user_service)):
    # req.body
    service.get_me()
    
