import unittest
from unittest.mock import MagicMock

from app.adapters.database.users.in_memory_user_repository import InMemoryUserRepository
from app.domain.users.command.user_create_command import UserCreateCommand
from app.domain.users.model.user import User
from app.domain.users.usecases.user_usecases import UserUseCases


class TestUserUseCases(unittest.TestCase):
    db = {}
    repository = InMemoryUserRepository(db)
    pwd_context = MagicMock()

    def test_list_empty(self):
        user_usecases = UserUseCases(self.repository, self.pwd_context)
        self.repository.all = MagicMock(return_value=[])
        self.assertEqual(user_usecases.list(), [])

    def test_list_with_results(self):
        user_mock = User(username='mock', email='email@mail.com', password='aaaa')
        self.repository.all = MagicMock(return_value=[user_mock])
        user_usecases = UserUseCases(self.repository, self.pwd_context)
        self.assertEqual(user_usecases.list(), [user_mock])

    def test_register(self):
        user_mock = User(username='mock', email='email@mail.com', password='aaaa')
        self.repository.save = MagicMock(return_value=user_mock)
        self.pwd_context.hash = MagicMock(return_value='aaaa')
        user_usecases = UserUseCases(self.repository, self.pwd_context)
        user_register = UserCreateCommand(
            username='mock', email='email@mail.com', password='1234'
        )
        self.assertIsNotNone(user_usecases.register(user_register))


if __name__ == '__main__':
    unittest.main()
