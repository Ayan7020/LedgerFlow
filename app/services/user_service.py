from app.models.Interfaces import IUserRepository
from app.core.exceptions import UnauthorizedException

class UserService:
    def __init__(
            self,
            user_repo: IUserRepository
        ):
        self.__user_repo = user_repo

    async def get_me(self,user_id: str):  
        user = await self.__user_repo.get_by_user_id(user_id)
        if user == None:
            raise UnauthorizedException("User not found")  
        return user