import abc
from typing import List

from app.domain.users.model.user import User


class UserRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def add(self, user: User) -> User:
        raise NotImplementedError

    @abc.abstractmethod
    def find_by_username(self, username: str) -> User:
        raise NotImplementedError

    @abc.abstractmethod
    def all(self) -> List[User]:
        raise NotImplementedError

    @abc.abstractmethod
    def total(self) -> int:
        raise NotImplementedError
