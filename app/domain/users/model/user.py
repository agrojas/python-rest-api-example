import uuid
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    # This is necessary to prevent circular imports
    from app.domain.users.repository.user_repository import UserRepository


@dataclass
class User:
    username: str
    email: str
    password: str
    id: uuid.UUID = uuid.uuid4()
    full_name: Optional[str] = None

    def save(self, user_repository: 'UserRepository'):
        return user_repository.add(self)

    def __hash__(self):
        return hash(self.id)
