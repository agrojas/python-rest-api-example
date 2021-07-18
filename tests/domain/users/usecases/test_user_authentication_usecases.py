import unittest
from unittest.mock import MagicMock

from app.domain.users.command.user_credentials_command import UserCredentialsCommand
from app.domain.users.usecases.user_authentication_usecases import (
    UserAuthenticationUseCases,
)


class TestUserAuthenticationUseCases(unittest.TestCase):
    uow = MagicMock()
    pwd_encoder = MagicMock()

    def test_find_by_credentials(self):
        user_authentication_usecases = UserAuthenticationUseCases(
            self.uow, self.pwd_encoder
        )
        user_with_credentials = MagicMock(return_value=[])
        self.uow.repository.find_by_username = MagicMock(
            return_value=user_with_credentials
        )
        user_credentials_command = UserCredentialsCommand(
            username="test", password="test"
        )
        self.pwd_encoder.verify = MagicMock(return_value=True)
        assert (
            user_authentication_usecases.find_by_credentials(user_credentials_command)
            == user_with_credentials
        )

    def test_find_by_credentials_username_not_found(self):
        user_authentication_usecases = UserAuthenticationUseCases(
            self.uow, self.pwd_encoder
        )
        self.uow.repository.find_by_username = MagicMock(return_value=None)
        user_credentials_command = UserCredentialsCommand(
            username="test", password="test"
        )
        self.pwd_encoder.verify = MagicMock(return_value=True)
        assert (
            user_authentication_usecases.find_by_credentials(user_credentials_command)
            is None
        )

    def test_find_by_credentials_wrong_password(self):
        user_authentication_usecases = UserAuthenticationUseCases(
            self.uow, self.pwd_encoder
        )
        user_with_credentials = MagicMock(return_value=[])
        self.uow.repository.find_by_username = MagicMock(
            return_value=user_with_credentials
        )
        user_credentials_command = UserCredentialsCommand(
            username="test", password="test"
        )
        self.pwd_encoder.verify = MagicMock(return_value=False)
        assert (
            user_authentication_usecases.find_by_credentials(user_credentials_command)
            is None
        )
