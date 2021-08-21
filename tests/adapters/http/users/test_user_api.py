import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.adapters.database.users.model import Base, UserDTO
from app.dependencies.dependencies import get_session
from app.dependencies.dependencies import get_settings
from tests.conf.config import settings_to_test


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


test_envs = {
    "ENVIRONMENT": "local",
    "VERSION_PREFIX": "/v1",
    "VERSION": "1.0",
    "TITLE": "Users API",
    "DESCRIPTION": "This is an example for a users service",
    "SECRET_KEY": "test",
    "ALGORITHM": "HS256",
    "ACCESS_TOKEN_EXPIRE_MINUTES": 30,
    "DATABASE_URL": "sqlite:///:memory:",
    "PORT": 5000,
}

token_admin = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MjU0Mzg4NzQwNH0.oVgFoLrMgfLRDqoyBO7XrroqwVrwwfPIMBLQOgqpiP8'


def override_get_settings():
    return settings_to_test


@pytest.fixture(scope="module")
def test_app():
    # Override environment variables to run TestClient app
    os.environ = test_envs
    from app import main

    client = TestClient(main.app)
    main.app.dependency_overrides[get_settings] = override_get_settings
    main.app.dependency_overrides[get_session] = override_get_db
    build_test_db_context()
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


def build_test_db_context():
    global TestingSessionLocal
    engine = create_engine(
        settings_to_test.database_url, connect_args={"check_same_thread": False}
    )
    UserDTO.__table__.create(bind=engine, checkfirst=True)
    TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    Base.metadata.create_all(bind=engine)


def test_get_users_not_found(test_app):
    response = test_app.get(
        "/v1/users/123", headers={'Authorization': f'Bearer {token_admin}'}
    )
    assert response.status_code == 404


def test_post_users(test_app):
    response = test_app.post(
        "/v1/users",
        json={
            "username": "string",
            "password": "string",
            "full_name": "string",
            "email": "user@example.com",
        },
    )
    assert response.status_code == 201
    assert response.json() is not None
    assert response.json()['id'] is not None
    assert response.json()['username'] == 'string'
    assert response.json()['full_name'] == 'string'
    assert response.json()['email'] == 'user@example.com'
    assert response.json()['status'] == 'ACTIVE'


def test_exist_users_after_created(test_app):
    create_response = test_app.post(
        "/v1/users",
        json={
            "username": "string_2",
            "password": "string",
            "full_name": "string",
            "email": "user_2@example.com",
        },
    )
    assert create_response.status_code == 201
    user_id = create_response.json()['id']
    response = test_app.get(
        f'/v1/users/{user_id}', headers={'Authorization': f'Bearer {token_admin}'}
    )
    assert response.status_code == 200
    assert response.json() is not None
    assert response.json()['id'] == user_id
    assert response.json()['username'] == 'string_2'
    assert response.json()['full_name'] == 'string'
    assert response.json()['email'] == 'user_2@example.com'
    assert response.json()['status'] == 'ACTIVE'


def test_create_users_invalid_body(test_app):
    create_response = test_app.post(
        "/v1/users",
        json={"username": "string_3", "password": "string", "full_name": "string"},
    )
    assert create_response.status_code == 422


def test_update_users_status(test_app):
    create_response = test_app.post(
        "/v1/users",
        json={
            "username": "string_3",
            "password": "secure",
            "full_name": "string",
            "email": "user_3@example.com",
        },
    )
    assert create_response.status_code == 201
    user_id = create_response.json()['id']
    response = test_app.patch(
        f'/v1/users/{user_id}/status',
        json={"status": "BLOCKED"},
        headers={'Authorization': f'Bearer {token_admin}'},
    )
    assert response.status_code == 202
    assert response.json() is not None
    assert response.json()['id'] == user_id
    assert response.json()['status'] == 'BLOCKED'


def test_update_users_status_invalid_body(test_app):
    create_response = test_app.post(
        "/v1/users",
        json={
            "username": "string_4",
            "password": "secure",
            "full_name": "string",
            "email": "user_4@example.com",
        },
    )
    assert create_response.status_code == 201
    user_id = create_response.json()['id']
    response = test_app.patch(
        f'/v1/users/{user_id}/status',
        json={"status": "INVALID"},
        headers={'Authorization': f'Bearer {token_admin}'},
    )
    assert response.status_code == 422
