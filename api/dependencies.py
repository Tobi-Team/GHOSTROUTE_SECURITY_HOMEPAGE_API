from fastapi import Depends
from config.db import get_db
from api.repositories.users import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession


def get_user_repo(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db)
