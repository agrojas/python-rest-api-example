from app.adapters.database.users.in_memory_user_repository import InMemoryUserRepository
from app.domain.users.model.user import User


def test_user_save():
    user = User(username="tesst", email="test@mail.com")
    user_repository = InMemoryUserRepository()

    assert user.save(user_repository).id == user.id


def test_user_repository_all():
    user_repository = InMemoryUserRepository()
    user1 = User(username="tesst", email="test@mail.com").save(user_repository)
    user2 = User(username="tesst", email="test@mail.com").save(user_repository)

    assert set(user_repository.all()) == {user1, user2}


def test_user_repository_total():
    user_repository = InMemoryUserRepository()
    User(username="tesst", email="test@mail.com").save(user_repository)
    User(username="tesst", email="test@mail.com").save(user_repository)

    assert user_repository.total() == 2
