from pydantic import EmailStr, Field
from pydantic.main import BaseModel
from typing import Optional
from app.domain.users.command.user_create_command import UserCreateCommand
from app.domain.users.model.user_status import UserStatus


class UserRequest(BaseModel):
    username: str = Field(example="username")
    password: str = Field(example="secure")
    full_name: Optional[str] = Field(example="Full Name")
    email: EmailStr = Field(example="username@mail.com")

    def to_create_user_command(self):
        return UserCreateCommand(
            username=self.username,
            email=self.email,
            password=self.password,
            full_name=self.full_name,
        )


class UserStatusRequest(BaseModel):
    status: UserStatus
