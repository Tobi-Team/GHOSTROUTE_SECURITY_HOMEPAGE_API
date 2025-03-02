from api.schemas.user import CreateUserSchema, UserSchema
from api.repositories.users import UserRepository
from api.dependencies import get_user_repo, get_redis_service
from fastapi import Depends
from api.middlewares.exceptions import exception_before_advice
from api.models.user import User
from utils.utils import generate_otp
from api.schemas import ServiceResponse
from api.tasks import send_verification_code
from api.services import RedisService


class UserService:

    def __init__(
        self,
        user_repo: UserRepository = Depends(get_user_repo),
        redis_service: RedisService = Depends(get_redis_service),
    ):
        self.user_repo = user_repo

    async def create_user(self, user: CreateUserSchema) -> UserSchema:
        created_user: User = await self.user_repo.save(user)

        new_user: UserSchema = UserSchema.model_validate(created_user)
        username: str = new_user.username
        email: str = new_user.email
        otp: str = generate_otp()
        # cache otp
        await self.redis_service.set(f"{email}_otp", otp)
        send_verification_code.delay(email, otp, username)
        return new_user
