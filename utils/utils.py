import random
import string
import traceback
from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from config.env_configs import configs
from pydantic import BaseModel, EmailStr
from api.models.base import Base
from typing import TypeVar


T = TypeVar("T", bound=Base)  # type: ignore

conf = ConnectionConfig(
    MAIL_USERNAME=configs.MAIL_USERNAME,
    MAIL_PASSWORD=configs.MAIL_PASSWORD,
    MAIL_FROM=configs.MAIL_FROM,
    MAIL_PORT=int(configs.MAIL_PORT),
    MAIL_SERVER=configs.MAIL_SERVER,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER="templates",
)


class EmailSchema(BaseModel):
    email: EmailStr
    subject: str
    message: str
    username: str


async def send_mail(mail_payload: EmailSchema) -> None:
    """Sends an email

    Args:
        mail_payload (EmailSchema): Email DTO
        background_tasks (BackgroundTasks): fast api background task instance
    """
    try:
        message = MessageSchema(
            subject=mail_payload.subject,
            recipients=[mail_payload.email],
            template_body={
                "name": mail_payload.username,
                "message": mail_payload.message,
            },
            subtype="html",
        )

        fm = FastMail(conf)
        background_tasks = BackgroundTasks()
        background_tasks.add_task(
            fm.send_message, message, template_name="registration_verification.html"
        )
        await background_tasks()
    except Exception:
        traceback.print_exc()


def generate_otp(length: int = 6) -> str:
    """Generates a random alphanumeric one-time password (OTP).

    Args:
        length (int): Length of the OTP to be generated. Defaults to 6.

    Returns:
        str: Alphanumeric OTP generated.
    """
    characters = string.ascii_letters + string.digits
    otp = "".join(random.choice(characters) for _ in range(length))
    return otp.upper()


def mapper(schema: T, model_obj: T) -> T:
    """Maps a schema object to a model object.

    Args:
        schema (T): Schema object.
        model_obj (T): Model object.

    Returns:
        T: Mapped model object.
    """
    return model_obj(**schema.dict())
