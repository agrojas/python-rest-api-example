from typing import List

from app.domain.users.command.user_create_command import UserCreateCommand
from app.domain.users.model.user import User
from app.domain.users.repository.user_repository import UserRepository


class UserUseCases:

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def list(self) -> List[User]:
        return self.user_repository.all()

    def register(self, user_command: UserCreateCommand) -> User:
        return User(username=user_command.username, email=user_command.email).save(self.user_repository)
