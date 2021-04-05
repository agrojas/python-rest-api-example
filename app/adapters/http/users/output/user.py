from uuid import UUID
from typing import Optional

from pydantic import EmailStr
from pydantic.main import BaseModel


class UserResponse(BaseModel):
    username: str
    full_name: Optional[str] = None
    email: EmailStr
    id: UUID

    class Config:
        orm_mode = True
