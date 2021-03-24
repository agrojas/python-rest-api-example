import uuid
from app.domain.users.model.user import User


def test_user_existing_user_id():
    user_id = uuid.uuid4()
    assert User(username='test', email='email', id=user_id).id == user_id


def test_user_defaults():
    user_id = uuid.uuid4()
    assert User(username='test', email='email').id != user_id