from fastapi import APIRouter
from api.controllers import user


router = APIRouter(
    prefix="/api/v1",
)


router.include_router(user.routes)
