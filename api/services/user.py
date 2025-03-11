from datetime import datetime, timedelta, timezone
from api.schemas.user import (
    AccessTokenSchema,
    CreateUserSchema,
    LoginSchema,
    UserSchema,
    ResendOTPSchema,
    VerifyOTPSchema,
)
from api.repositories.users import UserRepository
from api.dependencies import get_user_repo, get_redis_service
from fastapi import Depends
from api.middlewares.exceptions import exception_before_advice
from api.models.user import User
from utils.utils import generate_otp
from api.schemas import ServiceResponse
from api.tasks import send_verification_code
from api.services import RedisService
from utils.utils import mapper
from config.env_configs import configs
from api.schemas import ServiceException
from jose import jwt
from jose.exceptions import JWTClaimsError, JWTError, ExpiredSignatureError


class UserService:

    def __init__(
        self,
        user_repo: UserRepository = Depends(get_user_repo),
        redis_service: RedisService = Depends(get_redis_service),
    ):

        self.user_repo = user_repo
        self.redis_service = redis_service

    async def _generate_token(self, user: UserSchema) -> AccessTokenSchema:
        expires_at = datetime.now(tz=timezone.utc) + timedelta(
            days=configs.ACCESS_TOKEN_EXPIRES
        )
        now = datetime.now(tz=timezone.utc)

        # Calculate the difference in time
        time_difference = expires_at - now

        # Convert the difference to minutes (as integer)
        expires_in_minutes = int(time_difference.total_seconds() // 60)
        claims = {
            "id": str(user.id),
            "sub": user.username,
            "email": user.email,
            "exp": expires_at,
        }

        token_type = "bearer"
        try:
            token = jwt.encode(
                claims,
                configs.SECRET_KEY,
                configs.ALGORITHM,
            )
        except JWTError:
            raise ServiceException(status_code=401, message="Invalid access token!")
        return AccessTokenSchema(
            access_token=token,
            token_type=token_type,
            expires_at=expires_in_minutes,
        )

    async def verify_token(self, token: str) -> UserSchema:
        try:
            payload = jwt.decode(
                token,
                configs.SECRET_KEY,
                configs.ALGORITHM,
            )
            user_email = payload.get("email")
            user = await self.user_repo.get_user_by_email(user_email)
            if not user:
                raise ServiceException(status_code=404, message="User not found!")
            user_schema = UserSchema.model_validate(user)
            return user_schema
        except ExpiredSignatureError:
            raise ServiceException(status_code=401, message="Token has expired!")
        except JWTClaimsError:
            raise ServiceException(status_code=401, message="Invalid token claims!")
        except JWTError:
            raise ServiceException(status_code=401, message="Invalid token!")

    async def create_user(self, user: CreateUserSchema) -> UserSchema:
        model_instance = mapper(user, User)
        created_user: User = await self.user_repo.save(model_instance)

        new_user: UserSchema = UserSchema.model_validate(created_user)
        username: str = new_user.username
        email: str = new_user.email
        otp: str = generate_otp()
        # cache otp
        await self.redis_service.set(f"{email}_otp", otp)
        send_verification_code.apply_async(args=[email, otp, username])
        return new_user

    async def resend_otp(self, resend_otp_schema: ResendOTPSchema) -> str:
        otp: str = generate_otp()
        user_email: str = resend_otp_schema.email
        # get user by email
        user: User = await self.user_repo.get_user_by_email(user_email)
        if not user:
            raise ServiceException(status_code=404, message="User not found!")
        username: str = user.username
        # cache otp
        await self.redis_service.set(f"{user_email}_otp", otp)
        send_verification_code.apply_async(args=[user_email, otp, username])
        message: str = "OTP Resent Successfully"
        return message

    async def verify_otp(self, verify_otp_schema: VerifyOTPSchema):
        # get otp from redis
        otp = verify_otp_schema.otp
        email = verify_otp_schema.email
        cached_otp: str = await self.redis_service.get(f"{email}_otp")
        if not cached_otp:
            raise ServiceException(status_code=400, message="OTP has expired!")
        if cached_otp.upper() != otp.upper():
            raise ServiceException(status_code=400, message="Invalid OTP!")
        # get user by email
        user: User = await self.user_repo.get_user_by_email(email)
        if not user:
            raise ServiceException(status_code=404, message="User not found!")
        # update user status
        user.is_verified = True
        _ = await self.user_repo.save(user)
        # delete otp from redis
        _ = await self.redis_service.delete(f"{email}_otp")
        return True

    async def login_user(self, user: LoginSchema) -> AccessTokenSchema:
        user_obj: User = await self.user_repo.get_user_by_email(user.email)
        if not user_obj:
            raise ServiceException(status_code=404, message="User not found!")
        if not user_obj.check_password(user.password):
            raise ServiceException(status_code=401, message="Invalid credentials!")
        # update last_login
        _ = await self.user_repo.update_last_login(user_obj)
        dumped_user: UserSchema = UserSchema.model_validate(user_obj)
        # generate access token for the user
        token_response: AccessTokenSchema = await self._generate_token(dumped_user)
        return token_response
