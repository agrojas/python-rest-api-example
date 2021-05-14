import abc
from app.domain.users.repository.user_repository import UserRepository


class AbstractUserUnitOfWork(abc.ABC):
    repository: UserRepository

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError
