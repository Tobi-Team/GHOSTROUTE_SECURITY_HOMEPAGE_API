from fastapi import Depends
from config.db import get_db
from api.repositories.users import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from api.services import RedisService
from api.services.user import UserService


def get_user_repo(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


def get_redis_service() -> RedisService:
    return RedisService()


def get_user_service(
    user_repo: UserRepository = Depends(get_user_repo),
    redis_service: RedisService = Depends(get_redis_service),
):
    return UserService(user_repo, redis_service)
