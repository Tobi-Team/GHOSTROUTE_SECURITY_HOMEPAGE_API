from api.repositories.base import BaseRepository
from api.models.user import User
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime


class UserRepository(BaseRepository[User]):
    """User repository for custom db query related to user's domain"""

    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def get_user_by_email(self, email: str) -> User:
        """Get user by email"""
        user = self.session.query(User).filter(User.email == email).first()
        return user

    async def update_last_login(self, user_obj: User) -> User:
        user_obj.last_login = datetime.now()
        updated_user = await self.save(user_obj)
        return updated_user
