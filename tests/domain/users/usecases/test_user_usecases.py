import unittest
import uuid
from unittest.mock import MagicMock

from app.domain.users.command.user_create_command import UserCreateCommand
from app.domain.users.command.user_update_status_command import UpdateUserStatusCommand
from app.domain.users.model.user import User
from app.domain.users.model.user_id import UserId
from app.domain.users.model.user_status import UserStatus
from app.domain.users.usecases.user_usecases import UserUseCases
from app.domain.users.model.user_exceptions import UserAlreadyExistException
from app.domain.users.query.user_query import UserQuery


class TestUserUseCases(unittest.TestCase):
    uow = MagicMock()
    pwd_encoder = MagicMock()

    def test_list_empty(self):
        user_usecases = UserUseCases(self.uow, self.pwd_encoder)
        self.uow.repository.all = MagicMock(return_value=[])
        user_query = UserQuery()
        self.assertEqual([], user_usecases.list(user_query))

    def test_list_with_results(self):
        user_id = UserId(id=str(uuid.uuid4()))
        user_mock = User(
            id=user_id, username='mock', email='email@mail.com', password='aaaa'
        )
        self.uow.repository.all = MagicMock(return_value=[user_mock])
        user_usecases = UserUseCases(self.uow, self.pwd_encoder)
        user_query = UserQuery()
        self.assertEqual(user_usecases.list(user_query), [user_mock])

    def test_list_with_filtered_results(self):
        user_id = UserId(id=str(uuid.uuid4()))
        user_mock = User(
            id=user_id, username='mock', email='email@mail.com', password='aaaa'
        )
        self.uow.repository.all = MagicMock(return_value=[user_mock])
        user_usecases = UserUseCases(self.uow, self.pwd_encoder)
        user_query = UserQuery(q='mock')
        self.assertEqual(user_usecases.list(user_query), [user_mock])

    def test_register(self):
        user_id = UserId(id=str(uuid.uuid4()))
        user_mock = User(
            id=user_id, username='mock', email='email@mail.com', password='aaaa'
        )
        self.uow.repository.find_by_email_or_username = MagicMock(return_value=None)
        self.uow.repository.save = MagicMock(return_value=user_mock)
        self.pwd_encoder.encode = MagicMock(return_value='aaaa')
        user_usecases = UserUseCases(self.uow, self.pwd_encoder)
        user_register = UserCreateCommand(
            username='mock', email='email@mail.com', password='1234'
        )
        self.assertIsNotNone(user_usecases.register(user_register))

    def test_register_duplicate_username(self):
        user_id = UserId(id=str(uuid.uuid4()))
        user_mock = User(
            id=user_id, username='mock', email='email-0@mail.com', password='aaaa'
        )
        previous_user_mock = User(
            id=user_id, username='mock', email='email@mail.com', password='aaaa'
        )
        self.uow.repository.find_by_email_or_username = MagicMock(
            return_value=previous_user_mock
        )
        self.uow.repository.save = MagicMock(return_value=user_mock)
        self.pwd_encoder.encode = MagicMock(return_value='aaaa')
        user_usecases = UserUseCases(self.uow, self.pwd_encoder)
        user_register = UserCreateCommand(
            username='mock', email='email@mail.com', password='1234'
        )
        self.assertRaises(
            UserAlreadyExistException, user_usecases.register, user_register
        )

    def test_update_user_status_to_blocked(self):
        user_id = UserId(id=str(uuid.uuid4()))
        user_mock = User(
            id=user_id,
            username='mock',
            email='email@mail.com',
            password='aaaa',
            status=UserStatus.ACTIVE,
        )
        self.uow.repository.find_by_id = MagicMock(return_value=user_mock)
        self.uow.repository.save = MagicMock(return_value=user_mock)
        user_usecases = UserUseCases(self.uow, self.pwd_encoder)
        command = UpdateUserStatusCommand(
            user_id=user_id.id, status=UserStatus.BLOCKED.value
        )
        updated_user = user_usecases.update_status(command)
        assert updated_user.is_blocked()

    def test_update_user_status_to_active(self):
        user_id = UserId(id=str(uuid.uuid4()))
        user_mock = User(
            id=user_id,
            username='mock',
            email='email@mail.com',
            password='aaaa',
            status=UserStatus.BLOCKED,
        )
        self.uow.repository.find_by_id = MagicMock(return_value=user_mock)
        self.uow.repository.save = MagicMock(return_value=user_mock)
        user_usecases = UserUseCases(self.uow, self.pwd_encoder)
        command = UpdateUserStatusCommand(
            user_id=user_id.id, status=UserStatus.ACTIVE.value
        )
        updated_user = user_usecases.update_status(command)
        assert not updated_user.is_blocked()
