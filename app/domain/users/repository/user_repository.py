import abc
from typing import List

from app.domain.users.model.user import User
from app.domain.users.model.user_id import UserId


class UserRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def save(self, user: User):
        raise NotImplementedError

    @abc.abstractmethod
    def find_by_id(self, user_id: UserId) -> User:
        raise NotImplementedError

    @abc.abstractmethod
    def find_by_username(self, username: str) -> User:
        raise NotImplementedError

    @abc.abstractmethod
    def find_by_email_or_username(self, email: str, username: str) -> User:
        raise NotImplementedError

    @abc.abstractmethod
    def find_by_email(self, email: str) -> User:
        raise NotImplementedError

    @abc.abstractmethod
    def all(self) -> List[User]:
        raise NotImplementedError

    @abc.abstractmethod
    def total(self) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, user: User):
        raise NotImplementedError
