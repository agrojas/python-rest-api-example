import unittest
import uuid


from app.domain.users.model.user import User
from app.domain.users.model.user_id import UserId


class TestUserUseCases(unittest.TestCase):
    def test_user_existing_user_id(self):
        user_id = UserId(id=str(uuid.uuid4()))
        assert (
            User(username='test', email='email', id=user_id, password='aaaa').id
            == user_id
        )

    def test_user_defaults(self):
        user_id = UserId(id=str(uuid.uuid4()))
        user_id2 = UserId(id=str(uuid.uuid4()))
        new_user = User(username='test', email='email', password='aaaa', id=user_id)
        assert new_user.id != user_id2
        assert new_user.is_active
