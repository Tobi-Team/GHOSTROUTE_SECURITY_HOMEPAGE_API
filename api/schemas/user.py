from api.schemas import BaseSchema
from pydantic import Field, constr
from typing import Optional
from uuid import UUID


class CreateUserSchema(BaseSchema):
    username: str
    password: constr(min_length=8, max_length=16)
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserSchema(BaseSchema):
    id: UUID
    username: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
