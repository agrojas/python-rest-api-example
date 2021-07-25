import logging
from typing import List

import uuid as uuid
from app.domain.users.auth.password_encoder import PasswordEncoder
from app.domain.users.command.user_create_command import UserCreateCommand
from app.domain.users.command.user_update_status_command import UpdateUserStatusCommand
from app.domain.users.model.user import User
from app.domain.users.model.user_id import UserId
from app.domain.users.repository.unit_of_work import AbstractUserUnitOfWork


class UserUseCases:
    def __init__(self, user_uow: AbstractUserUnitOfWork, pwd_encoder: PasswordEncoder):
        self.user_uow: AbstractUserUnitOfWork = user_uow
        self.pwd_encoder = pwd_encoder

    def list(self) -> List[User]:
        return self.user_uow.repository.all()

    def register(self, user_command: UserCreateCommand) -> User:
        user_id = UserId(str(uuid.uuid4()))
        try:
            user = User(
                id=user_id,
                username=user_command.username,
                email=user_command.email,
                full_name=user_command.full_name,
                password=self.pwd_encoder.encode(user_command.password),
            )
            self.user_uow.repository.save(user)
            self.user_uow.commit()
            return self.user_uow.repository.find_by_id(user_id)
        except Exception as e:
            logging.error(e)
            self.user_uow.rollback()
            raise

    def find_by_username(self, username: str):
        return self.user_uow.repository.find_by_username(username)

    def find_by_id(self, user_id: str):
        return self.user_uow.repository.find_by_id(UserId(user_id))

    def update_status(
        self, update_user_status_command: UpdateUserStatusCommand
    ) -> User:
        user = self.user_uow.repository.find_by_id(update_user_status_command.user_id)
        user.update_status(update_user_status_command.status)
        self.user_uow.repository.save(user)
        self.user_uow.commit()
        return user
