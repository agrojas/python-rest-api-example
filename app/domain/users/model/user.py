import datetime
from typing import Optional, Union

from pydantic import BaseModel, Field
from pydantic.schema import date

from app.domain.users.model.user_exceptions import UserAlreadyHadStatusError
from app.domain.users.model.user_id import UserId
from app.domain.users.model.user_status import UserStatus


class User(BaseModel):
    id: UserId = Field(example="123e4567-e89b-12d3-a456-426614174000")
    username: str = Field(example="username")
    email: str = Field(example="username@mail.com")
    password: str = Field(example="secure")
    full_name: Optional[str] = Field(example="Full Name")
    status: Optional[UserStatus] = Field(UserStatus.ACTIVE, example=UserStatus.ACTIVE)
    created_at: Union[str, date, None] = Field(example="Full Name")
    updated_at: Union[str, date, None] = Field(example="Full Name")

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def update_status(self, status: UserStatus):
        if self.status == status:
            raise UserAlreadyHadStatusError()
        self.status = status

    def is_blocked(self):
        return UserStatus.BLOCKED == self.status
