import unittest
from unittest.mock import MagicMock

from app.adapters.http.auth.exceptions.authentication_exception import (
    AuthenticationException,
)
from app.adapters.http.auth.jwt_authenticator import JwtAuthenticator
from app.domain.users.model.user import User
from app.domain.users.model.user_id import UserId
from tests.conf.config import settings_to_test


class TestJwtAuthenticator(unittest.TestCase):

    user_usecases = MagicMock()
    jwt_authenticator = JwtAuthenticator(user_usecases, settings=settings_to_test)

    def test_fail_with_invalid_jwt(self):
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.5mhBHqs5_DTLdINd9p5m7ZJ6XD0Xc55kIaCRY5rinvalid"
        self.assertRaises(
            AuthenticationException, self.jwt_authenticator.authenticate, token
        )

    def test_fail_with_wrong_credentials(self):
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.5mhBHqs5_DTLdINd9p5m7ZJ6XD0Xc55kIaCRY5r6HRA"
        self.user_usecases.user_uow.repository.find_by_username = MagicMock(
            return_value=None
        )
        self.assertRaises(
            AuthenticationException, self.jwt_authenticator.authenticate, token
        )

    def test_valid_credentials(self):
        user = User(
            id=UserId("id"), username="asd", password="asd", email="asd@asd.com"
        )
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.5mhBHqs5_DTLdINd9p5m7ZJ6XD0Xc55kIaCRY5r6HRA"
        self.user_usecases.user_uow.repository.find_by_username = MagicMock(
            return_value=user
        )
        user_result = self.jwt_authenticator.authenticate(token)
        assert user_result.username == user.username
