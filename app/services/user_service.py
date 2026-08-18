from app.core import app_logger
from app.core.exceptions import UnauthorizedException
from app.core.observability import tracing

from app.models.Interfaces import IUserRepository

class UserService:
    def __init__(
            self,
            user_repo: IUserRepository
        ):
        self.__user_repo = user_repo

    @tracing("UserService.get_me")
    async def get_me(self,user_id: str):  
        user = await self.__user_repo.get_by_user_id(user_id)
        if user == None:
            app_logger.warning("User not found")
            raise UnauthorizedException("User not found")  
        return user