from typing import Optional

from app.domain.users.auth.password_encoder import PasswordEncoder
from app.domain.users.command.user_credentials_command import UserCredentialsCommand
from app.domain.users.model.user import User
from app.domain.users.repository.unit_of_work import AbstractUserUnitOfWork


class UserAuthenticationUseCases:
    def __init__(self, user_uow: AbstractUserUnitOfWork, pwd_encoder: PasswordEncoder):
        self.user_uow = user_uow
        self.pwd_encoder = pwd_encoder

    def find_by_credentials(
        self, user_command: UserCredentialsCommand
    ) -> Optional[User]:
        user = self.user_uow.repository.find_by_username(user_command.username)
        if not user:
            return None
        if not self.verify_password(user_command.password, user.password):
            return None
        return user

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_encoder.verify(plain_password, hashed_password)
