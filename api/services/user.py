from api.schemas.user import CreateUserSchema
from api.repositories.users import UserRepository
from api.dependencies import get_user_repo
from fastapi import Depends


class UserService:
    
    def __init__(self, user_repo: UserRepository = Depends(get_user_repo)):
        self.user_repo = user_repo
        
    
        