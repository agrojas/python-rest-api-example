import abc


class PasswordEncoder(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def encode(self, password: str) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def verify(self, plain_password: str, hashed_password: str) -> bool:
        raise NotImplementedError()
