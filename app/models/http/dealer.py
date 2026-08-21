from pydantic import BaseModel 
 

class CreateDealerRequest(BaseModel):
    name: str