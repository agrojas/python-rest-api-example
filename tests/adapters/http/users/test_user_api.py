import unittest
from unittest.mock import MagicMock

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.adapters.database.users.model import Base
from app.main import api


# class TestUserAPI(unittest.TestCase):
#     SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
#
#     engine = create_engine(
#         SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
#     )
#     TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#     Base.metadata.create_all(bind=engine)
#
#     def override_user_usecases_dependency(self):
#         return MagicMock()
#
#
#     client = TestClient(api)
#
#     def test_get_users(self):
#         response = self.client.get("/users")
#         assert response.status_code == 200
#         assert response.json() == []
