import unittest
import uuid

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.adapters.database.users.model import Base
from app.adapters.database.users.sql_user_repository import SQLUserRepository
from app.domain.users.model.user import User
from app.domain.users.model.user_id import UserId
from tests.conf.config import settings_to_test


class TestSQLUserRepository(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine(settings_to_test.database_url)
        self.session = Session(self.engine)
        Base.metadata.create_all(self.engine)
        self.session.commit()

    def tearDown(self):
        Base.metadata.drop_all(self.engine)

    def test_user_save(self):
        user_id = UserId(id=str(uuid.uuid4()))
        user = User(
            id=user_id, username="tesst1", email="test@mail.com", password='aaaa'
        )
        user_repository = SQLUserRepository(self.session)
        user.save(user_repository)
        retrived_user = user_repository.find_by_id(user_id)
        assert retrived_user.id == user.id

    def test_user_repository_all(self):
        user_repository = SQLUserRepository(self.session)
        user1 = User(
            id=UserId(id=str(uuid.uuid4())),
            username="tesst2",
            email="test2@mail.com",
            password='aaaa',
        )
        user1.save(user_repository)

        assert user_repository.all() == [user1]

    def test_user_repository_total(self):
        user_repository = SQLUserRepository(self.session)
        User(
            id=UserId(id=str(uuid.uuid4())),
            username="tesst4",
            email="test4@mail.com",
            password='aaaa',
        ).save(user_repository)
        User(
            id=UserId(id=str(uuid.uuid4())),
            username="tesst5",
            email="test5@mail.com",
            password='aaaa',
        ).save(user_repository)

        assert user_repository.total() == 2

    def test_user_repository_find_by_username(self):
        user_repository = SQLUserRepository(self.session)
        User(
            id=UserId(id=str(uuid.uuid4())),
            username="tesst4",
            email="test4@mail.com",
            password='aaaa',
        ).save(user_repository)
        user2 = User(
            id=UserId(id=str(uuid.uuid4())),
            username="tesst5",
            email="test5@mail.com",
            password='aaaa',
        )
        user2.save(user_repository)

        assert user_repository.find_by_username("tesst5") == user2

    def test_user_repository_find_by_id(self):
        user_repository = SQLUserRepository(self.session)
        id_user_1 = UserId(id=str(uuid.uuid4()))
        user1 = User(
            id=id_user_1, username="tesst4", email="test4@mail.com", password='aaaa',
        )
        user1.save(user_repository)
        user2 = User(
            id=UserId(id=str(uuid.uuid4())),
            username="tesst5",
            email="test5@mail.com",
            password='aaaa',
        )
        user2.save(user_repository)

        assert user_repository.find_by_id(id_user_1) == user1
