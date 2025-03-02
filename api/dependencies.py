from fastapi import Depends
from config.db import get_db
from api.repositories.users import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from api.services import RedisService


def get_user_repo(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


def get_redis_service() -> RedisService:
    return RedisService()


def get_user_service(
    user_repo: UserRepository = Depends(get_user_repo),
    redis_service: RedisService = Depends(get_redis_service),
):
    from api.services.user import UserService

    return UserService(user_repo, redis_service)


__all__ = ["get_user_service", "get_redis_service", "get_user_repo"]
