from passlib.context import CryptContext

from app.domain.users.auth.password_encoder import PasswordEncoder


class ByCryptPasswordEncoder(PasswordEncoder):
    def __init__(self, pwd_context: CryptContext):
        self.pwd_context = pwd_context

    def encode(self, password):
        return self.pwd_context.hash(password)

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)
