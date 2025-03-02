from pydantic import BaseModel
from typing import Optional
from config.env_configs import configs
import traceback
import logging


logger = logging.getLogger(__name__)

DEBUG = configs.DEBUG


class ServiceResponse(BaseModel):
    message: str
    status: bool
    status_code: int
    data: Optional[dict] = None


class ServiceException(Exception):

    def __init__(self, **kwargs):
        self.status_code = kwargs.get("message", None)
        self.message = kwargs.get("message", None)
        self.traceback = None
        self._log_exception()

    def _log_exception(self):
        logger.error(self.traceback)
        if DEBUG == True:
            self.traceback = traceback.format_exc()
