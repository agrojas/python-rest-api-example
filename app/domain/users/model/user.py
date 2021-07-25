from typing import Optional

from pydantic.main import BaseModel

from app.domain.users.model.user_id import UserId


class User(BaseModel):
    id: UserId
    username: str
    email: str
    password: str
    full_name: Optional[str] = None
    is_active: Optional[bool] = True

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def update_status(self, status):
        self.is_active = status
