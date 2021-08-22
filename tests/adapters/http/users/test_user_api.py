from tests.adapters.http.bootstrap_app import token_admin, test_app


def test_get_users_not_found(test_app: test_app):
    response = test_app.get(
        "/v1/users/123", headers={'Authorization': f'Bearer {token_admin}'}
    )
    assert response.status_code == 404


def test_post_users(test_app: test_app):
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


def test_exist_users_after_created(test_app: test_app):
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


def test_create_users_invalid_body(test_app: test_app):
    create_response = test_app.post(
        "/v1/users",
        json={"username": "string_3", "password": "string", "full_name": "string"},
    )
    assert create_response.status_code == 422


def test_update_users_status(test_app: test_app):
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


def test_update_users_status_invalid_body(test_app: test_app):
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
