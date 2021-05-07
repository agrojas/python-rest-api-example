from typing import List

from passlib.context import CryptContext

from app.domain.users.command.user_create_command import UserCreateCommand
from app.domain.users.model.user import User
from app.domain.users.repository.user_repository import UserRepository


class UserUseCases:
    def __init__(self, user_repository: UserRepository, pwd_context: CryptContext):
        self.user_repository = user_repository
        self.pwd_context = pwd_context

    def list(self) -> List[User]:
        return self.user_repository.all()

    def register(self, user_command: UserCreateCommand) -> User:
        return User(
            username=user_command.username,
            email=user_command.email,
            full_name=user_command.full_name,
            password=self.pwd_context.hash(user_command.password),
        ).save(self.user_repository)

    def find_by_username(self, username: str):
        return self.user_repository.find_by_username(username)
