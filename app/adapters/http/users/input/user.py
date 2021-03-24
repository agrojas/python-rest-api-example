from pydantic import EmailStr
from pydantic.main import BaseModel

from app.domain.users.command.user_create_command import UserCreateCommand


class UserRequest(BaseModel):
    username: str
    email: EmailStr

    def to_create_user_command(self):
        return UserCreateCommand(username=self.username, email=self.email)
