from .base import ModelBase
from sqlalchemy import Boolean, Column, DateTime
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import event
import bcrypt
from datetime import datetime


class User(ModelBase):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}
    __mapper_args__ = {"polymorphic_identity": "users"}
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    username = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=True)
    verified = Column(Boolean, nullable=True, default=False)
    is_active = Column(Boolean, nullable=False, default=True)
    is_admin = Column(Boolean, nullable=False, default=False)
    is_superuser = Column(Boolean, nullable=False, default=False)
    last_login = Column(DateTime, nullable=True)

    def check_password(self, password):
        """
        Compare provided password with stored hashed password

        Args:
            password (str): The password to check

        Returns:
            bool: True if password matches, False otherwise
        """
        if not self.password or not password:
            return False

        return bcrypt.checkpw(password.encode("utf-8"), self.password.encode("utf-8"))


@event.listens_for(User, "before_insert")
def hash_password_before_insert(mapper, connection, target):
    if target.password:
        # Generate a salt and hash the password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(target.password.encode("utf-8"), salt)
        target.password = hashed_password.decode("utf-8")


@event.listens_for(User, "before_update")
def update_updated_at(mapper, connection, target):
    target.updated_at = datetime.now()
