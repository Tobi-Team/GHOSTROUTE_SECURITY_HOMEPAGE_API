from functools import wraps
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from api.schemas import InternalServerException, ServiceResponse, ServiceException


async def exception_handler(request: Request, exc: ServiceException) -> ServiceResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=ServiceResponse(
            success=False,
            message=exc.message,
            status_code=exc.status_code,
            data=None,
            traceback=exc.traceback,
        ).model_dump(exclude_none=True),
    )


def exception_before_advice(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            if isinstance(e, ServiceException):
                raise ServiceException(
                    status_code=e.status_code,
                    message=e.message,
                )
            elif isinstance(e, HTTPException):
                raise ServiceException(
                    status_code=e.status_code,
                    message=e.message,
                )
            else:
                raise InternalServerException()

    return wrapper
