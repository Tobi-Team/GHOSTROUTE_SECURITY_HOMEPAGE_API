from api.repositories.base import BaseRepository
from api.models.user import User
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository(BaseRepository[User]):
    """User repository for custom db query related to user's domain"""

    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    def get_user_by_email(self, email: str) -> User:
        """Get user by email"""
        return self.session.query(User).filter(User.email == email).first()
