from fastapi import Depends
from config.db import get_db
from api.repositories.users import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from api.services import RedisService


def get_user_repo(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


def get_redis_service() -> RedisService:
    return RedisService()
