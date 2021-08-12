import unittest
import uuid


from app.domain.users.model.user import User
from app.domain.users.model.user_id import UserId
from app.domain.users.model.user_status import UserStatus


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
        assert not new_user.is_blocked()

    def test_user_update_status(self):
        user_id = UserId(id=str(uuid.uuid4()))
        new_user = User(username='test', email='email', password='aaaa', id=user_id)
        new_user.update_status(UserStatus.BLOCKED)
        assert new_user.is_blocked()
