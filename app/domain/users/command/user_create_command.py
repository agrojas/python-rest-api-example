from typing import Optional

from pydantic import EmailStr
from pydantic.main import BaseModel


class UserCreateCommand(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: Optional[str] = None
