from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from api.schemas.user import CreateUserSchema, UserSchema
from api.schemas import ServiceResponse
from config.db import get_db
from api.dependencies import get_user_service
from api.services.user import UserService
from api.middlewares.exceptions import exception_before_advice


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
    ).model_dump(exclude_none=True)
    return response
