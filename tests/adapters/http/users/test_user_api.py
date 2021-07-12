import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import main
from app.adapters.database.users.model import Base, UserDTO
from app.dependencies.dependencies import get_session, get_settings
from tests.conf.config import settings_to_test


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


def override_get_settings():
    return settings_to_test


@pytest.fixture(scope="module")
def test_app():
    client = TestClient(main.app)
    main.app.dependency_overrides[get_settings] = override_get_settings
    main.app.dependency_overrides[get_session] = override_get_db
    build_test_db_context()
    yield client  # testing happens here


def build_test_db_context():
    global TestingSessionLocal
    engine = create_engine(
        settings_to_test.database_url, connect_args={"check_same_thread": False}
    )
    UserDTO.__table__.create(bind=engine, checkfirst=True)
    TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    Base.metadata.create_all(bind=engine)


def test_get_users_empty(test_app):
    response = test_app.get("/users")
    assert response.status_code == 200
    assert response.json() == []


def test_get_users_not_found(test_app):
    response = test_app.get("/users/123")
    assert response.status_code == 404


def test_post_users(test_app):
    response = test_app.post(
        "/users",
        json={
            "username": "string",
            "password": "string",
            "full_name": "string",
            "email": "user@example.com",
        },
    )
    assert response.status_code == 200
    assert response.json() is not None
    assert response.json()['id'] is not None
    assert response.json()['username'] == 'string'
    assert response.json()['full_name'] == 'string'
    assert response.json()['email'] == 'user@example.com'
    assert response.json()['is_active']


def test_exist_users_after_created(test_app):
    create_response = test_app.post(
        "/users",
        json={
            "username": "string_2",
            "password": "string",
            "full_name": "string",
            "email": "user_2@example.com",
        },
    )
    assert create_response.status_code == 200
    user_id = create_response.json()['id']
    response = test_app.get("/users/" + str(user_id))
    assert response.status_code == 200
    assert response.json() is not None
    assert response.json()['id'] == user_id
    assert response.json()['username'] == 'string_2'
    assert response.json()['full_name'] == 'string'
    assert response.json()['email'] == 'user_2@example.com'
    assert response.json()['is_active']


def test_create_users_invalid_body(test_app):
    create_response = test_app.post(
        "/users",
        json={"username": "string_3", "password": "string", "full_name": "string"},
    )
    assert create_response.status_code == 422
