from passlib.context import CryptContext

from app.domain.users.command.user_credentials_command import UserCredentialsCommand
from app.domain.users.model.user import User
from app.domain.users.repository.user_repository import UserRepository


class UserAuthenticationUseCases:
    def __init__(self, user_repository: UserRepository, pwd_context):
        self.user_repository = user_repository
        self.pwd_context = pwd_context

    def find_by_credentials(self, user_command: UserCredentialsCommand) -> User:
        user = self.user_repository.find_by_username(user_command.username)
        if not user:
            return False
        if not self.verify_password(user_command.password, user.password):
            return False
        return user

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    # def get_user(db, username: str):
    #     if username in db:
    #         user_dict = db[username]
    #         return UserInDB(**user_dict)
    #
    #
    # def fake_decode_token(token):
    #     # This doesn't provide any security at all
    #     # Check the next version
    #     user = get_user(fake_users_db, token)
    #     return user
