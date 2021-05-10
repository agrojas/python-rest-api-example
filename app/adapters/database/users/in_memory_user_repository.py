from typing import List

from app.domain.users.model.user import User
from app.domain.users.repository.user_repository import UserRepository


class InMemoryUserRepository(UserRepository):
    def __init__(self, db):
        self.users = db

    def find_by_id(self, id: str) -> User:
        return self.users[id]

    def find_by_username(self, username: str) -> User:
        return list(lambda u: u.username == username, self.users)[0]

    def add(self, user: User) -> User:
        self.users[user.id] = user
        return user

    def all(self) -> List[User]:
        return list(self.users.values())

    def total(self) -> int:
        return len(self.users)
