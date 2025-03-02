from api.schemas import BaseSchema
from pydantic import Field
from typing import Optional


class CreateUserSchema(BaseSchema):
    username: str
    password: Field(min_length=8, max_length=16)
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
