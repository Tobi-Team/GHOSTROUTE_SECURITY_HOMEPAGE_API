from api.schemas import BaseSchema
from pydantic import Field, constr
from typing import Optional


class CreateUserSchema(BaseSchema):
    username: str
    password: constr(min_length=8, max_length=16)  # Use constr for min and max length
    email: str
    first_name: Optional[str]
    last_name: Optional[str]


class UserSchema(BaseSchema):
    id: int
    username: str
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
