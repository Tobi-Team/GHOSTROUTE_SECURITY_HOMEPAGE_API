from typing import Optional
from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

env = os.getenv("ENV", "test")


class AppConfigs(BaseSettings):
    DB_URL: str = ""
    TEST_DB_URL: str = ""
    ENV: str = env
    SECRET_KEY: str = ""
    ALGORITHM: str = "HS512"
    ACCESS_TOKEN_EXPIRES: int = 6
    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_PORT: int = 465
    MAIL_USERNAME: str = ""
    MAIL_PASSWORD: str = ""
    MAIL_FROM: str = "default-email@example.com"
    DEBUG: bool = True if env == "dev" else False
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 1


configs = AppConfigs()

__all__ = ["configs"]
