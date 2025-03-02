from pydantic import BaseModel, ConfigDict
from typing import Optional
from config.env_configs import configs
import traceback
import logging


logger = logging.getLogger(__name__)

DEBUG = configs.DEBUG


class BaseSchema(BaseModel):
    model_config = {"from_attributes": True}


class ServiceResponse(BaseSchema):
    message: str
    success: bool
    status_code: int
    data: Optional[dict] = None


class ServiceErrorResponse(BaseSchema):
    message: str
    success: bool
    status_code: int
    traceback: Optional[str] = None


class ServiceException(Exception):

    def __init__(self, **kwargs):
        self.status_code = kwargs.get("status_code", None)
        self.message = kwargs.get("message", None)
        self.traceback = None
        self.success: bool = False
        self._log_exception()

    def _log_exception(self):
        logger.error(self.traceback)
        if DEBUG == True:
            traceback.print_exc()


class InternalServerException(ServiceException):

    def __init__(self) -> None:
        super().__init__(status_code=500, message="Don't panic, this is from us!")
        if DEBUG == True:
            traceback.print_exc()
            self.traceback = traceback.format_exc()
        else:
            self.traceback = None
