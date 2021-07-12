import unittest
import uuid
from unittest.mock import MagicMock

from app.domain.users.command.user_create_command import UserCreateCommand
from app.domain.users.model.user import User
from app.domain.users.model.user_id import UserId
from app.domain.users.usecases.user_usecases import UserUseCases


class TestUserUseCases(unittest.TestCase):
    uow = MagicMock()
    pwd_encoder = MagicMock()

    def test_list_empty(self):
        user_usecases = UserUseCases(self.uow, self.pwd_encoder)
        self.uow.repository.all = MagicMock(return_value=[])
        self.assertEqual([], user_usecases.list())

    def test_list_with_results(self):
        user_id = UserId(id=str(uuid.uuid4()))
        user_mock = User(
            id=user_id, username='mock', email='email@mail.com', password='aaaa'
        )
        self.uow.repository.all = MagicMock(return_value=[user_mock])
        user_usecases = UserUseCases(self.uow, self.pwd_encoder)
        self.assertEqual(user_usecases.list(), [user_mock])

    def test_register(self):
        user_id = UserId(id=str(uuid.uuid4()))
        user_mock = User(
            id=user_id, username='mock', email='email@mail.com', password='aaaa'
        )
        self.uow.repository.save = MagicMock(return_value=user_mock)
        self.pwd_encoder.encode = MagicMock(return_value='aaaa')
        user_usecases = UserUseCases(self.uow, self.pwd_encoder)
        user_register = UserCreateCommand(
            username='mock', email='email@mail.com', password='1234'
        )
        self.assertIsNotNone(user_usecases.register(user_register))


if __name__ == '__main__':
    unittest.main()
