from uuid import UUID, uuid4

from pydantic import EmailStr, Field
from pydantic.main import BaseModel


class UserResponse(BaseModel):
    username: str
    email: EmailStr
    id: UUID

    class Config:
        orm_mode = True
