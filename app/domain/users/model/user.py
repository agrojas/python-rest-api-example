from typing import TYPE_CHECKING, Optional

from pydantic.main import BaseModel

from app.domain.users.model.user_id import UserId

if TYPE_CHECKING:
    # This is necessary to prevent circular imports
    from app.domain.users.repository.user_repository import UserRepository


class User(BaseModel):
    id: UserId
    username: str
    email: str
    password: str
    full_name: Optional[str] = None
    is_active: Optional[bool] = True

    def save(self, user_repository: 'UserRepository'):
        return user_repository.add(self)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id
