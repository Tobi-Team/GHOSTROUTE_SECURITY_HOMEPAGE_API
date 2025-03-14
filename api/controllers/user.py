from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from api.schemas.user import (
    AccessTokenSchema,
    CreateUserSchema,
    LoginSchema,
    UserSchema,
    ResendOTPSchema,
    VerifyOTPSchema,
    ResetPasswordSchema,
)
from api.schemas import ServiceResponse
from config.db import get_db
from api.dependencies import get_user_service
from api.services.user import UserService
from api.middlewares.exceptions import exception_before_advice
from fastapi import Request


routes = APIRouter(prefix="/auth", tags=["auth"])


@routes.post("/register", response_model=ServiceResponse)
@exception_before_advice
async def register(
    user_payload: CreateUserSchema,
    user_service: UserService = Depends(get_user_service),
) -> ServiceResponse:
    user: UserSchema = await user_service.create_user(user_payload)
    response: ServiceResponse = ServiceResponse(
        message="User created successfully",
        success=True,
        status_code=201,
        data=user.model_dump(exclude_none=True),
    )
    return response


@routes.post("/login", response_model=ServiceResponse)
@exception_before_advice
async def login(
    login_payload: LoginSchema, user_service: UserService = Depends(get_user_service)
):
    token: AccessTokenSchema = await user_service.login_user(login_payload)
    response: ServiceResponse = ServiceResponse(
        message="User logged in successfully",
        success=True,
        status_code=200,
        data=token.model_dump(),
    )
    return response


@routes.post("/resend-otp", response_model=ServiceResponse)
@exception_before_advice
async def resend_otp(
    resend_otp_payload: ResendOTPSchema,
    user_service: UserService = Depends(get_user_service),
):
    message: str = await user_service.resend_otp(resend_otp_payload)
    response: ServiceResponse = ServiceResponse(
        message=message,
        success=True,
        status_code=200,
    )
    return response


@routes.post("/verify-otp", response_model=ServiceResponse)
@exception_before_advice
async def verify_otp(
    verify_otp_payload: VerifyOTPSchema,
    user_service: UserService = Depends(get_user_service),
):
    verified = await user_service.verify_otp(verify_otp_payload)
    if verified:
        response: ServiceResponse = ServiceResponse(
            message="OTP verified successfully",
            success=True,
            status_code=200,
        )
    else:
        response: ServiceResponse = ServiceResponse(
            message="OTP verification failed",
            success=False,
            status_code=400,
        )
    return response


@routes.post("/forgot-password", response_model=ServiceResponse)
@exception_before_advice
async def forgot_password(
    resend_otp_payload: ResendOTPSchema,
    user_service: UserService = Depends(get_user_service),
):
    message: str = await user_service.resend_otp(resend_otp_payload)
    response: ServiceResponse = ServiceResponse(
        message=message,
        success=True,
        status_code=200,
    )
    return response


@routes.post("/reset-password", response_model=ServiceResponse)
@exception_before_advice
async def reset_password(
    reset_password_payload: ResetPasswordSchema,
    user_service: UserService = Depends(get_user_service),
):
    message: str = await user_service.reset_password(reset_password_payload)
    response: ServiceResponse = ServiceResponse(
        message=message,
        success=True,
        status_code=200,
    )
    return response


@routes.get("/verify-token", response_model=ServiceResponse)
@exception_before_advice
async def verify_token(
    request: Request, user_service: UserService = Depends(get_user_service)
):
    # extract the token from the request header
    token: str = request.headers.get("Authorization").split(" ")[1]
    user: UserSchema = await user_service.verify_token(token)
    response: ServiceResponse = ServiceResponse(
        message="Token verified successfully",
        success=True,
        status_code=200,
        data=user.model_dump(exclude_none=True),
    )
    return response
