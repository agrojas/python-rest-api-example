import unittest

from app.adapters.http.auth.jwt_user_signer import JwtUserSigner
from tests.conf.config import settings_to_test


class TestJwtAuthenticator(unittest.TestCase):
    def test_encode_is_not_none(self):
        result = JwtUserSigner(settings_to_test).create_access_token("username")
        assert result is not None
