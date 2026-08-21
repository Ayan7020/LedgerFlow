from fastapi import APIRouter,Depends

from .dependencies import (
    get_current_user, 
    get_dealer_service
)

from app.services import DealerService
from app.models.http import CreateDealerRequest

dealer_router = APIRouter(prefix="/dealer",tags=["Dealer"])

@dealer_router.post("/create")
async def create_dealer(body: CreateDealerRequest,current_user_id:str = Depends(get_current_user),service: DealerService = Depends(get_dealer_service)): 
    await service.create(name=body.name,created_by_id=current_user_id)  
    return {
        "success": True,
        "message": "Dealer created successfully",
        "data": {}
    }

@dealer_router.post("/get-all")
async def get_all_dealers(current_user_id:str = Depends(get_current_user),service: DealerService = Depends(get_dealer_service)): 
    dealers = await service.get_all(user_id=current_user_id)  
    return {
        "success": True,
        "message": "",
        "data": {
            "dealers": [dealer.name for dealer in dealers]
        }
    }
