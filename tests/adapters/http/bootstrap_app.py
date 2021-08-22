import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.adapters.database.users.model import Base, UserDTO
from app.dependencies.dependencies import get_session
from app.dependencies.dependencies import get_settings
from app.dependencies.dependencies import user_token_validation
from tests.conf.config import settings_to_test


def build_test_db_context():
    engine = create_engine(
        settings_to_test.database_url, connect_args={"check_same_thread": False}
    )
    UserDTO.__table__.create(bind=engine, checkfirst=True)
    session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    Base.metadata.create_all(bind=engine)
    return session()


TestingSessionLocal = build_test_db_context()


def override_get_session():
    try:
        yield TestingSessionLocal
    finally:
        TestingSessionLocal.close()


token_admin = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MjU0Mzg4NzQwNH0.oVgFoLrMgfLRDqoyBO7XrroqwVrwwfPIMBLQOgqpiP8'


def override_get_settings():
    return settings_to_test


def override_validate():
    return True


@pytest.fixture(scope="module")
def test_app():
    # Override environment variables to run TestClient app
    os.environ = settings_to_test.dict()
    from app import main

    client = TestClient(main.app)
    main.app.dependency_overrides[get_settings] = override_get_settings
    main.app.dependency_overrides[get_session] = override_get_session
    main.app.dependency_overrides[user_token_validation] = override_validate
    client.post(
        "/v1/users",
        json={
            "username": "admin",
            "password": "admin",
            "full_name": "admin",
            "email": "admin@example.com",
        },
    )
    yield client  # testing happens here
