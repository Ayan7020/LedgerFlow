from fastapi import APIRouter,Depends

from .dependencies import (
    get_current_user,
    get_user_service
)

from app.services import UserService

user_router = APIRouter(prefix="/user",tags=["User"])

@user_router.get("/me")
async def get_me(current_user_id:str = Depends(get_current_user),service: UserService = Depends(get_user_service)): 
    user = await service.get_me(user_id=current_user_id)  
    return {
        "success": True,
        "message": "User Info Fetched",
        "data": {
            "_id": user.id,
            "email": user.email
        }
    }
