from typing import Optional

from pydantic import EmailStr, validator
from pydantic.main import BaseModel


class UserId(BaseModel):
    id: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    username: str
    full_name: Optional[str]
    email: EmailStr
    id: UserId
    status: Optional[str]

    @validator('id')
    def map_id(cls, v):
        return v.id

    class Config:
        orm_mode = True
