from jose import jwt, JWTError

from app.adapters.http.auth.exceptions.authentication_exception import (
    AuthenticationException,
)
from app.domain.users.model.user_exceptions import UsersBlockedException
from app.domain.users.usecases.user_usecases import UserUseCases
from app.conf.config import Settings
from app.domain.users.model.user import User


class Authenticator:
    def __init__(self, user_usecases: UserUseCases, settings: Settings):
        self.user_usecases = user_usecases
        self.secret_key = settings.secret_key
        self.algorithm = settings.algorithm

    def authenticate(self, token: str) -> User:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            username: str = payload.get("sub")
            if username is None:
                raise AuthenticationException()
        except JWTError:
            raise AuthenticationException()
        user = self.user_usecases.user_uow.repository.find_by_username(
            username=username
        )
        if user is None:
            raise AuthenticationException()
        if user.is_blocked():
            raise UsersBlockedException()
        return user
