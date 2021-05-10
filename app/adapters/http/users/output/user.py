from uuid import UUID
from typing import Optional

from pydantic import EmailStr
from pydantic.main import BaseModel


class UserId(BaseModel):
    id: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    username: str
    full_name: Optional[str] = None
    email: EmailStr
    id: UserId

    class Config:
        orm_mode = True
