from pydantic import EmailStr
from pydantic.main import BaseModel
from typing import Optional
from app.domain.users.command.user_create_command import UserCreateCommand


class UserRequest(BaseModel):
    username: str
    password: str
    full_name: Optional[str] = None
    email: EmailStr

    def to_create_user_command(self):
        return UserCreateCommand(
            username=self.username,
            email=self.email,
            password=self.password,
            full_name=self.full_name,
        )
