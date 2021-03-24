import random
import string


import uuid
from dataclasses import dataclass
from typing import TYPE_CHECKING

from pydantic import Field

if TYPE_CHECKING:
    # This is necessary to prevent circular imports
    from app.domain.users.repository.user_repository import UserRepository


@dataclass
class User:
    username: str
    email: str
    secret: str
    id: uuid.UUID

    def __init__(self, username, email, id=uuid.uuid4()):
        self.id = id
        self.username = username
        self.email = email
        self.secret = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

    def save(self, user_repository: 'UserRepository'):
        return user_repository.add(self)

    def __hash__(self):
        return hash(self.id)
