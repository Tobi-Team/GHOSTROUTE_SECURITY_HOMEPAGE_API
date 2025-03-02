from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from api.schemas.user import CreateUserSchema, UserSchema
from api.schemas import ServiceResponse
from config.db import get_db
from api.dependencies import get_user_service
from api.services.user import UserService


routes = APIRouter(prefix="/auth", tags=["auth"])


@routes.post("/register", response_model=ServiceResponse)
async def register(
    user_payload: CreateUserSchema,
    user_service: UserService = Depends(get_user_service),
) -> ServiceResponse:
    user: UserSchema = await user_service.create_user(user_payload)
    return ServiceResponse(
        message="User created successfully",
        success=True,
        status_code=201,
        data=user,
    )
