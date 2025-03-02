from sparky_utils.logger import LoggerConfig
import logging
from fastapi import FastAPI
from api.schemas import ServiceException, ServiceResponse
from config import init_db
from api.middlewares.exceptions import exception_handler, exception_before_advice
from api.controllers import router

logger_config = LoggerConfig()


def create_app():
    """Fast API app entry point"""
    logger = logging.getLogger(__name__)

    app = FastAPI(
        title="GHOSTROUTE SECURITY HOMEPAGE API",
        description="GHOSTROUTE SECURITY HOMEPAGE API",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    @app.get("/")
    @exception_before_advice
    async def root():
        logger.info("Hello World")
        return ServiceResponse(
            success=True,
            message="Welcome to Ghost Route  Security Auth Service",
            data=None,
            status_code=200,
        )

    app.include_router(router)
    app.exception_handler(ServiceException)(exception_handler)

    init_db()
    logger.info("Server is running......")

    return app
