from uuid import UUID

from pydantic import EmailStr
from pydantic.main import BaseModel


class UserResponse(BaseModel):
    username: str
    email: EmailStr
    id: UUID
