import unittest

from app.adapters.database.users.in_memory_user_repository import InMemoryUserRepository
from app.domain.users.model.user import User


class TestUserUseCases(unittest.TestCase):
    db = {}

    def test_user_save(self):
        user = User(username="tesst", email="test@mail.com", password='aaaa')
        user_repository = InMemoryUserRepository(self.db)
        assert user.save(user_repository).id == user.id

    def test_user_repository_all(self):
        user_repository = InMemoryUserRepository(self.db)
        user1 = User(username="tesst", email="test@mail.com", password='aaaa').save(
            user_repository
        )
        user2 = User(username="tesst", email="test@mail.com", password='aaaa').save(
            user_repository
        )
        assert set(user_repository.all()) == {user1, user2}

    def test_user_repository_total(self):
        user_repository = InMemoryUserRepository(self.db)
        User(username="tesst", email="test@mail.com", password='aaaa').save(
            user_repository
        )
        User(username="tesst2", email="test@mail.com", password='aaaa').save(
            user_repository
        )

        assert user_repository.total() == 2
